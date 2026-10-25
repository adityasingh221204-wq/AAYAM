# AAYAM Project — Cross-Team Collaboration & Handoff Document

> **Module:** AI/ML & Opportunity Intelligence  
> **Contributor:** Aarushi  
> **Feature Branch:** `feat/aarushi-ai-ml`  
> **Status:** ✅ Complete & Verified (113/113 Unit Tests Passing)  
> **Target Reviewer:** Project Lead & Platform Team

---

## 1. 📌 Deliverables Completed by Aarushi (AI/ML & Opportunity Intelligence)

All core requirements set forth in `TEAM_COLLABORATION.md` for Member 3 have been completed, verified against canonical contracts, and covered with unit tests:

### 1.1 Enhanced Opportunity Pathways Engine & Explorer (`pages/3_Opportunity_Pathways.py`)
- **Multi-Factor Filter Sidebar**: Filter pathways dynamically by `track` (Employment / Self-Employment / Micro-Enterprise), `sector`, `location_type`, and max upfront capital required.
- **Ranked Opportunity Cards**: Rendered with:
  - Title, sector, track, and color-coded `fit_tier` badges (`High Alignment`, `Moderate Alignment`, `Development Opportunity`).
  - Required education and interactive skills breakdown: matched skills highlighted in green (`✓`), missing skills in amber (`+`).
  - Transparent 4-item explainability list detailing reasons for match scoring.
- **Affordability Analysis ("Can I afford this?")**:
  - Automatically assesses liquid savings vs. upfront cost.
  - Evaluates eligibility for **PM Mudra Yojana (Shishu/Kishor)** with 15% margin money coverage.
- **Sub-score Breakdown Chart**: Integrated `plot_opportunity_score_breakdown(opp)` horizontal bar chart showing points across Skills (40), Affordability (25), Education (15), and Monthly Income Uplift (20).

### 1.2 India Intelligence Macro Telemetry Dashboard (`pages/6_India_Intelligence.py`)
- **5 Dedicated Functional Tabs**:
  1. `💳 RBI Payments`: Real-time telemetry, YoY growth rates, payment channel selector (UPI, RTGS, NEFT, IMPS, Cards), and monthly volume trend analysis.
  2. `🚨 Fraud Trends`: Analysis of Central Payments Fraud Information Registry (CPFIR) volume, value, and basis points.
  3. `💼 Labour Force`: Sectoral comparison bar chart (Rural vs. Urban vs. Combined for LFPR, WPR, and UR) + State-level workforce indicators.
  4. `🛒 Household Expenditure`: HCES 2023-24 monthly per capita consumption expenditure fractile analysis.
  5. `🏭 Enterprises`: ASUSE 2023-24 unincorporated enterprise analytics, GVA, and worker compensation.

### 1.3 Expanded Opportunity Catalogue Dataset & ETL Pipeline
- **Dataset Expansion**: Expanded `data/processed/opportunities/opportunity_catalogue.csv` and `.json` from 8 to **12 canonical pathways**, adding:
  1. `OPP-EMP-009`: Community Digital Health Assistant & Ayushman Bharat Field Coordinator (Healthcare, ABDM / NSDC).
  2. `OPP-EMP-010`: Quick-Commerce Fleet Hub Supervisor & EV Dispatcher (Logistics & Clean Mobility, PMKVY / LSSC).
  3. `OPP-ENT-011`: Women-Led SHG Handloom & Agri-Artisan Micro-Enterprise (Textiles & Crafts, NRLM Lakhpati Didi / Mudra Tarun).
  4. `OPP-ENT-012`: PM SVANidhi Urban Micro-Retail & Digital Smart Food Cart (Urban Retail, PM SVANidhi / FSSAI FoSTaC).
- **Government Scheme Linkages**: Validated 100% scheme linkages across all 12 records (PMKVY 4.0, PM Mudra Yojana, PMEGP, PM-JAY/ABDM, PM SVANidhi, NRLM).
- **ETL Synchronization**: Updated `scripts/preprocess_datasets.py` `build_opportunities()` to maintain catalog integrity across automated rebuilds.

### 1.4 Chart Library Additions (`src/ui/charts.py`)
- `plot_opportunity_score_breakdown(opp: dict) -> go.Figure`: 4-component horizontal breakdown chart.
- `plot_rbi_system_trend(df_payments: pd.DataFrame, system_name: str) -> go.Figure`: Specific payment rail volume trend line.
- `plot_plfs_wpr_by_state(df_plfs: pd.DataFrame) -> go.Figure`: State-level workforce comparisons.
- `plot_hces_fractiles(df_hces: pd.DataFrame, sector: str) -> go.Figure`: Consumption expenditure deciles.

### 1.5 Unit Test Suite (`tests/test_recommendations_recovery_loaders.py`)
- Added 5 new targeted unit tests:
  - `test_opportunity_catalogue_expanded_count`: Asserts ≥ 12 opportunities loaded.
  - `test_new_opportunities_present`: Asserts presence of new IDs (`OPP-EMP-009` through `OPP-ENT-012`).
  - `test_all_opportunities_have_valid_scheme_linkage`: Validates scheme integrity.
  - `test_rank_opportunities_with_new_catalogue`: Tests ranking with a live healthcare profile.
  - `test_mudra_margin_money_affordability`: Tests margin money affordability heuristics.
- **Suite Results:** 113 / 113 passing tests (`python -m pytest tests/`).

---

## 2. 🤝 What Other Teammates Need to Know & Do

### 🛡️ For Member 2 (Cybersecurity & Threat Intelligence — `feat/member2-cybersecurity`):
- **Current State:** The test suite and data loaders are fully functional. Your base files (`src/engines/cyber.py`, `pages/4_CyberDrishti.py`, `pages/7_Trust_Graph.py`, `pages/8_Recovery_Centre.py`) are unblocked.
- **Dependencies from M3:** When building `pages/7_Trust_Graph.py`, the network graph can link to `src/ui/charts.py`.
- **Action Items Left:**
  1. Add 5 new threat rules to `src/engines/cyber.py` (e.g., job offer WhatsApp scams, fake KYC update links, lottery winner impersonation, reverse UPI chargeback lures).
  2. Add 5 new CERT-In advisories to `data/processed/cyber_threats/cert_in_advisories.csv`.
  3. Complete the interactive Plotly network graph in `pages/7_Trust_Graph.py`.
  4. Write 5 unit tests in `tests/test_cyber_engine.py`.

### 🖥️ For Member 4 (Platform, UI/UX & DevOps — `feat/member4-platform`):
- **Current State:** Member 3 has implemented the UI components and sub-score charts.
- **CSS Classes Needed in `src/ui/theme.py`:**
  - `.aayam-badge-tier`, `.aayam-badge-tier-high`, `.aayam-badge-tier-mod`, `.aayam-badge-tier-dev` (color badges for fit tiers).
  - `.aayam-progress-bar` (custom gradient bars for scores).
- **Action Items Left:**
  1. Enhance `pages/1_Command_Centre.py` with the "System Health" telemetry sidebar (12 opportunities, 6 public datasets, 113+ tests) and inline quick threat screen.
  2. Polish `app.py` with CSS card entrance animations and the "About AAYAM & SDG Alignment" collapsible expander.
  3. Add `tests/conftest.py` with shared fixtures to unify test fixtures across members.
  4. Final deployment validation on Streamlit Cloud / local runner.

### 👤 For Member 1 / Project Lead (`main` / `feat/member1-fintech`):
- **Current State:** Feature branch `feat/aarushi-ai-ml` is ready for review and merge via Pull Request.
- **Review Checklist:**
  - [x] All 113 unit tests pass cleanly (`python -m pytest tests/`).
  - [x] No temporary batch scripts committed.
  - [x] Clean git history under Aarushi (`connect2aarushi@gmail.com`).
  - [x] Data provenance and legal disclaimers present on all enhanced pages.

---

## 3. 🧪 Verification Command

To verify the test suite:
```bash
git checkout feat/aarushi-ai-ml
python -m pytest tests/ -v
streamlit run app.py
```
