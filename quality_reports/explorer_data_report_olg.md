# Data Feasibility Report: Global Imbalances OLG Paper
**Date:** 2026-05-19
**Agent:** explorer
**Paper:** Net Foreign Assets, Demographics, and the Structural Determinants of External Imbalances: A Two-Country OLG Approach

---

## Summary Assessment

This project is **empirically feasible** at the panel level (N≈40–60, T≈30–40 years), but faces three binding constraints that require explicit design decisions before data assembly begins:

1. **Utilization-adjusted TFP** — No single public database delivers long-run utilization-adjusted country-specific TFP for a 40–60 country panel at annual frequency. The researcher must either (a) use PWT output-side TFP as a baseline and apply a utilization correction from national capacity utilization data, or (b) restrict the advanced-economy sample for richer TFP measures and use simpler residuals for EMs. This is the single hardest constraint.

2. **UN population projection vintages** — Constructing the *anticipated* old-age dependency ratio requires historical vintage versions of UN projections (i.e., what demographers forecast *at time t*, not retroactively applied current best estimates). The UN's digital archive holds 1980–2024 vintages but they are not aggregated in a single machine-readable panel; the researcher must extract and stack multiple vintage files manually or use the HMD/Wittgenstein Centre as a partial substitute.

3. **NIIP valuation decomposition** — Decomposing NIIP changes into current account, valuation effects, capital transfers, and errors & omissions at panel frequency is achievable via Lane & Milesi-Ferretti (EWN), but the decomposition is only clean from 2001 for the CPIS-era data; pre-2001 valuation residuals carry more measurement noise.

**Bottom line:** The core panel (NIIP, demographics, income, public debt) can be assembled in 4–8 weeks using fully public data. TFP and projection vintages require dedicated effort (2–4 additional weeks each) and may constrain the country scope.

---

## A. External Balance Variables

### A1. Lane & Milesi-Ferretti — External Wealth of Nations (EWN) Database

**Provider:** IMF Research / Peterson Institute for International Economics (updated host)
**Coverage:** 1970–2023 (latest update), ~200 countries; annual
**Access:** Public, free download (IMF Data or PIIE website)
**Key variables available:**
- Net International Investment Position (NIIP) as % of GDP
- Gross foreign assets and liabilities by category (FDI, portfolio equity, portfolio debt, other investment, reserves)
- Current account balance (linked from WEO)
- Valuation effects (VAL_it) = ΔNIIP − CA, constructed by LMF
- Capital transfers (limited; mainly advanced economies post-2000)

**Known issues:**
- Pre-1990 NIIP estimates for emerging markets are rough and rely on cumulated current accounts; large revisions between 2007 and 2018 versions
- Valuation decomposition is residual-based; absorbs statistical discrepancies and errors & omissions before 2001
- No explicit capital transfers series for many EMs; must be separately sourced from BOP data (IMF BOP)
- Latest public version (October 2022) may be one or two years stale relative to WEO; cross-check with IMF IFS

**Feasibility grade: A**
**Key papers:** Lane & Milesi-Ferretti (2001, 2007, 2018); Gourinchas & Rey (2007); Alfaro, Kalemli-Ozcan & Volosovych (2008); IMF EBA methodology

---

### A2. IMF Balance of Payments / International Financial Statistics (IFS)

**Provider:** IMF Statistics Department
**Coverage:** 1980–present; ~190 countries; annual and quarterly
**Access:** Public via IMF Data platform (imf.org/en/Data); bulk download available
**Key variables available:**
- Current account balance and subcomponents (goods, services, primary income, secondary income)
- Capital account (capital transfers, KA_it)
- Errors and omissions (EOM_it) — BPM6 basis from ~2005, BPM5 before
- Financial account flows (FDI, portfolio, other investment, reserves)

**Known issues:**
- BPM5→BPM6 break (2005–2012 transition window, country-specific); splicing requires care
- Errors and omissions are volatile and can be large for EMs with weak reporting; sum-to-zero assumption at global level is routinely violated
- Capital transfers series thin before 1995 for most countries; frequently mixed with current transfers

**Feasibility grade: A** for CA and EOM; **B** for capital transfers pre-2000
**Key papers:** Chinn & Prasad (2003); Gruber & Kamin (2007)

---

### A3. World Bank World Development Indicators (WDI)

**Provider:** World Bank
**Coverage:** 1960–2024; ~217 countries; annual
**Access:** Public, API-accessible (wbdata, WDI R package)
**Key variables available:**
- Current account balance (% of GDP)
- Net ODA and transfers
- Cross-check for GDP denominators (consistent with WEO)

**Known issues:**
- WDI current account often lags by 1–2 years for small EMs; use WEO as primary source
- Redundant with WEO for most macro aggregates; most useful for cross-checking and filling gaps

**Feasibility grade: B** (secondary/backup)

---

## B. Demographic Variables

### B1. UN World Population Prospects (WPP) — Current and Historical Vintages

**Provider:** United Nations Population Division
**Coverage (current):** 2024 revision covers 237 countries/territories; projections to 2100; historical estimates 1950–2023
**Coverage (vintages):** Digital archives hold editions from 1980, 1982, 1984, 1986, 1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2015, 2017, 2019, 2022, 2024
**Access:** Public; current revision fully downloadable via UNPD website and API; older vintages available as PDFs (pre-2000) and XLS/CSV (2000+) at population.un.org/wpp/archive/

**Key variables available:**
- Population by 5-year age group and sex (ages 0–4, 5–9, ..., 80+)
- Old-age dependency ratio (65+ / 15–64) — directly provided in some vintages; computable from age-group data in all
- Projected old-age dependency ratio at 5-year intervals: E_t[φ_{i,t+T}] — the key variable for the anticipated demographics channel
- Median age, total fertility rate, life expectancy at birth and at 65 (e_65)
- Working-age population (15–64) and growth rates

**Critical challenge — vintage reconstruction:**
To properly proxy E_t[φ_{i,t+T}], the researcher needs, for each observation year t, the projection *published at time t* for period t+T (e.g., T=20 years). This requires:
1. Downloading every WPP edition (every 2 years since 1980; every 4–5 years before)
2. Extracting the relevant projection horizon column from each vintage
3. Stacking into a panel indexed by (country, base_year, projection_horizon)

The 1980, 1984, 1990, 1992 vintages are PDF-only; OCR or manual extraction will be needed for country-level data. The 1994, 1996, 1998, 2000 vintages are Excel/Lotus but poorly formatted. Starting in 2002 and especially 2010+, the files become cleanly machine-readable CSVs.

**Practical recommendation:** Use WPP vintages 2000–2023 (clean machine-readable; 24 years of coverage) as primary instrument. For 1980–1999, consider using the Wittgenstein Centre (B2 below) or accept that anticipated demographics are estimated from current-vintage WPP retroactively applied — with a note on the limitation.

**Known issues:**
- Projection errors are large at long horizons for high-fertility countries (Sub-Saharan Africa)
- Country coverage varies pre-1990; some small states absent from early vintages
- Life expectancy at 65 is available in the core series but less prominently featured; verify with HMD for advanced economies

**Feasibility grade: A** for current demographics; **B** for vintage projections (significant manual effort)
**Key papers:** IMF EBA methodology uses WPP current vintage; Ferrero (2010); Gagnon et al. (2021)

---

### B2. Human Mortality Database (HMD)

**Provider:** UC Berkeley and Max Planck Institute for Demographic Research
**Coverage:** 1840s–2021 (country-specific start dates); 41 countries (mostly OECD + Eastern Europe)
**Access:** Public, free registration required; bulk download available
**Key variables available:**
- Period life tables by single year of age and sex
- Life expectancy at exact ages: e_0, e_65, e_80
- Mortality rates (q_x, m_x) and survival probabilities (l_x) — direct OLG calibration inputs
- Population exposure and death counts by year and age

**Known issues:**
- Country scope limited to ~41 high-income and upper-middle-income countries; no Sub-Saharan Africa, Southeast Asia except Japan
- Annual updates lag; some countries (e.g., Greece, Portugal) have gaps in latest years
- Not a substitute for UN WPP projections; provides realized mortality, not projected

**Feasibility grade: A** for advanced economies e_65 series; **C** for emerging markets (coverage gap)
**Complement to WPP for advanced economy sample**

---

### B3. Wittgenstein Centre Human Capital Data Explorer

**Provider:** Vienna Institute of Demography / IIASA / WIC
**Coverage:** 1950–2100 projections; ~200 countries; multiple SSP scenarios
**Access:** Public, downloadable (wcde.org)
**Key variables available:**
- Population by age, sex, and education level
- Old-age dependency ratios under different scenarios
- Historical population reconstructions consistent with WPP
- SSP1–SSP5 projections (useful as robustness check on projection specification)

**Known issues:**
- Education disaggregation useful for some channels but adds complexity
- Projections are scenario-based (SSP1–5); researcher must choose or average across scenarios
- Not a direct substitute for WPP vintage-specific projections

**Feasibility grade: B** (valuable supplement, especially for projection scenario robustness)

---

## C. Income & Productivity (TFP — Most Difficult)

### C1. Penn World Tables (PWT 10.x)

**Provider:** Groningen Growth and Development Centre (GGDC), University of Groningen
**Coverage:** PWT 10.01 covers 183 countries, 1950–2019; updated irregularly (PWT 10.01 released 2021; check for 11.x)
**Access:** Public, free download (rug.nl/ggdc/productivity/pwt/)
**Key variables available:**
- `ctfp`: TFP level at current PPPs relative to USA = 1 (output-side TFP)
- `cwtfp`: Welfare-relevant TFP
- `rtfp`: TFP relative to the world frontier
- `rgdpna`: Real GDP at constant national prices (for growth accounting)
- `hc`: Human capital index (Barro-Lee based)
- `rnna`: Capital stock
- Real GDP per capita multiple variants: `rgdpe`, `rgdpo`, `rgdpna`
- Factor shares (`labsh`), depreciation rates (`delta`)

**Key limitation — utilization adjustment:**
PWT TFP is NOT utilization-adjusted. It reflects observed factor utilization including the business cycle component. The country-specific structural component ã_it in the paper's model requires removing: (a) global TFP trend, (b) cyclical utilization variation. PWT does not provide utilization-adjusted measures.

**Practical workaround options:**
1. Use HP-filtered TFP or 5-year moving average to remove cyclical component (crude but common)
2. Use capacity utilization from national accounts (Fed, Eurostat, OECD) to adjust PWT TFP for advanced economies; use manufacturing capacity utilization as proxy for EMs
3. Interact with a global TFP factor (first PC of PWT `ctfp` panel) to isolate country-specific deviation ã_it = ctfp_it − global_factor_t
3. Use Fernald (2014) utilization adjustment factors for the US; apply parametric adjustment to other countries (strong assumption)

**Known issues:**
- Coverage gap: PWT 10.01 ends 2019; no 2020–2023 estimates
- TFP constructed as Solow residual; absorbs all measurement error in capital and labor
- Capital stock initial conditions matter greatly for TFP levels; noisy for EMs
- Comparability across income groups limited for structural TFP questions

**Feasibility grade: B** (best available for broad country coverage, but utilization issue requires explicit treatment)
**Key papers:** Feenstra, Inklaar & Timmer (2015); PWT underlies most CA determinant papers

---

### C2. EU-KLEMS (2023 Release)

**Provider:** The Conference Board / Groningen; European Commission funding
**Coverage:** EU-KLEMS 2023: 30 countries (EU28 + USA + Japan), 1980–2021; some series to 2022
**Access:** Public, free download (euklems.net)
**Key variables available:**
- Industry-level TFP growth with capital service flows (quality-adjusted)
- Labor composition (hours worked by skill, age, gender)
- Capital services by type (ICT, structures, machinery)
- Economy-wide TFP index (chained, 2010=100)
- Capital utilization rates available for some countries/sectors

**Key advantage:** Capital services approach (not capital stock) is conceptually more appropriate; some editions include capacity utilization adjustments for manufacturing

**Known issues:**
- Country scope limited to 30 OECD countries; no EMs → cannot be primary source for full panel
- Industry-level aggregation to economy-wide TFP requires care with sectoral weights
- Backward extrapolation before 1995 varies in quality
- Annual updates lag 2–3 years

**Feasibility grade: A** for OECD sub-sample of the panel; **D** for EMs (not covered)

---

### C3. World KLEMS

**Provider:** GGDC / World KLEMS consortium
**Coverage:** ~40 countries including major EMs (Brazil, China, India, Mexico, Russia, South Africa, Indonesia); 1980–2018 approximately; varies by country
**Access:** Public, free download (worldklems.net)
**Key variables available:**
- TFP growth (Törnqvist index) at economy level
- Some country contributors provide industry-level data
- Varies significantly by country in terms of methodology and reliability

**Known issues:**
- Country-specific data quality is highly heterogeneous: China and India TFP series are contested
- Temporal coverage highly uneven: some countries have 1980–2018, others only 1995–2015
- Not a unified harmonized dataset; assembled from national contributor submissions
- No utilization adjustment in most country files

**Feasibility grade: B** for EM supplement to EU-KLEMS; **C** for panel use due to heterogeneity

---

### C4. Bergeaud, Cette & Lecat (BCL) Long-Run Productivity Database

**Provider:** Banque de France
**Coverage:** 17 advanced economies (G7 + W. Europe + Australia/NZ/Canada), 1890–2019
**Access:** Public, downloadable (banque-france.fr/economie/relations-internationales-et-cooperation/bcl)
**Key variables available:**
- TFP growth (multifactor productivity) at economy level
- Labor productivity decomposition
- Long historical run: allows pre-1980 trends that could instrument current TFP levels

**Known issues:**
- 17 countries only — insufficient for the full paper panel
- No utilization adjustment
- Useful as historical instrument or robustness check for the advanced economy sub-sample

**Feasibility grade: B** for advanced economy historical robustness; **D** for main panel (scope too narrow)

---

### C5. IMF Article IV / WEO TFP Residuals

**Provider:** IMF Research
**Coverage:** ~150 countries; 1980–2023 via WEO; annual
**Access:** WEO TFP projections and historical data accessible via WEO online database; some Article IV staff reports have country-specific TFP estimates

**Key variables available:**
- WEO sometimes reports implicit TFP residuals in Article IV background papers
- IMF Investment and Capital Stock Dataset (ICSD) provides capital stock data that can feed TFP calculations

**Known issues:**
- WEO TFP data not systematically available in machine-readable panel format
- Methodology varies across country desks and time
- Would require manual extraction from Article IV reports for many countries

**Feasibility grade: C** (not a primary source; useful for individual country checks)

---

### TFP Strategy Summary

**Recommended approach:** Use PWT 10.x `ctfp` as the baseline for the full panel. For the advanced economy sub-sample (30 countries), augment with EU-KLEMS for capital service-based TFP. Apply a global factor (first principal component of `ctfp` across all countries in sample) to strip the global component, leaving ã_it as the residual. For utilization adjustment, either: (a) control for the output gap (from WEO) as a proxy for cyclical utilization variation, or (b) apply a direct utilization correction using manufacturing capacity utilization (OECD Stat for OECD countries; World Bank for EMs) as a scaling factor. Document this as a key measurement decision with robustness checks.

---

## D. Fiscal Variables

### D1. IMF World Economic Outlook (WEO) Database

**Provider:** IMF
**Coverage:** 1980–2030 (projections to 2030); ~190 countries; annual; updated April and October
**Access:** Public, free download (imf.org/en/Publications/WEO)
**Key variables available:**
- Gross government debt (% of GDP) — `GGXWDG_NGDP` — **primary source for d^g_it**
- General government structural balance (% of potential GDP) — `GGCB`
- Cyclically adjusted primary balance (% of potential GDP) — `GGCBP` — **primary source for pb^str_it**
- General government revenue, expenditure, primary balance (current and structural)
- Output gap (% of potential GDP) — for utilization correction of TFP
- Potential GDP and growth

**Known issues:**
- Structural balance estimates are IMF desk-specific and subject to large revisions; use with caution for empirical work spanning multiple WEO vintages
- Gross debt concept varies: some countries report consolidated general government, others include off-balance-sheet items differently
- Data before 1990 thinner for EMs; pre-2000 for many Sub-Saharan African countries
- WEO structural balance methodology was updated in 2014; creates break in the series

**Feasibility grade: A** for gross public debt; **B** for structural primary balance (revision risk)
**Key papers:** Chinn & Prasad (2003); IMF EBA explicitly uses WEO CAPB series

---

### D2. OECD Economic Outlook / OECD Fiscal Database

**Provider:** OECD
**Coverage:** OECD Economic Outlook: ~50 countries (OECD + key partners), 1970–2024; annual and semi-annual
**Access:** Public via OECD.Stat; some series require API key
**Key variables available:**
- General government gross financial liabilities (% of GDP) — `GGFLQ`
- Cyclically adjusted primary balance (% of potential GDP) — `CAPBQ`
- Government net financial liabilities
- Underlying primary balance (strips asset price effects)
- More carefully constructed structural balance than WEO for OECD countries

**Known issues:**
- Limited to OECD countries (~38); does not cover major EMs (Brazil, India, China, Indonesia)
- OECD methodology for structural balance changes over time

**Feasibility grade: A** for OECD sub-sample; **C** for full panel (coverage gap)
**Key papers:** OECD fiscal papers; IMF EBA EMs supplement uses WEO as fallback

---

### D3. Historical Public Debt Database (HPDD) / Global Debt Database (GDD)

**Provider:** IMF Fiscal Affairs Department
**Coverage:** GDD: ~190 countries, 1950–2022 (gross public debt); HPDD: ~180 countries, 1800+
**Access:** Public download (IMF website)
**Key variables available:**
- Gross general government debt (% of GDP) — long historical series
- Central government debt where general government unavailable
- Some domestic/external debt breakdown

**Known issues:**
- Historical series constructed from heterogeneous sources; pre-1990 for EMs often central government only
- Useful as backup/historical extension; WEO preferred for post-1980 paper sample

**Feasibility grade: B** (useful historical supplement and gap-filler)

---

## E. Global Interest Rate / r*

### E1. Holston, Laubach & Williams (HLW) Estimates

**Provider:** Federal Reserve Bank of New York (NY Fed)
**Coverage:** US: 1961–Q3 2024; Euro Area: 1972–Q3 2024; UK: 1985–Q3 2024; Canada: 1980–Q3 2024; quarterly
**Access:** Public, downloadable from NY Fed website (newyorkfed.org/research/policy/rstar)
**Key variables available:**
- r* (neutral real rate) for US, EA, UK, Canada — the four largest advanced economies
- Potential growth g* (which r* closely tracks in HLW specification)
- Trend inflation and other state variables

**Known issues:**
- Limited to 4 countries; cannot construct a global r* directly from this source alone
- HLW estimates have very wide Kalman filter confidence bands; real-time uncertainty is large
- Strong parametric assumptions (state space model); sensitivity to lambda parameter
- No EM coverage

**Feasibility grade: A** for advanced economy r* benchmark; **C** for global r* (limited country scope)
**Key papers:** Holston, Laubach & Williams (2017, JME); widely used in macroeconomic panel work

---

### E2. Rachel & Smith (2015) / Rachel & Summers (2019) Global r* Estimates

**Provider:** Bank of England (working paper series) / Brookings
**Coverage:** ~1980–2015 (Rachel & Smith); extended to 2019 (Rachel & Summers); annual
**Access:** Public, downloadable from Bank of England website and Brookings; data appendix available
**Key variables available:**
- Constructed global r* (weighted average of advanced economies)
- Decomposition into: demographic component, productivity component, inequality/precautionary savings component, safety premium component
- World saving and investment rate decomposition

**Known issues:**
- Annual frequency; no quarterly disaggregation
- Not updated beyond 2019; requires extrapolation or alternative for 2020–2023
- Methodology is accounting-based decomposition, not structural estimation
- Global aggregate hides substantial cross-country heterogeneity

**Feasibility grade: A** for global r* trend variable; series needs extension to 2023
**Key papers:** Rachel & Smith (2015, BOE WP); Rachel & Summers (2019, Brookings Papers)

---

### E3. BIS Long-Run Real Interest Rate Estimates

**Provider:** Bank for International Settlements
**Coverage:** Borio, Disyatat, Juselius & Rungcharoenkitkul (2017): ~19 advanced economies, 1870–2016; annual
**Access:** Public, working paper appendix; BIS website
**Key variables available:**
- Long-term real interest rates (ex-post and ex-ante) for a panel of AEs
- Decomposition of long-run rate decline
- Useful as alternative global r* proxy

**Known issues:**
- Working paper vintage; may not be updated post-2016
- Advanced economies only
- Ex-ante real rate requires inflation expectations series (themselves uncertain)

**Feasibility grade: B** for robustness check on r* specification

---

### E4. Supporting Global Variables (World GDP Growth, Global Saving, VIX)

**World GDP growth:** IMF WEO `NGDP_RPCH` aggregated with PPP weights — **Grade A**
**Global saving rate:** WEO `NGSD_NGDP` at world level, or computed from IMF IFS — **Grade A**
**VIX:** CBOE Volatility Index via FRED (Federal Reserve Bank of St. Louis) — 1990–present, daily/monthly/annual — **Grade A**

---

## F. Controls and REER

### F1. Real Effective Exchange Rate (REER)

**Provider 1:** BIS Effective Exchange Rate Indices
**Coverage:** ~64 countries, 1964–2024; monthly; narrow and broad REER indices (26 and 61 trading partners)
**Access:** Public, downloadable (bis.org/statistics/eer.htm)
**Key variables:** Narrow REER (26 trading partners), Broad REER (61 trading partners), CPI-deflated and PPI-deflated

**Provider 2:** IMF Information Notice System (INS) / IFS REER
**Coverage:** ~190 countries, 1970s–2024; monthly
**Access:** Public via IMF Data

**Provider 3:** Darvas (2012) "Compositional Effects on Productivity, Labour Cost and Export Adjustment" — Bruegel dataset
**Coverage:** ~178 countries, 1995–2022
**Access:** Public (bruegel.org)

**Known issues for all REER sources:**
- Choice of deflator (CPI vs. PPI vs. ULC) matters for external competitiveness channel
- Country pair weights and base year affect levels comparisons
- For ECM short-run dynamics, monthly BIS REER averaged to annual is standard

**Feasibility grade: A** (BIS as primary, IFS as gap-filler)
**Key papers:** IMF EBA uses BIS REER; Gruber & Kamin (2007)

---

### F2. Population Growth (Working-Age, n_it)

**Provider:** UN WPP (same as B1) — working-age population (15–64) growth rate
**Coverage:** 1950–2100; all countries
**Access:** Public (computed from WPP age-group series)
**Known issues:** Consistent with main demographic data; no additional sourcing needed
**Feasibility grade: A**

---

## G. Bilateral Data (Extensions)

### G1. IMF Coordinated Portfolio Investment Survey (CPIS)

**Provider:** IMF Statistics Department
**Coverage:** 2001–2023 annual; ~80 reporting economies; ~250 destination economies
**Access:** Public via IMF Data (imf.org/en/Data); downloadable CSV
**Key variables:** Bilateral portfolio holdings A_ijt: total portfolio, equity securities, long-term debt securities, short-term debt securities
**Known issues:**
- Starts only in 2001 (with a trial survey in 1997); no pre-2001 data
- Reporting countries (~80) differ from receiving countries; asymmetric coverage
- Large "confidential" cells masked; offshore financial centers (Cayman Islands, Luxembourg) are major hubs and distort bilateral patterns
- EMs underrepresented as reporters before 2010

**Feasibility grade: A** for 2001–2023 bilateral portfolio extension; **D** for pre-2001 or full-panel period
**Key papers:** Alfaro et al. (2008); Lane & Milesi-Ferretti (2008) bilateral positions paper

---

### G2. IMF Coordinated Direct Investment Survey (CDIS)

**Provider:** IMF Statistics Department
**Coverage:** 2009–2022 annual; ~100 reporting economies
**Access:** Public via IMF Data
**Key variables:** Bilateral inward and outward FDI stocks between reporting pairs; by financial instrument
**Known issues:**
- Starts 2009 only; very limited temporal coverage for panel use
- Round-tripping (tax haven transit) inflates bilateral FDI; Netherlands, Luxembourg, Ireland, BVI distort bilateral patterns
- Ultimate investor basis vs. immediate investor basis differ substantially

**Feasibility grade: B** for cross-sectional/recent panel analysis; **C** for long panel (too short)

---

### G3. BIS Locational Banking Statistics (LBS)

**Provider:** Bank for International Settlements
**Coverage:** 1983–present (quarterly); ~50 reporting countries (BIS-reporting banks)
**Access:** Public, downloadable (bis.org/statistics/bankstats.htm)
**Key variables:** Bilateral cross-border banking claims and liabilities between reporting country and counterparty country; by instrument and currency; by sector (bank vs. non-bank)
**Known issues:**
- Reporting side only (not destination side); coverage gaps for non-reporting countries as creditors
- Locational (not consolidated) basis: follows where the booking office is located, which differs from ultimate risk
- Currency composition available only from 2012; currency breakdown key for valuation effects

**Feasibility grade: A** for bilateral banking claims; good temporal coverage from 1983
**Key papers:** Lane & Milesi-Ferretti (2007) use BIS to crosscheck; Gourinchas & Rey (2007)

---

### G4. Gravity Controls (CEPII / GeoDist Database)

**Provider:** CEPII (Centre d'Études Prospectives et d'Informations Internationales)
**Coverage:** ~220 country pairs; time-invariant structural variables
**Access:** Public, free download (cepii.fr/CEPII/en/bdd_modele/bdd_modele.asp)
**Key variables:**
- Bilateral geodesic distance (simple and weighted by city population)
- Common language (official, spoken)
- Colonial relationship (ever, current)
- Common legal origin (French, British, German, Scandinavian, Socialist civil law)
- Contiguity, landlocked status, island status
- Time-varying: bilateral RTA membership (DESTA database complement)

**Known issues:**
- Time-invariant variables cannot identify within-pair variation; only useful with cross-sectional or between-pair variation
- DESTA database (Dür, Baccini & Elsig 2014) needed for time-varying trade agreement dummies

**Feasibility grade: A** for gravity controls

---

## Feasibility Summary Table

| Variable | Best Source | Grade | Key Issue |
|---|---|---|---|
| NIIP (% GDP) | Lane & Milesi-Ferretti EWN | A | Pre-1990 EM estimates noisy |
| Current Account | IMF WEO / IFS | A | BPM5→BPM6 splice |
| Valuation effects (VAL) | LMF EWN (ΔNIIP − CA) | A | Residual; absorbs E&O pre-2001 |
| Capital transfers (CAP) | IMF IFS BOP | B | Thin pre-1995 for EMs |
| Errors & omissions (EOM) | IMF IFS BOP | B | Volatile; methodology breaks |
| Old-age dependency (current) | UN WPP current vintage | A | Country coverage varies pre-1990 |
| Anticipated dependency E_t[φ_{t+T}] | UN WPP historical vintages | B | PDF/manual extraction pre-2000 |
| Life expectancy at 65 (e_65) | HMD (AEs) + UN WPP | A/C | HMD: 41 countries only |
| Real GDP per capita | PWT 10.x / WEO | A | PWT ends 2019; WEO for recent years |
| Country TFP (not util.-adj.) | PWT 10.x `ctfp` | B | Not utilization-adjusted |
| Country TFP (util.-adj., AEs) | EU-KLEMS 2023 | A | OECD only, 30 countries |
| Country TFP (util.-adj., EMs) | World KLEMS | C | Heterogeneous, gaps |
| Country-specific TFP (ã_it) | PWT + global factor residual | B | Requires methodological choice |
| Gross public debt (d^g) | IMF WEO | A | Concept variation across countries |
| Structural primary balance | IMF WEO | B | Revision risk; 2014 methodology break |
| Global r* | Rachel & Smith + HLW | A | R&S ends 2019; needs extension |
| World GDP growth | IMF WEO world aggregate | A | — |
| Global saving rate | IMF WEO world aggregate | A | — |
| VIX | CBOE/FRED | A | Only from 1990 |
| REER | BIS EER | A | Deflator choice matters |
| Working-age population growth | UN WPP | A | Consistent with other WPP variables |
| Bilateral portfolio (CPIS) | IMF CPIS | A | Only from 2001 |
| Bilateral FDI (CDIS) | IMF CDIS | B | Only from 2009 |
| Bilateral banking (BIS LBS) | BIS Locational Banking Stats | A | 50 reporting countries only |
| Gravity controls | CEPII GeoDist | A | Time-invariant; suits cross-section |

---

## Critical Gaps

### Gap 1: Utilization-Adjusted TFP for Emerging Markets (Severe)
No public database provides long-run utilization-adjusted TFP for a 40–60 country panel. The workaround — using PWT `ctfp` and controlling for the output gap — is common in the literature but imperfect. Papers in this literature (e.g., Gruber & Kamin 2007; Chinn & Prasad 2003) typically use log GDP per capita relative to the US as a catch-all productivity proxy rather than structural TFP. The researcher should evaluate whether ã_it can be approximated by: (a) PWT `ctfp` minus a global factor; (b) the Solow residual from national accounts data; or (c) GDP per capita relative to frontier. This will likely be the most discussed measurement decision in referee reports.

### Gap 2: UN Population Projection Vintages Pre-2000 (Moderate-Severe)
Constructing E_t[φ_{i,t+T}] from genuine period-t projections before 2000 is extremely labor-intensive. The 1980–1998 WPP editions are PDF-only for most country-level detail. Practical options: (i) restrict the panel to 2000–2023 for the anticipated demographics specification; (ii) use the 2000 WPP vintage for all pre-2000 observations (a maintained assumption); (iii) use WPP-consistent cohort-based projections from the Wittgenstein Centre (which has longer machine-readable archives). This gap directly affects the core identification strategy.

### Gap 3: NIIP Decomposition Pre-2001 (Moderate)
The valuation effects channel (VAL_it) is mechanically computed as ΔNIIP − CA. Before 2001, the LMF EWN series is constructed from a mix of survey data and cumulated flows; the resulting valuation residual absorbs capital transfers and errors & omissions that cannot be separately identified. The paper's decomposition (ΔNIIP = CA + VAL + CAP + EOM) will be cleanly estimable only for 2001–2023.

### Gap 4: Global r* After 2019 (Minor-Moderate)
Rachel & Smith (2015) and Rachel & Summers (2019) global r* estimates end around 2015–2019. For 2020–2023, the researcher must either: (a) extrapolate using HLW for AE aggregate; (b) use US or EA r* from HLW as global proxy; or (c) use market-based long-run real rate expectations (e.g., 10-year TIPS real yield, 5y5y inflation swap rates) as supplements. The COVID/post-COVID period is particularly challenging for r* estimation regardless of method.

### Gap 5: Structural Primary Balance Quality for EMs (Moderate)
WEO structural balance estimates for EMs are IMF desk estimates of varying quality; they are frequently revised, and the 2014 methodology change creates a structural break. For EMs, the researcher may need to construct a country-specific cyclical adjustment using the output gap and fiscal multiplier assumptions from the literature.

### Gap 6: BIS VIX Availability Pre-1990 (Minor)
VIX is available only from 1986 (CBOE historical) and robustly from 1990. If the panel extends to 1980, an alternative risk proxy is needed for 1980–1989. Options: US stock return volatility (CRSP); geopolitical risk index (Caldara & Iacoviello 2022); G7 real interest rate variance.

---

## Recommended Data Stack

For a viable paper at N≈50, T≈30 (1994–2023 for core; 1985–2023 with caveats):

### Core Panel Stack
| Variable | Source | Download Location |
|---|---|---|
| NIIP (% GDP) | LMF EWN (2022 update) | IMF/PIIE website |
| Current account | IMF WEO (April vintage each year) | imf.org/WEO |
| Gross public debt | IMF WEO `GGXWDG_NGDP` | imf.org/WEO |
| Structural primary balance | IMF WEO `GGCBP` | imf.org/WEO |
| GDP per capita (real) | PWT 10.x `rgdpna`/pop or WEO | rug.nl/ggdc/pwt |
| Country TFP (baseline) | PWT 10.x `ctfp` | rug.nl/ggdc/pwt |
| Country TFP (AE supplement) | EU-KLEMS 2023 | euklems.net |
| Old-age dependency (current) | UN WPP 2024 current vintage | population.un.org/wpp |
| Anticipated dependency | UN WPP vintages 2000, 2002, ..., 2022 | population.un.org/wpp/archive |
| Life expectancy at 65 (AEs) | Human Mortality Database | mortality.org |
| Life expectancy at 65 (EMs) | UN WPP core series | population.un.org/wpp |
| Population growth (15–64) | UN WPP 2024 | population.un.org/wpp |
| REER | BIS EER (narrow, CPI-deflated) | bis.org/statistics/eer |
| Global r* | Rachel & Summers (2019) + HLW extension | BoE WP / NY Fed |
| VIX | FRED (VIXCLS series) | fred.stlouisfed.org |
| World GDP growth | IMF WEO | imf.org/WEO |

### Extension Stack (Bilateral Analysis)
| Variable | Source |
|---|---|
| Bilateral portfolio holdings | IMF CPIS (2001–2023) |
| Bilateral banking claims | BIS Locational Banking Statistics |
| Bilateral FDI stocks | IMF CDIS (2009–2022) |
| Gravity variables | CEPII GeoDist + DESTA RTA database |

### Country Sample Recommendation
- **Core 40-country sample:** G7 + EA periphery (Greece, Portugal, Spain, Ireland) + OECD EMs (Korea, Mexico, Turkey, Chile, Czech Republic, Hungary, Poland) + major non-OECD EMs (Brazil, China, India, Indonesia, Russia, South Africa, Thailand, Malaysia) + major commodity exporters with good data (Norway, Australia, Canada, Saudi Arabia, Nigeria, Angola)
- Exclude very small economies, tax havens, and countries with fewer than 20 years of NIIP data
- Split sample robustness: advanced economies (EU-KLEMS TFP available) vs. emerging markets (PWT only)

---

## Data Assembly Timeline Estimate

| Task | Effort | Parallelizable |
|---|---|---|
| Download and merge core macro variables (NIIP, CA, debt, REER, VIX, r*) | 1–2 weeks | Yes |
| UN WPP current vintage demographics (all age groups, 200 countries) | 3–5 days | Yes |
| UN WPP vintage projection extraction (2000–2022 editions, 12 files) | 2–3 weeks | Partially |
| HMD life expectancy at 65 (registration + download, 41 countries) | 2–3 days | Yes |
| PWT 10.x TFP: download, merge, construct global factor, compute ã_it | 1 week | Yes |
| EU-KLEMS 2023: download, aggregate industry→economy, merge to panel | 1–2 weeks | Yes |
| IMF WEO structural balance: download April vintages, splice methodology break | 1–2 weeks | Yes |
| r* compilation and extension to 2023 | 1 week | Yes |
| Panel assembly, variable construction, country-year merging | 2–3 weeks | No |
| Validation, outlier checks, documentation | 1–2 weeks | No |
| **Total (sequential critical path)** | **8–14 weeks** | — |

**Recommended resourcing:** One RA focused on the UN WPP vintage extraction (the most labor-intensive single task) while the lead researcher assembles the core macro panel in parallel. The TFP decision (PWT baseline vs. EU-KLEMS supplement) should be made first, as it affects the country sample and panel dimensions.

---

*Report generated by the explorer agent, 2026-05-19.*
*This report covers public and administrative data only. Restricted or proprietary data (e.g., Consensus Economics long-run forecasts as alternative to UN WPP projections) are not evaluated but could be considered if institutional access is available.*
