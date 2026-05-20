"""
UCI Classification Script — Pillar 1 + 2 + 3
Applies 3-pillar strategy from taxonomy_uci_classification_strategy.md
to taxonomy_gleif_corrected.xlsx → taxonomy_gleif_classified.xlsx
"""

import pandas as pd
import numpy as np
import re

INPUT  = "/home/user/test/taxonomy_gleif_corrected.xlsx"
OUTPUT = "/home/user/test/taxonomy_gleif_classified.xlsx"

# ---------------------------------------------------------------------------
# LEI-based lookup for non-Latin names (Chinese / Japanese / Korean / TW)
# Format: UCI_LEI -> (uci_category, country)
# ---------------------------------------------------------------------------
LEI_CATEGORY_MAP = {
    # Chinese G-SIBs
    "54930053HGCFWVHYZX42": ("GSIB_nonUS", "CN"),   # 中国银行 Bank of China
    "5493002ERZU2K9PZDL40": ("GSIB_nonUS", "CN"),   # 中国工商银行 ICBC
    "5493001KQW6DM7KEDR62": ("GSIB_nonUS", "CN"),   # 中国建设银行 CCB
    "549300E7TSGLCOVSY746": ("GSIB_nonUS", "CN"),   # 中国农业银行 AgBank
    "549300AX1UM10U30HK09": ("GSIB_nonUS", "CN"),   # 交通银行 BoCom
    # Fallback GLEIF LEIs for Chinese G-SIBs
    "JZVGT2Y6MXOILG9LCL20": ("GSIB_nonUS", "CN"),
    "B29QUI9A3LCHNWMQNB51": ("GSIB_nonUS", "CN"),
    "I7331LVCZKQKX5T5VQ57": ("GSIB_nonUS", "CN"),
    "B4TYDEB6GKMZO031MB27": ("GSIB_nonUS", "CN"),
    "9ZUIEKY5I1RMBKMTCO21": ("GSIB_nonUS", "CN"),
    # Japanese G-SIBs
    "353800V2V8PUY9TK3E06": ("GSIB_nonUS", "JP"),   # 三菱UFJフィナンシャルG MUFG
    "35380028MYWPB6AUO129": ("GSIB_nonUS", "JP"),   # 三井住友FG SMFG
    "5U0XI89JRFVHWIBS4F54": ("GSIB_nonUS", "JP"),   # 三井住友銀行 SMBC
    "353800CI5L6DDAN5XZ33": ("GSIB_nonUS", "JP"),   # みずほFG Mizuho
    "549300B3CEAHYG7K8164": ("GSIB_nonUS", "JP"),   # 野村HD Nomura Holdings
    "54930025BDY2HW6EF014": ("GSIB_nonUS", "CH"),   # 瑞士信貸(香港) Credit Suisse HK
    # Chinese other banks
    "300300C1030935001303": ("Bank_Other", "CN"),   # 兴业银行 Industrial Bank
    "300300AKNDEHIGVDZW37": ("Bank_Other", "CN"),   # 华夏银行 HuaxiaBank
    "300300C1031031001330": ("Bank_Other", "CN"),   # 浦发银行 SPDB
    "300300C1031633000208": ("Bank_Other", "CN"),   # 浙商银行
    "300300C1069331000086": ("Bank_Other", "CN"),   # 东方汇理银行(中国) Amundi China
    "300300C1086832000046": ("Bank_Other", "CN"),   # 江苏银行
    "300300C1092133000091": ("Bank_Other", "CN"),   # 宁波银行
    "549300HBUGSQD1VCXG94": ("Bank_Other", "CN"),   # 中国民生银行 CMBC
    "549300MKO5B60FFIHF58": ("Bank_Other", "CN"),   # 招商银行 CMB
    "300300C1030211000384": ("Bank_Other", "CN"),   # 中信银行 CITIC Bank
    "300300NIFA1100057377": ("Bank_Other", "CN"),   # 中国中信集团 CITIC Group
    # Chinese insurance
    "529900BA5ILEL308WX03": ("InsurancePension", "CN"),  # 中国太平洋保险 CPIC
    "300300S6Z7Z0G5MZKF86": ("InsurancePension", "CN"),  # 中国人寿保险集团 China Life
    "254900GB3V5T9KMKQT53": ("InsurancePension", "HK"),  # 中國人壽保險(海外) China Life HK
    # Chinese corporate
    "300300FEEFS8BQPXIV57": ("Corporate_Industrial", "CN"),  # 歌尔股份 GoerTek
    "3003003TRPHLHZD2IF61": ("Corporate_Industrial", "CN"),  # 美的集团 Midea
    "3003004E77BXPPJ1H509": ("Corporate_Industrial", "HK"),  # 永青集团 HK
    "3003006NEE85FZWERU37": ("Corporate_Industrial", "HK"),  # 中兴通讯HK ZTE
    "3003007EXL0825P1MJ10": ("Corporate_Industrial", "TW"),  # 群創光電 Innolux
    "3003009FOUMDW0ANZ412": ("Corporate_Industrial", "CN"),  # 华晨宝马 BMW Brilliance JV
    "3003003B3HWW4VKZYK94": ("Corporate_Industrial", "CN"),  # 浙商中拓
    "300300OC39LS1GEO8K91": ("Corporate_Industrial", "CN"),  # 杭州热联集团
    "300300U0SYTSNVT4Y161": ("Corporate_Industrial", "CN"),  # 广州越秀集团
    "300300CWNOP91UK67Q39": ("Corporate_Industrial", "HK"),  # 香港天源
    "300300FC31JXHL0MCE95": ("Corporate_Industrial", "SG"),  # 中石油财务(新加坡)
    "836800D3BMI4CG7VXS63": ("Corporate_Industrial", "CN"),  # 立铠精密科技
    "6556009GPZKYO37T6987": ("Corporate_Industrial", "HK"),  # 百度HK Baidu
    "655600K2J6FGZ1EP8281": ("Corporate_Industrial", "HK"),  # 科兴控股 Sinovac
    "30030004CM3GSZXX7O56": ("Corporate_Industrial", "TW"),  # 鸿海精密 Foxconn
    "213800NIZ8C8KBEXUI96": ("Corporate_Industrial", "HK"),  # 香港華為 Huawei HK
    "254900B3WB4OGRB7HM13": ("Corporate_Industrial", "TW"),  # 華碩電腦 ASUS
    "254900ZXV0XDSPS4SJ31": ("Corporate_Industrial", "SG"),  # 新奥天然气(新加坡)
    # Japanese insurance
    "5299009QN2NZ191KLS29": ("InsurancePension", "JP"),  # 東京海上HD Tokio Marine
    "353800CWW4SRGEYEB512": ("InsurancePension", "JP"),  # SOMPOホールディングス
    "549300I5OQCDADQSPI57": ("InsurancePension", "JP"),  # 住友生命保険
    "549300JDVRDBH680VF26": ("InsurancePension", "JP"),  # 富国生命保険
    "549300Y0HHMFW3EVWY08": ("InsurancePension", "JP"),  # 日本生命保険
    "549300SLU4LP6YMRLK07": ("InsurancePension", "JP"),  # 明治安田生命保険
    "353800CLHMU44O1XGX62": ("InsurancePension", "JP"),  # 大同生命保険
    "3538008ARJ1MACEWA242": ("InsurancePension", "JP"),  # T&Dホールディングス
    "549300T1BG1ICC1YND13": ("InsurancePension", "HK"),  # 安達人壽保險香港 Chubb Life HK
    "549300QTTCJ72V42ZG09": ("InsurancePension", "JP"),  # 全国共済農業協同組合 JA Kyosai
    "213800T38ERVY7FN8L42": ("InsurancePension", "JP"),  # アクサ生命保険 AXA Life JP
    # Japanese corporate
    "KVIPTY4PULAPGC1VVD26": ("Corporate_Industrial", "JP"),  # 三菱商事 Mitsubishi Corp
    "2NRSB4GOU9DD6CNW5R48": ("Corporate_Industrial", "JP"),  # 三井物産 Mitsui
    "4P4N3ORD02UGQT1T1W12": ("Corporate_Industrial", "JP"),  # 丸紅 Marubeni
    "V82KK8NH1P0JS71FJC05": ("Corporate_Industrial", "JP"),  # 住友商事 Sumitomo Corp
    "5493006W3QUS5LMH6R84": ("Corporate_Industrial", "JP"),  # トヨタ自動車 Toyota
    "549300T6IPOCDWLKC615": ("Corporate_Industrial", "JP"),  # 日立製作所 Hitachi
    "8EUP1TJYZFX3T1E5AJ33": ("Corporate_Industrial", "JP"),  # 阪和興業 Hanwa
    "353800PFUKP5ONPJNZ86": ("Corporate_Industrial", "JP"),  # 関西電力 Kansai Electric
    "353800OO5E7W1FV1SB75": ("Corporate_Industrial", "JP"),  # JERA
    "353800BRAE0QFP3ZLY22": ("Corporate_Industrial", "JP"),  # 清水建設 Shimizu
    "353800YEPK9PD7QO3449": ("Corporate_Industrial", "JP"),  # シャープ Sharp
    "3538001KQ5SAOZSQTT44": ("Corporate_Industrial", "JP"),  # ENEOSホールディングス
    "35380034IXNKM8B8SU08": ("Corporate_Industrial", "JP"),  # ジャパン・フード・サービス
    "353800GRN97NR54RGC94": ("Corporate_Industrial", "JP"),  # TGグローバルトレーディング
    "353800RNB2UPUVYX4W34": ("Corporate_Industrial", "JP"),  # 山新
    "5493006B73PSJ6SAEP96": ("Corporate_Industrial", "HK"),  # 雀巢香港 Nestlé HK
    # Japanese banks (non-GSIB)
    "549300KZ8RU11X0L9455": ("Bank_Other", "JP"),   # 北國銀行
    "549300WDPFPR0TE6OX32": ("Bank_Other", "JP"),   # 伊予銀行
    "549300I9WRBRFYSQB633": ("Bank_Other", "JP"),   # 第四北越銀行
    "549300X8PMHXCLWNCB66": ("Bank_Other", "JP"),   # 福岡銀行
    "5493005DJ3JFDBOF7R79": ("Bank_Other", "JP"),   # 横浜銀行
    "54930051TFGW2KIXPU60": ("Bank_Other", "JP"),   # 広島銀行
    "5493007VSMFZCPV1NB83": ("Bank_Other", "JP"),   # 農林中央金庫 Norinchukin
    "M2M9DTFX7VM34QT15B77": ("Bank_Other", "JP"),   # 中国銀行(JP) Chugoku Bank
    "X0XUGKC9FD2CYUQNC010": ("Bank_Other", "JP"),   # あおぞら銀行 Aozora
    "FE70I3MHDCWOZWK19W48": ("Bank_Other", "JP"),   # 八十二長野銀行
    "353800MNO5C8V2SHGA81": ("Bank_Other", "JP"),   # しずおかFG
    # Japanese sovereign/policy
    "5493001HGBABMWFZUI25": ("Sovereign_Gov", "JP"),  # 日本政策投資銀行 DBJ
    # Taiwanese banks
    "549300GCRU5QIM9WHM73": ("Bank_Other", "TW"),   # 兆豐國際商業銀行
    "549300X6CNQE512OPC90": ("Bank_Other", "TW"),   # 玉山金融控股
    "549300ZFPYDS135LU078": ("Bank_Other", "TW"),   # 台新國際商業銀行
    "5493006DVOBII1E8FK30": ("Bank_Other", "TW"),   # 國泰世華商業銀行
    "549300MGVLXK8G4X5Y29": ("Bank_Other", "TW"),   # 遠東國際商業銀行
    "549300IWDYIFW6JXM387": ("Bank_Other", "TW"),   # 中國信託金融控股
    "549300MTLEDCCBA8DW32": ("Bank_Other", "TW"),   # 永豐商業銀行
    "549300QBHSCPTZ7YV010": ("Bank_Other", "TW"),   # 臺灣銀行
    "549300RSNEVPCE8HET83": ("Bank_Other", "TW"),   # 臺灣土地銀行
    "529900BC1U046Q2GUZ64": ("Bank_Other", "TW"),   # 第一金融控股
    "549300G7Y2TS2XNIB476": ("Bank_Other", "TW"),   # 富邦金融控股
    "5493004LOSHK43HOYT35": ("Bank_Other", "TW"),   # 凱基商業銀行
    # Taiwanese insurance
    "2549000SMBY8FELB3491": ("InsurancePension", "TW"),  # 全球人壽保險
    "254900DUWXV1O3KM4P58": ("InsurancePension", "TW"),  # 凱基人壽保險
    "254900MGZPWGJDGJRO25": ("InsurancePension", "TW"),  # 三商美邦人壽保險
    "549300O7HK85BJZ81863": ("InsurancePension", "TW"),  # 南山人壽保險
    "549300UYPBBM6KXH0621": ("InsurancePension", "TW"),  # 新光人壽保險
    "5299009XR1QLFAMQ3X77": ("InsurancePension", "TW"),  # 國泰金融控股
    # Taiwanese corporate
    "549300KB6NK5SBD14S87": ("Corporate_Industrial", "TW"),  # 台積電 TSMC
    # Korean banks
    "549300ML2LNRZUCS7149": ("Bank_Other", "KR"),   # 한국산업은행 KDB
    "988400EB8A6G49E5KO54": ("Bank_Other", "KR"),   # 신한금융지주
    "549300VUVMRL6RE7R376": ("Bank_Other", "KR"),   # 우리은행
    "529900TKE4MXG3Q6GW86": ("Bank_Other", "KR"),   # KB금융지주
    "6RPK2YDJN6L35AS0M510": ("Bank_Other", "KR"),   # 하나은행
    # Korean insurance/pension
    "QHF0YTOE8OP1LN1NBT86": ("InsurancePension", "KR"),  # 국민연금공단 NPS
    # Korean sovereign
    "3R3ONDQY8DVH8ZQMP532": ("Sovereign_Gov", "KR"),  # 한국투자공사 KIC
    "988400ZTQ08W926ONT36": ("Sovereign_Gov", "KR"),  # 한국석유공사 KNOC
    # Korean corporate
    "988400C2UFBF4B660C58": ("Corporate_Industrial", "KR"),  # 대한항공 Korean Air
    "988400KOE4LX969V8V02": ("Corporate_Industrial", "KR"),  # HD현대오일뱅크
    "988400SQWZ34LADYL505": ("Corporate_Industrial", "KR"),  # LS Group
    # Arabic-script entities
    "213800JDGK6R55U59G76": ("Corporate_Industrial", "SA"),  # شركة ارامكو = Aramco Trading
    "213800NCSKH968YFDB88": ("Bank_Other", "BH"),             # Arab Banking Corporation
    "5493008JZL5CRK3VS565": ("Sovereign_Gov", "QA"),          # Qatar Investment Authority
    "254900LMNZ7EZCGH0D78": ("Corporate_Industrial", "OM"),   # Petroleum Development Oman
    "5493001JH4LYPQTBQP79": ("Bank_Other", "JO"),             # Arab Bank
    "54930029BCN8HF3B1286": ("Bank_Other", "AE"),             # Emirates NBD
    "5493006VS13CBNYBI229": ("Corporate_Industrial", "AE"),   # Shell Int'l Trading ME
    "549300NB7FE83IH6BW96": ("Bank_Other", "KW"),             # National Bank of Kuwait
    # Other known entities with non-standard names
    "254900IYR3SR0M2CJ686": ("Other_Financial", "HK"),  # 香港都會大學 HKMU (university)
}

# ---------------------------------------------------------------------------
# G-SIB LEI → jurisdiction (for is_gsib + gsib_jurisdiction flags)
# ---------------------------------------------------------------------------
GSIB_LEI_JURISDICTION = {
    k: v[1] for k, v in LEI_CATEGORY_MAP.items() if v[0] in ("GSIB_nonUS", "GSIB_US")
}

# ---------------------------------------------------------------------------
# Name-pattern lists
# ---------------------------------------------------------------------------

GSIB_US_PATTERNS = [
    r"JPMORGAN", r"JP MORGAN",
    r"BANK OF AMERICA",
    r"CITIGROUP", r"CITIBANK", r"CITI\b",
    r"WELLS FARGO",
    r"GOLDMAN SACHS(?! ASSET)",
    r"MORGAN STANLEY(?! INVESTMENT)(?! SMITH)",
    r"BANK OF NEW YORK MELLON", r"BNY MELLON",
    r"STATE STREET(?! GLOBAL ADVISORS)(?! REALTY)",
]

GSIB_NONUS_PATTERNS = [
    r"BNP PARIBAS(?! ASSET MANAGEMENT)(?! AM\b)(?! INVEST)",
    r"CREDIT AGRICOLE(?! ASSURANCES)(?! ASSET)",
    r"SOCIETE GENERALE(?! GESTION)(?! ASSET)(?! AM\b)",
    r"DEUTSCHE BANK(?! ASSET)(?! INVEST)(?! REALTY)",
    r"BARCLAYS(?! ASSET)(?! INVEST)(?! WEALTH)",
    r"HSBC(?! TRINKAUS)(?! ASSET)(?! INVEST)(?! GLOBAL ASSET)",
    r"STANDARD CHARTERED(?! INVEST)",
    r"ING GROEP", r"ING BANK",
    r"UNICREDIT(?! INVEST)(?! ASSET)(?! FUND)",
    r"INTESA SANPAOLO(?! ASSET)(?! VITA)",
    r"SANTANDER(?! ASSET MANAGEMENT)(?! INVEST)(?! AM\b)",
    r"BBVA",
    r"CREDIT SUISSE",
    r"UBS(?! ASSET)(?! REAL ESTATE)(?! FUND)(?! ETF)(?! FUND MANAGEMENT)",
    r"RABOBANK",
    r"NORDEA",
    r"ABN AMRO",
    r"COMMERZBANK",
    r"MITSUBISHI UFJ", r"MUFG",
    r"SUMITOMO MITSUI(?! ASSET)",
    r"MIZUHO(?! SECURITIES)(?! RESEARCH)",
    r"NOMURA HOLDINGS",
    r"ROYAL BANK OF CANADA", r"RBC\b",
    r"TORONTO.DOMINION", r"\bTD BANK",
    r"BPCE\b",
    r"NATWEST GROUP",
    r"LLOYDS BANKING GROUP",
]

# Patterns that indicate an AM/wealth subsidiary — exclude from GSIB rule
GSIB_AM_EXCLUSION_PATTERNS = [
    r"ASSET MANAGEMENT",
    r"ASSET MGMT",
    r"\bAM\b",
    r"INVEST(MENT|MENTS|ISSEMENTS)?\b",
    r"GESTION",
    r"FONDS",
    r"\bFUND\b",
    r"CAPITAL\b(?! ONE)",
    r"TRINKAUS",
    r"GLOBAL ADVISORS",
    r"WEALTH",
    r"FUND MANAGEMENT",
]

AM_GLOBAL_PATTERNS = [
    r"BLACKROCK", r"BLACK ROCK",
    r"VANGUARD",
    r"FIDELITY(?! LIFE| NATIONAL)", r"FMR LLC", r"\bFMR\b",
    r"AMUNDI",
    r"FRANKLIN TEMPLETON", r"FRANKLIN RESOURCES",
    r"WELLINGTON MANAGEMENT", r"WELLINGTON LUXEMBOURG",
    r"INVESCO",
    r"T\.? ROWE PRICE",
    r"PIMCO", r"PACIFIC INVESTMENT MANAGEMENT",
    r"ALLIANZ GLOBAL INVESTORS", r"ALLIANZ INVEST",
    r"DWS\b",
    r"SCHRODERS", r"SCHRODER",
    r"ABRDN", r"ABERDEEN",
    r"NATIXIS INVESTMENT", r"NATIXIS ASSET",
    r"NUVEEN",
    r"PRINCIPAL FINANCIAL(?! INSURANCE)", r"PRINCIPAL ASSET",
    r"NORTHERN TRUST ASSET",
    r"DIMENSIONAL FUND",
    r"CAPITAL GROUP",
    r"DODGE & COX",
    r"LEGG MASON",
    r"NEUBERGER BERMAN",
    r"LAZARD ASSET",
    r"COLUMBIA THREADNEEDLE",
    r"M&G INVESTMENTS", r"M&G INVESTMENT MANAGEMENT", r"M&G PLC",
    r"CANDRIAM",
    r"BNPP AM", r"BNP PARIBAS ASSET",
    r"SOCIETE GENERALE GESTION",
    r"GOLDMAN SACHS ASSET",
    r"MORGAN STANLEY INVESTMENT",
    r"JP ?MORGAN ASSET",
    r"STATE STREET GLOBAL ADVISORS",
    r"HSBC GLOBAL ASSET", r"HSBC ASSET", r"HSBC TRINKAUS",
    r"UNICREDIT INVEST", r"UNICREDIT ASSET",
    r"SANTANDER ASSET MANAGEMENT",
    r"UBS ASSET", r"UBS FUND MANAGEMENT",
    r"PICTET ASSET",
    r"GAM\b",
    r"DEKA\b",
    r"UNION INVESTMENT",
    r"LYXOR",
    r"OSSIAM",
    r"AXA INVESTMENT", r"AXA IM\b",
    r"CARMIGNAC",
    r"ODDO BHF ASSET",
    r"GROUPAMA ASSET",
    r"TIKEHAU",
    r"ROTHSCHILD ASSET", r"EDMOND DE ROTHSCHILD",
    r"NINETY ONE",
    r"FIRST SENTIER",
    r"APG ASSET",
    r"ROBECO",
    r"NN INVESTMENT", r"NN IP\b",
    r"BAILLIE GIFFORD",
    r"JANUS HENDERSON",
    r"JUPITER FUND", r"JUPITER ASSET",
    r"LIONTRUST",
    r"POLAR CAPITAL",
    r"QUILTER",
    r"RATHBONE",
    r"MAN GROUP",
    r"WINTON(?! GROUP)",
    r"AQR CAPITAL",
    r"BRIDGEWATER",
    r"ASHMORE INVESTMENT", r"ASHMORE ASSET", r"ASHMORE GROUP",
    r"HARTFORD FUNDS",
    r"JOHN HANCOCK INVESTMENT",
    r"TRANSAMERICA ASSET",
    r"GRANTHAM.*MAYO.*OTTERLOO", r"\bGMO\b",
    r"SEI INVESTMENTS",
    r"FUNDSIGHT",
    r"FUNDROCK",
    r"CARNE GLOBAL FUND",
    r"WAYSTONE",
    r"COLCHESTER GLOBAL INVESTORS",
    r"FIDEURAM ASSET",
    r"UNIVERSAL.INVESTMENT.GESELLSCHAFT", r"UNIVERSAL INVESTMENT",
    r"RUSSELL INVESTMENTS",
    r"WILLIAM BLAIR",
    r"ALLIANCE BERNSTEIN", r"ALLIANCEBERNSTEIN",
    r"EATON VANCE",
    r"PUTNAM INVEST",
    r"MFS INVESTMENT",
    r"COLUMBIA MANAGEMENT",
    r"AMERICAN CENTURY",
    r"PIONEER INVEST",
    r"PARTNERS GROUP \(LUXEMBOURG\)",
    r"PARTNERS GROUP \(UK\)",
    r"PARTNERS GROUP \(US\)",
    r"PARTNERS GROUP \(CAYMAN\)",
    r"PARTNERS GROUP AG",
    r"PARTNERS GROUP HOLDING",
    r"JACKSON NATIONAL ASSET",
    r"FIL INVESTMENT", r"FIL LIMITED",  # Fidelity International
    r"BANTLEON",
    r"FONDACO",
    r"ALTER DOMUS",
    r"EQUITABLE INVESTMENT",
    r"LINCOLN FINANCIAL INVEST",
    r"JOHN HANCOCK VARIABLE",
    r"GUIDESTONE FINANCIAL",
    r"WESTERN ASSET MANAGEMENT",
    r"BRANDYWINE GLOBAL",
    r"ACADIAN ASSET",
    r"EPOCH INVEST",
    r"HARDING LOEVNER",
    r"PARAMETRIC PORTFOLIO",
    r"AEW CAPITAL",
    r"SOMPO ASSET",
    r"NIPPON LIFE GLOBAL", r"NIPPON LIFE INVEST",
    r"MEIJI YASUDA ASSET",
    r"SUMITOMO MITSUI ASSET",
    r"TOKIO MARINE ASSET",
    r"NISSAY ASSET",
    r"AMERIPRISE FINANCIAL",
    r"MASTERINVEST",
    r"BAYERNINVEST",
    r"NOMURA ASSET MANAGEMENT",
    r"PACIFIC LIFE FUND ADVISORS",
    r"CA INDOSUEZ FUND",
    r"ARROWSTREET CAPITAL",
    r"CPR ASSET MANAGEMENT",
    r"AEGON ASSET",
    r"CALVERT RESEARCH",
    r"J\.P\. MORGAN INTERNATIONAL FINANCE",
    r"J\.P\. MORGAN INVEST",
    r"GLOBAL AGGREGATE",  # bond fund
]

INSURANCE_PATTERNS = [
    r"\bAXA\b(?! INVESTMENT)(?! IM\b)",
    r"AXA SA\b", r"AXA GROUP",
    r"ALLIANZ(?! GLOBAL INVESTORS)(?! INVEST)",
    r"GENERALI",
    r"ZURICH INSURANCE", r"ZURICH GROUP",
    r"MUNICH RE", r"MUENCHENER RUECK",
    r"SWISS RE",
    r"HANNOVER RE",
    r"SCOR\b",
    r"AVIVA",
    r"LEGAL & GENERAL",
    r"PRUDENTIAL(?! FINANCIAL ASSET)",
    r"METLIFE",
    r"AMERICAN INTERNATIONAL GROUP",
    r"AIG\b",
    r"MANULIFE",
    r"SUNLIFE", r"SUN LIFE",
    r"GREAT-WEST LIFECO",
    r"INTACT FINANCIAL",
    r"PENSION",
    r"CAISSE DE DEPOT", r"CDPQ",
    r"APG\b(?! ASSET)",
    r"CALPERS", r"CALSTRS",
    r"ABP\b",
    r"PGGM\b",
    r"TIAA\b",
    r"USAA\b",
    r"NATIONWIDE MUTUAL",
    r"ERIE INDEMNITY",
    r"MARKEL",
    r"AXIS CAPITAL",
    r"REINSURANCE",
    r"ASSURANCES",
    r"VERSICHERUNG",
    r"PREVIDENZA",
    r"FONDI PENSIONE",
    r"POSTE VITA",
    r"CNP ASSURANCES",
    r"SOGECAP",
    r"CARDIF(?! ASSET)",
    r"TALANX",
    r"BALOISE",
    r"HELVETIA",
    r"MAPFRE",
    r"UNIPOL", r"UNIPOLSAI",
    r"GROUPAMA(?! ASSET)",
    r"CREDIT AGRICOLE ASSURANCES",
    r"NATIXIS ASSURANCES",
    r"AIA\b", r"AIA GROUP",
    r"AEGON\b(?! ASSET)",
    r"VARIABLE ANNUITY LIFE",
    r"FWD GROUP",
    r"MANULIFE",
    r"JACKSON NATIONAL(?! ASSET)",
    r"PACIFIC LIFE(?! FUND)",
    r"EQUITABLE LIFE",
    r"GLOBE LIFE",
    r"LINCOLN NATIONAL",
    r"PROTECTIVE LIFE",
    r"TRANSAMERICA(?! ASSET)",
    r"UNUM GROUP",
    r"REINSURANCE GROUP",
    r"RGA\b",
    r"SAMPO GROUP",
    r"NN GROUP",
    r"ACHMEA",
]

BANK_OTHER_PATTERNS = [
    r"BANK\b", r"BANQUE\b", r"BANCA\b", r"BANCO\b",
    r"BANKEN\b", r"BANKHAUS\b",
    r"SAVINGS BANK", r"CREDIT UNION",
    r"LANDESBANK", r"SPARKASSE", r"VOLKSBANK", r"RAIFFEISENBANK",
    r"CAISSE D.EPARGNE", r"CREDIT MUTUEL",
    r"CAJA\b", r"CAISSE\b",
    r"COOPERATIVE BANK", r"BUILDING SOCIETY",
    r"FINANCIAL HOLDING",
    r"FINANCIAL GROUP(?! INC)",
    r"FINANCIAL CORP", r"FINANCIAL SERVICES GROUP",
    r"BANCORP\b", r"BANKCORP\b", r"BANC\b",
    r"NOMURA HOLDINGS",
    r"DAIWA SECURITIES",
    r"JEFFERIES",
    r"MACQUARIE(?! INVESTMENT)(?! ASSET)",
    r"CANTOR FITZGERALD",
    r"RAYMOND JAMES",
    r"STIFEL\b",
    r"PIPER SANDLER",
    r"SECURITIES(?! ZIMBABWE)",
    r"BROKERAGE", r"CLEARING",
    r"DEPOSITORY", r"CUSTODY",
    r"TRUST COMPANY",
    r"FEDERAL RESERVE", r"CENTRAL BANK",
    r"JULIUS B.R GRUPPE", r"JULIUS BAER GRUPPE",
    r"B\. METZLER",
    r"OVERSEA.CHINESE BANKING", r"OCBC\b",
    r"DBS GROUP", r"DBS BANK",
    r"UNITED OVERSEAS BANK", r"\bUOB\b",
    r"HANG SENG BANK",
    r"BANK OF EAST ASIA",
    r"MALAYAN BANKING", r"MAYBANK",
    r"CIMB GROUP",
    r"PUBLIC BANK BERHAD",
    r"SIAM COMMERCIAL BANK", r"KASIKORNBANK", r"BANGKOK BANK",
    r"AXIS BANK", r"HDFC BANK", r"ICICI BANK", r"KOTAK MAHINDRA",
    r"QATAR NATIONAL BANK", r"\bQNB\b",
    r"EMIRATES NBD", r"FIRST ABU DHABI",
    r"NATIONAL BANK OF KUWAIT",
    r"J\. SAFRA SARASIN",
    r"LGT GRUPPE",
    r"ARAB BANKING CORPORATION",
    r"ARAB INTERNATIONAL BANK",
    r"AUSTRALIA AND NEW ZEALAND BANKING", r"\bANZ\b",
    r"NATWEST GROUP",
    r"LLOYDS BANKING",
    r"WESTPAC", r"COMMONWEALTH BANK",
    r"NATIONAL AUSTRALIA BANK",
    r"RESONA HOLDINGS",
]

SOVEREIGN_PATTERNS = [
    r"GOVERNMENT OF\b", r"MINISTRY OF\b",
    r"REPUBLIC OF\b", r"KINGDOM OF\b",
    r"FEDERAL REPUBLIC", r"SOVEREIGN WEALTH", r"SOVEREIGN FUND",
    r"TREASURY\b",
    r"NATIONAL BANK OF\b", r"RESERVE BANK OF\b",
    r"BANQUE DE FRANCE", r"BUNDESBANK",
    r"BANCA D.ITALIA", r"BANCO DE ESPANA",
    r"NORGES BANK", r"RIKSBANK", r"DANMARKS NATIONALBANK",
    r"PEOPLES BANK OF CHINA", r"PBOC",
    r"BANK OF JAPAN", r"BANK OF ENGLAND",
    r"EUROPEAN CENTRAL BANK", r"\bECB\b",
    r"WORLD BANK", r"IMF\b", r"INTERNATIONAL MONETARY FUND",
    r"BIS\b", r"BANK FOR INTERNATIONAL SETTLEMENTS",
    r"EUROPEAN STABILITY MECHANISM",
    r"CAISSE DES DEPOTS",
    r"KFW\b",
    r"EIB\b", r"EUROPEAN INVESTMENT BANK",
    r"DEVELOPMENT BANK",
    r"EXPORT.IMPORT BANK",
    r"PUBLIC SECTOR",
    r"TEMASEK",
    r"GIC\b",
    r"MUBADALA", r"ADIA\b",
    r"SAUDI ARAMCO",
    r"NORGES BANK INVESTMENT",
    r"KHAZANAH",
]

CORPORATE_PATTERNS = [
    r"PHARMACEUTICAL", r"PHARMA\b",
    r"TECHNOLOGY(?! FINANCE)", r"SEMICONDUCTOR",
    r"AUTOMOTIVE", r"AUTOMOBILE",
    r"ENERGY\b(?! FINANCE)",
    r"UTILITIES", r"TELECOM",
    r"CONSUMER GOODS", r"MANUFACTURING",
    r"INDUSTRIALS", r"HEALTHCARE", r"MEDICAL",
    r"RETAIL\b", r"AEROSPACE", r"DEFENSE",
    r"OIL\b", r"GAS\b", r"MINING\b",
    r"CHEMICALS", r"FOOD\b", r"BEVERAGE",
    r"MEDIA\b", r"ENTERTAINMENT",
    r"TRANSPORT", r"LOGISTICS",
    r"REAL ESTATE(?! FUND| INVEST| TRUST| REIT)",
    r"PROPERTY(?! FUND)",
    r"CONSTRUCTION(?! FINANCE)",
    r"INFRASTRUCTURE(?! FUND| INVEST)",
    r"UTILITY", r"POWER\b", r"NETWORKS\b",
    r"TELECOMS",
    r"APPLE INC", r"MICROSOFT", r"AMAZON\b",
    r"ALPHABET\b", r"GOOGLE\b",
    r"META PLATFORMS", r"TESLA\b", r"NVIDIA",
    r"TOYOTA(?! ASSET)", r"VOLKSWAGEN", r"SIEMENS",
    r"GENERAL ELECTRIC", r"\bGE\b CAPITAL",
    r"GENERAL MOTORS", r"FORD MOTOR",
    r"BOEING", r"AIRBUS",
    r"BAYERISCHE MOTOREN WERKE", r"\bBMW\b",
    r"SHELL\b", r"BP\b",
    r"EXXON", r"CHEVRON",
    r"TOTAL(ENERGIES)?\b",
    r"ENI\b", r"NESTL",
    r"UNILEVER", r"LVMH", r"DANONE",
    r"ROCHE\b", r"NOVARTIS",
    r"PFIZER", r"JOHNSON & JOHNSON",
    r"TRAFIGURA", r"GLENCORE", r"VITOL\b",
    r"MERCURIA", r"GUNVOR", r"COMMODITY",
    r"OLAM GROUP", r"WILMAR", r"BUNGE\b",
    r"ARCHER.DANIELS", r"CARGILL",
    r"MARSH & MCLENNAN",
    r"ENGIE\b",
    r"SINGAPORE AIRLINES",
    r"AKTIEBOLAGET VOLVO",
    r"SEATRIUM",
    r"COFCO",
    r"LOUIS DREYFUS",
    r"PETROCHINA",
    r"SINOPEC",
    r"CNOOC",
    r"KEPPEL\b",
    r"HINDALCO",
    r"TATA\b",
    r"RELIANCE INDUSTRIES",
    r"INFOSYS",
    r"WIPRO",
    r"MAPLETREE",
    r"PROCTER & GAMBLE",
    r"\bNIKE\b",
    r"ELECTRICITE DE FRANCE", r"\bEDF\b",
    r"VINCI\b",
    r"SCHNEIDER ELECTRIC",
    r"SAINT.GOBAIN",
    r"MICHELIN",
    r"RENAULT",
    r"PEUGEOT", r"STELLANTIS",
    r"L.OREAL",
    r"HERMES\b",
    r"PERNOD RICARD",
    r"CAPGEMINI",
    r"ATOS\b",
    r"THALES\b",
    r"SAFRAN\b",
    r"AIR FRANCE",
    r"ACCOR\b",
    r"CARREFOUR",
    r"PARKWAY PANTAI",
    r"IHH HEALTHCARE",
    r"BUMRUNGRAD",
]

HF_PATTERNS = [
    r"HEDGE FUND", r"ALTERNATIVE INVESTMENT",
    r"MULTI.STRATEGY", r"MACRO FUND",
    r"LONG.SHORT", r"GLOBAL MACRO",
    r"TWO SIGMA", r"D\.E\. SHAW", r"DE SHAW",
    r"POINT72",
    r"CITADEL(?! SECURITIES)",
    r"MILLENNIUM MANAGEMENT",
    r"TUDOR INVESTMENT",
    r"APPALOOSA", r"PAULSON",
    r"PERSHING SQUARE",
    r"ELLIOTT MANAGEMENT",
    r"GREENLIGHT CAPITAL",
    r"MARSHALL WACE",
    r"CAPULA INVESTMENT", r"CQS\b",
    r"WINTON GROUP",
    r"SYSTEMATICA", r"CHEYNE CAPITAL",
    r"BREVAN HOWARD", r"GLG PARTNERS",
    r"LANSDOWNE PARTNERS",
    r"ALGEBRIS", r"BLUECREST",
]

PE_PATTERNS = [
    r"PRIVATE EQUITY", r"BUYOUT FUND",
    r"VENTURE CAPITAL", r"\bVC\b",
    r"GROWTH CAPITAL", r"PRIVATE CREDIT",
    r"DIRECT LENDING", r"MEZZANINE",
    r"BLACKSTONE(?! REAL ESTATE FUND)",
    r"KKR\b", r"CARLYLE GROUP",
    r"APOLLO GLOBAL", r"WARBURG PINCUS",
    r"BAIN CAPITAL", r"TPG\b",
    r"ARES MANAGEMENT",
    r"BROOKFIELD ASSET", r"BROOKFIELD INFRA",
    r"INFRASTRUCTURE FUND", r"INFRA INVEST",
    r"EQT\b", r"CINVEN\b", r"CVC CAPITAL",
    r"PAI PARTNERS", r"EURAZEO",
    r"BRIDGEPOINT", r"PERMIRA",
    r"IK INVESTMENT", r"BC PARTNERS",
    r"INVESTCORP", r"ARDIAN\b",
    r"SILVERLAKE", r"VISTA EQUITY",
    r"VERITAS CAPITAL", r"THOMA BRAVO",
    r"FRANCISCO PARTNERS",
    r"INSIGHT PARTNERS",
    r"GENERAL ATLANTIC",
    r"SUMMIT PARTNERS",
    r"PARTNERS GROUP HOLDING AG",
    r"PARTNERS GROUP \(LUXEMBOURG\)",
    r"PARTNERS GROUP \(UK\)",
    r"PARTNERS GROUP \(US\)",
    r"PARTNERS GROUP \(USA\)",
    r"PARTNERS GROUP \(CAYMAN\)",
]

FX_DEALER_PATTERNS = [
    r"JPMORGAN", r"JP MORGAN",
    r"CITIGROUP", r"CITIBANK",
    r"DEUTSCHE BANK",
    r"BARCLAYS",
    r"UBS\b",
    r"HSBC\b",
    r"BNP PARIBAS(?! ASSET)",
    r"SOCIETE GENERALE(?! GESTION)",
    r"GOLDMAN SACHS(?! ASSET)",
    r"MORGAN STANLEY(?! INVESTMENT)",
    r"BANK OF AMERICA",
    r"MITSUBISHI UFJ", r"MUFG",
    r"STANDARD CHARTERED(?! INVEST)",
    r"NOMURA HOLDINGS",
    r"CREDIT SUISSE",
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def matches_any(name: str, patterns: list) -> bool:
    if not isinstance(name, str):
        return False
    for p in patterns:
        if re.search(p, name, re.IGNORECASE):
            return True
    return False


def is_gsib_am_exclusion(name: str) -> bool:
    return matches_any(name, GSIB_AM_EXCLUSION_PATTERNS)


# ---------------------------------------------------------------------------
# Pillar 1: UCI Category
# ---------------------------------------------------------------------------

def classify_uci(row) -> str:
    lei  = str(row.get("UCI_LEI", "") or "")
    name = str(row.get("uci_entity_name", "") or "")
    corr_lei  = str(row.get("corrected_parent_lei", "") or "")
    corr_name = str(row.get("corrected_parent_name", "") or "")

    eff_lei  = corr_lei  if corr_lei  not in ("", "nan", "NaN") else lei
    eff_name = corr_name if corr_name not in ("", "nan", "NaN") else name

    if not eff_lei or eff_lei in ("nan", "NaN", "LEI_INVALIDE"):
        return "UNCLASSIFIABLE"

    # 1. LEI-based (handles non-Latin names, known edge cases)
    if eff_lei in LEI_CATEGORY_MAP:
        return LEI_CATEGORY_MAP[eff_lei][0]

    # 2. PE / Infra (before AM — Partners Group etc.)
    if matches_any(eff_name, PE_PATTERNS):
        return "PE_Infra_Manager"

    # 3. Asset managers (before G-SIBs — AM subsidiaries of G-SIBs)
    if matches_any(eff_name, AM_GLOBAL_PATTERNS):
        return "AssetManager_Global"

    # 4. Hedge funds
    if matches_any(eff_name, HF_PATTERNS):
        return "HedgeFund_AltManager"

    # 5. US G-SIBs
    if matches_any(eff_name, GSIB_US_PATTERNS) and not is_gsib_am_exclusion(eff_name):
        return "GSIB_US"

    # 6. Non-US G-SIBs
    if matches_any(eff_name, GSIB_NONUS_PATTERNS) and not is_gsib_am_exclusion(eff_name):
        return "GSIB_nonUS"

    # 7. Insurance / Pension
    if matches_any(eff_name, INSURANCE_PATTERNS):
        return "InsurancePension"

    # 8. Other banks
    if matches_any(eff_name, BANK_OTHER_PATTERNS):
        return "Bank_Other"

    # 9. Sovereign / Gov
    if matches_any(eff_name, SOVEREIGN_PATTERNS):
        return "Sovereign_Gov"

    # 10. Corporate
    if matches_any(eff_name, CORPORATE_PATTERNS):
        return "Corporate_Industrial"

    return "Other_Financial"


# ---------------------------------------------------------------------------
# Pillar 2: G-SIB flags
# ---------------------------------------------------------------------------

def get_gsib_flags(row):
    lei  = str(row.get("UCI_LEI", "") or "")
    name = str(row.get("uci_entity_name", "") or "")
    corr_lei  = str(row.get("corrected_parent_lei", "") or "")
    corr_name = str(row.get("corrected_parent_name", "") or "")

    eff_lei  = corr_lei  if corr_lei  not in ("", "nan", "NaN") else lei
    eff_name = corr_name if corr_name not in ("", "nan", "NaN") else name

    is_gsib      = False
    jurisdiction = np.nan
    is_fx_dealer = False
    dual_role    = np.nan

    # LEI-based
    if eff_lei in GSIB_LEI_JURISDICTION:
        is_gsib     = True
        jurisdiction = GSIB_LEI_JURISDICTION[eff_lei]
    elif matches_any(eff_name, GSIB_US_PATTERNS) and not is_gsib_am_exclusion(eff_name):
        is_gsib      = True
        jurisdiction = "US"
    elif matches_any(eff_name, GSIB_NONUS_PATTERNS) and not is_gsib_am_exclusion(eff_name):
        is_gsib = True
        country = str(row.get("uci_entity_country", "") or
                      row.get("corrected_parent_country", "") or "")
        jurisdiction = country if country not in ("", "nan", "NaN") else "non-US"

    # FX dealer
    if matches_any(eff_name, FX_DEALER_PATTERNS) and not is_gsib_am_exclusion(eff_name):
        is_fx_dealer = True
    # Also flag via LEI if known G-SIB FX dealer
    if eff_lei in GSIB_LEI_JURISDICTION and eff_lei in {
        "353800V2V8PUY9TK3E06",  # MUFG
        "35380028MYWPB6AUO129",  # SMFG
        "54930053HGCFWVHYZX42",  # Bank of China
        "549300B3CEAHYG7K8164",  # Nomura
        "353800CI5L6DDAN5XZ33",  # Mizuho
    }:
        is_fx_dealer = True

    if is_gsib and is_fx_dealer:
        dual_role = "GSIB_and_FX_dealer"
    elif is_gsib:
        dual_role = "GSIB_only"
    elif is_fx_dealer:
        dual_role = "FX_dealer_only"

    return is_gsib, jurisdiction, is_fx_dealer, dual_role


# ---------------------------------------------------------------------------
# Pillar 3: Intragroup potential
# ---------------------------------------------------------------------------

def compute_intragroup(df: pd.DataFrame):
    def effective_parent(row):
        corr = str(row.get("corrected_parent_lei", "") or "")
        if corr not in ("", "nan", "NaN", "LEI_INVALIDE"):
            return corr
        uci_ult = str(row.get("uci_ultimate_parent_lei", "") or "")
        if uci_ult not in ("", "nan", "NaN"):
            return uci_ult
        uci = str(row.get("UCI_LEI", "") or "")
        return uci if uci not in ("", "nan", "NaN") else np.nan

    eff_parent = df.apply(effective_parent, axis=1)
    sibling_counts = eff_parent.value_counts()

    def intragroup(row, ep):
        if pd.isna(ep):
            return "no"
        n = sibling_counts.get(ep, 1)
        conf = str(row.get("UCI_Confidence", "") or "")
        if n >= 3 and conf == "high":
            return "confirmed"
        elif n >= 2:
            return "probable"
        return "uncertain"

    result = pd.Series([
        intragroup(df.iloc[i], eff_parent.iloc[i])
        for i in range(len(df))
    ], index=df.index)

    return eff_parent, result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Loading taxonomy_gleif_corrected.xlsx...")
    df = pd.read_excel(INPUT)
    print(f"  {len(df)} rows × {len(df.columns)} columns")

    print("Applying Pillar 1: UCI category...")
    df["uci_category"] = df.apply(classify_uci, axis=1)

    print("Applying Pillar 2: G-SIB flags...")
    flags = df.apply(get_gsib_flags, axis=1, result_type="expand")
    df["is_gsib"]           = flags[0]
    df["gsib_jurisdiction"] = flags[1]
    df["is_fx_dealer"]      = flags[2]
    df["gsib_dual_role"]    = flags[3]

    print("Applying Pillar 3: Intragroup potential...")
    eff_parent, intragroup = compute_intragroup(df)
    df["effective_parent_lei"] = eff_parent
    df["intragroup_potential"] = intragroup

    # Summary
    print("\n=== UCI Category Distribution ===")
    print(df["uci_category"].value_counts().to_string())
    print(f"\n=== G-SIBs: {df['is_gsib'].sum()} | FX Dealers: {df['is_fx_dealer'].sum()}")
    print("\n=== Intragroup Potential ===")
    print(df["intragroup_potential"].value_counts().to_string())

    # Other_Financial deep-dive
    other = df[df["uci_category"] == "Other_Financial"]
    print(f"\n=== Other_Financial: {len(other)} rows, {other['UCI_LEI'].nunique()} unique UCIs ===")
    top30 = other["uci_entity_name"].value_counts().head(30)
    print(top30.to_string())

    print(f"\nSaving to {OUTPUT}...")
    df.to_excel(OUTPUT, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
