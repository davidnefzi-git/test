#!/usr/bin/env python3
"""
enrich_leis.py — Enrichissement d'un fichier Excel de LEI via l'API GLEIF.

Étapes principales :
1. Connexion à Google Drive (OAuth2 desktop) et téléchargement du fichier .xlsx
2. Détection automatique de la colonne LEI et nettoyage des valeurs
3. Interrogation de l'API GLEIF (avec retry, throttle, checkpoint)
4. Construction et export du fichier enrichi taxonomy_gelif_enriched.xlsx
"""

import os
import sys
import re
import time
import json
import logging
import pickle
import importlib
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# 0. Installation automatique des dépendances manquantes
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES = {
    "openpyxl": "openpyxl",
    "pandas": "pandas",
    "requests": "requests",
    "tqdm": "tqdm",
}

def install_missing():
    missing = []
    for module, pkg in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"[INFO] Installation des dépendances manquantes : {', '.join(missing)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet"] + missing)
        print("[INFO] Installation terminée.")

install_missing()

# ---------------------------------------------------------------------------
# Imports après installation
# ---------------------------------------------------------------------------
import pandas as pd
import requests
from tqdm import tqdm

# ---------------------------------------------------------------------------
# 1. Configuration du logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename="errors.log",
    level=logging.WARNING,
    format="%(asctime)s — %(levelname)s — %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 2. Constantes
# ---------------------------------------------------------------------------
GLEIF_BASE = "https://api.gleif.org/api/v1"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "credentials.json"
OUTPUT_FILE = "taxonomy_gelif_enriched.xlsx"
CHECKPOINT_FILE = "checkpoint.json"
REQUEST_DELAY = 0.5   # secondes entre chaque requête GLEIF
MAX_RETRIES = 4
RETRY_BACKOFF = [2, 4, 8, 16]  # secondes

# ---------------------------------------------------------------------------
# 3. Connexion Google Drive
# ---------------------------------------------------------------------------

def get_drive_service():
    """Retourne un service Google Drive authentifié (OAuth2 desktop)."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as fh:
            creds = pickle.load(fh)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Fichier '{CREDENTIALS_FILE}' introuvable. "
                    "Téléchargez vos identifiants OAuth2 depuis la console Google Cloud "
                    "et placez-les dans le répertoire courant."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as fh:
            pickle.dump(creds, fh)

    return build("drive", "v3", credentials=creds)


def find_and_download_xlsx(service, folder_name="taxonomy_gelif"):
    """Cherche le dossier et télécharge le premier .xlsx trouvé."""
    from googleapiclient.http import MediaIoBaseDownload
    import io

    # Chercher le dossier
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id,name)").execute()
    folders = results.get("files", [])
    if not folders:
        raise FileNotFoundError(f"Dossier '{folder_name}' introuvable sur Google Drive.")
    folder_id = folders[0]["id"]
    print(f"[INFO] Dossier trouvé : {folder_name} (id={folder_id})")

    # Chercher les .xlsx dans le dossier
    query = (
        f"'{folder_id}' in parents and "
        "mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' and "
        "trashed=false"
    )
    results = service.files().list(q=query, fields="files(id,name)").execute()
    files = results.get("files", [])
    if not files:
        raise FileNotFoundError(f"Aucun fichier .xlsx trouvé dans '{folder_name}'.")

    file_meta = files[0]
    print(f"[INFO] Fichier trouvé : {file_meta['name']}")

    request = service.files().get_media(fileId=file_meta["id"])
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    buf.seek(0)
    local_path = file_meta["name"]
    with open(local_path, "wb") as fh:
        fh.write(buf.read())
    print(f"[INFO] Fichier téléchargé : {local_path}")
    return local_path


def download_via_gdown(share_url: str) -> str:
    """Télécharge un fichier Google Drive via un lien de partage public."""
    import gdown
    output = "input_leis.xlsx"
    gdown.download(share_url, output, quiet=False, fuzzy=True)
    return output


# ---------------------------------------------------------------------------
# 4. Acquisition du fichier (Drive ou fallback gdown)
# ---------------------------------------------------------------------------

def _drive_available() -> bool:
    """Vérifie rapidement si les bibliothèques Google Drive sont utilisables."""
    try:
        from google.oauth2.credentials import Credentials  # noqa: F401
        return True
    except BaseException:
        return False


def _prompt_fallback() -> str:
    """Propose à l'utilisateur une alternative à Google Drive OAuth2."""
    print("\nAuthentification Google Drive non disponible dans cet environnement.")
    print("Options de remplacement :")
    print("  1. Fournir un lien de partage public Google Drive")
    print("  2. Spécifier un chemin local vers le fichier .xlsx")
    choice = input("Votre choix (1/2) : ").strip()
    if choice == "1":
        url = input("Lien de partage Google Drive : ").strip()
        return download_via_gdown(url)
    else:
        path = input("Chemin local du fichier .xlsx : ").strip()
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fichier introuvable : {path}")
        return path


def acquire_input_file() -> str:
    """
    Tente l'authentification Google Drive. Si elle échoue, propose gdown ou chemin local.
    Retourne le chemin local du fichier .xlsx.
    """
    if not _drive_available():
        logger.warning("Bibliothèques Google Drive inutilisables dans cet environnement.")
        return _prompt_fallback()

    try:
        service = get_drive_service()
        return find_and_download_xlsx(service)
    except Exception as exc:
        print(f"[AVERTISSEMENT] Google Drive inaccessible : {exc}")
        logger.warning("Échec Drive : %s", exc)
        return _prompt_fallback()


# ---------------------------------------------------------------------------
# 5. Lecture et détection de la colonne LEI
# ---------------------------------------------------------------------------

LEI_COLUMN_CANDIDATES = [
    "LEI", "lei", "Lei", "LegalEntityIdentifier", "legal_entity_identifier",
    "LEI_Code", "lei_code", "LEI Code", "Code LEI",
]
LEI_PATTERN = re.compile(r"^[A-Z0-9]{20}$")


def detect_lei_column(df: pd.DataFrame) -> str:
    """Détecte automatiquement la colonne LEI dans le DataFrame."""
    matched = [c for c in df.columns if c in LEI_COLUMN_CANDIDATES]

    if len(matched) == 1:
        print(f"[INFO] Colonne LEI détectée : '{matched[0]}'")
        return matched[0]

    if len(matched) > 1:
        print(f"[INFO] Plusieurs colonnes candidates : {matched}")
        for i, col in enumerate(matched):
            print(f"  {i}: {col}")
        idx = int(input("Numéro de la colonne à utiliser : ").strip())
        return matched[idx]

    # Recherche heuristique : colonne dont >50 % des valeurs ressemblent à des LEI
    for col in df.columns:
        sample = df[col].dropna().astype(str).str.strip().str.upper()
        if sample.empty:
            continue
        ratio = sample.str.match(r"^[A-Z0-9]{20}$").mean()
        if ratio > 0.5:
            print(f"[INFO] Colonne LEI détectée par heuristique : '{col}' ({ratio:.0%} valides)")
            return col

    raise ValueError(
        "Impossible de détecter automatiquement la colonne LEI. "
        "Vérifiez les noms de colonnes du fichier."
    )


def clean_lei(value) -> str:
    """Nettoie et valide une valeur LEI. Retourne None si invalide."""
    if pd.isna(value):
        return None
    lei = str(value).strip().upper()
    if LEI_PATTERN.match(lei):
        return lei
    return None


# ---------------------------------------------------------------------------
# 6. Interrogation API GLEIF
# ---------------------------------------------------------------------------

def gleif_get(url: str) -> dict | None:
    """Effectue une requête GET sur l'API GLEIF avec retry et backoff."""
    for attempt, wait in enumerate([0] + RETRY_BACKOFF):
        if wait:
            time.sleep(wait)
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 404:
                return None  # LEI inconnu, pas la peine de réessayer
            if resp.status_code == 429:
                logger.warning("Rate-limit atteint, pause 30s (attempt %d)", attempt)
                time.sleep(30)
                continue
            logger.warning("HTTP %d pour %s (attempt %d)", resp.status_code, url, attempt)
        except requests.exceptions.Timeout:
            logger.warning("Timeout pour %s (attempt %d)", url, attempt)
        except requests.exceptions.ConnectionError as exc:
            logger.warning("Connexion refusée pour %s : %s (attempt %d)", url, exc, attempt)
    return "ERROR"  # toutes les tentatives échouées


def extract_entity_fields(data: dict) -> dict:
    """Extrait les champs pertinents d'un enregistrement LEI (nœud 'data')."""
    attrs = data.get("attributes", {})
    entity = attrs.get("entity", {})
    reg = attrs.get("registration", {})
    address = entity.get("legalAddress", {})

    return {
        "entity_name": entity.get("legalName", {}).get("name", "N/A"),
        "entity_city": address.get("city", "N/A"),
        "entity_country": address.get("country", "N/A"),
        "entity_status": reg.get("status", "N/A"),
        "entity_category": entity.get("category", "N/A"),
    }


def get_ultimate_parent_lei(data_node: dict, relationships: dict) -> str | None:
    """
    Retourne le LEI de l'ultimate parent depuis les relationships GLEIF.
    Retourne None si absent ou si l'entité est son propre parent.
    """
    self_lei = data_node.get("id", "")
    up = relationships.get("ultimate-parent", {})
    parent_data = up.get("data")
    if not parent_data:
        return None
    parent_lei = parent_data.get("id", "")
    if parent_lei == self_lei:
        return "SELF"
    return parent_lei or None


def fetch_lei_info(lei: str) -> dict:
    """
    Interroge l'API GLEIF pour un LEI et retourne un dict avec toutes les colonnes.
    """
    empty_parent = {
        "ultimate_parent_lei": "N/A",
        "ultimate_parent_name": "N/A",
        "ultimate_parent_city": "N/A",
        "ultimate_parent_country": "N/A",
        "ultimate_parent_status": "N/A",
    }

    url = f"{GLEIF_BASE}/lei-records/{lei}"
    result = gleif_get(url)

    if result is None:
        return {
            "entity_name": "LEI_INCONNU",
            "entity_city": "N/A",
            "entity_country": "N/A",
            "entity_status": "N/A",
            "entity_category": "N/A",
            **empty_parent,
        }

    if result == "ERROR":
        return {
            "entity_name": "ERREUR_API",
            "entity_city": "ERREUR_API",
            "entity_country": "ERREUR_API",
            "entity_status": "ERREUR_API",
            "entity_category": "ERREUR_API",
            **{k: "ERREUR_API" for k in empty_parent},
        }

    data_node = result.get("data", {})
    relationships = data_node.get("relationships", {})
    entity_fields = extract_entity_fields(data_node)

    parent_lei = get_ultimate_parent_lei(data_node, relationships)

    if parent_lei is None:
        parent_fields = empty_parent
    elif parent_lei == "SELF":
        parent_fields = {
            "ultimate_parent_lei": "Même entité",
            "ultimate_parent_name": "Même entité",
            "ultimate_parent_city": "N/A",
            "ultimate_parent_country": "N/A",
            "ultimate_parent_status": "N/A",
        }
    else:
        time.sleep(REQUEST_DELAY)
        parent_url = f"{GLEIF_BASE}/lei-records/{parent_lei}"
        parent_result = gleif_get(parent_url)
        if parent_result and parent_result != "ERROR":
            p = extract_entity_fields(parent_result.get("data", {}))
            parent_fields = {
                "ultimate_parent_lei": parent_lei,
                "ultimate_parent_name": p["entity_name"],
                "ultimate_parent_city": p["entity_city"],
                "ultimate_parent_country": p["entity_country"],
                "ultimate_parent_status": p["entity_status"],
            }
        else:
            parent_fields = {
                "ultimate_parent_lei": parent_lei,
                "ultimate_parent_name": "ERREUR_API" if parent_result == "ERROR" else "LEI_INCONNU",
                "ultimate_parent_city": "N/A",
                "ultimate_parent_country": "N/A",
                "ultimate_parent_status": "N/A",
            }

    return {**entity_fields, **parent_fields}


# ---------------------------------------------------------------------------
# 7. Checkpoint
# ---------------------------------------------------------------------------

def load_checkpoint() -> dict:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_checkpoint(cache: dict):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as fh:
        json.dump(cache, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 8. Pipeline principal
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Enrichissement LEI via GLEIF")
    print("=" * 60)

    # — Acquisition du fichier
    local_file = acquire_input_file()

    # — Lecture Excel
    print(f"\n[INFO] Lecture du fichier : {local_file}")
    df = pd.read_excel(local_file, dtype=str)
    print(f"[INFO] {len(df)} lignes, colonnes : {list(df.columns)}")

    # — Détection colonne LEI
    lei_col = detect_lei_column(df)

    # — Nettoyage LEI
    df["_lei_clean"] = df[lei_col].apply(clean_lei)
    invalid_count = df["_lei_clean"].isna().sum()
    if invalid_count:
        print(f"[AVERTISSEMENT] {invalid_count} valeurs LEI invalides ou manquantes (ignorées).")
        logger.warning("%d LEI invalides ignorés", invalid_count)

    unique_leis = df["_lei_clean"].dropna().unique().tolist()
    print(f"[INFO] {len(unique_leis)} LEI uniques valides à traiter.")

    # — Chargement du checkpoint
    cache = load_checkpoint()
    already_done = sum(1 for lei in unique_leis if lei in cache)
    print(f"[INFO] {already_done} LEI déjà traités (reprise depuis checkpoint).")

    # — Traitement des LEI
    NEW_COLUMNS = [
        "entity_name", "entity_city", "entity_country", "entity_status", "entity_category",
        "ultimate_parent_lei", "ultimate_parent_name",
        "ultimate_parent_city", "ultimate_parent_country", "ultimate_parent_status",
    ]

    to_process = [lei for lei in unique_leis if lei not in cache]
    if to_process:
        print(f"\n[INFO] Traitement de {len(to_process)} LEI(s) restants...")
        for lei in tqdm(to_process, desc="GLEIF API", unit="LEI"):
            cache[lei] = fetch_lei_info(lei)
            save_checkpoint(cache)
            time.sleep(REQUEST_DELAY)
    else:
        print("[INFO] Tous les LEI sont déjà dans le cache.")

    # — Construction du DataFrame enrichi
    rows = []
    for _, row in df.iterrows():
        lei = row["_lei_clean"]
        if pd.isna(lei) or lei is None:
            enriched = {col: "LEI_INVALIDE" for col in NEW_COLUMNS}
        else:
            enriched = cache.get(lei, {col: "NON_TROUVÉ" for col in NEW_COLUMNS})
        rows.append(enriched)

    enriched_df = pd.DataFrame(rows)
    df = df.drop(columns=["_lei_clean"])
    result_df = pd.concat([df.reset_index(drop=True), enriched_df.reset_index(drop=True)], axis=1)

    # — Export
    result_df.to_excel(OUTPUT_FILE, index=False)
    print(f"\n[OK] Fichier enrichi exporté : {OUTPUT_FILE}")
    print(f"[OK] Erreurs consignées dans : errors.log")
    if os.path.exists(CHECKPOINT_FILE):
        print(f"[OK] Checkpoint conservé dans : {CHECKPOINT_FILE}")


if __name__ == "__main__":
    main()
