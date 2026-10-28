# AAYAM Project — Team Collaboration Guide

> **Repository:** [github.com/adityasingh221204-wq/AAYAM](https://github.com/adityasingh221204-wq/AAYAM)
> **Stack:** Python 3.12 · Streamlit · Plotly · pandas · pytest

---

## 📌 What Has Already Been Built

The initial working version of AAYAM is live in the repository. Before you begin, **clone the repo and run it locally** so you understand what exists:

```bash
git clone https://github.com/adityasingh221204-wq/AAYAM.git
cd AAYAM
pip install -r requirements.txt
python scripts/preprocess_datasets.py   # regenerates all processed CSVs
python -m pytest tests/ -v              # verify 148 tests pass
streamlit run app.py                    # open http://localhost:8501
```

### What's in the repo

| Path | What It Is |
|---|---|
| `app.py` | Main homepage — launches the 8-module navigation |
| `pages/1_Command_Centre.py` | Executive unified dashboard |
| `pages/2_Economic_Digital_Twin.py` | Personal financial profile & resilience scoring |
| `pages/3_Opportunity_Pathways.py` | Ranked employment & enterprise pathways |
| `pages/4_CyberDrishti.py` | Live suspicious message screener |
| `pages/5_ArthSim.py` | What-if financial scenario simulator |
| `pages/6_India_Intelligence.py` | RBI + PLFS + HCES macroeconomic analytics |
| `pages/7_Trust_Graph.py` | Cyber threat relationship graph |
| `pages/8_Recovery_Centre.py` | Incident response playbook |
| `src/engines/economy.py` | Financial indicators & resilience score engine |
| `src/engines/cyber.py` | CyberDrishti 8-rule threat detection engine |
| `src/engines/recommendations.py` | Opportunity ranking engine |
| `src/engines/simulator.py` | ArthSim scenario simulator |
| `src/engines/recovery.py` | Incident recovery playbook engine |
| `src/data/loaders.py` | Canonical public dataset loader |
| `src/ui/theme.py` | Dark fintech CSS theme |
| `src/ui/components.py` | Reusable Streamlit widgets |
| `src/ui/charts.py` | Plotly chart builders |
| `scripts/preprocess_datasets.py` | Full ETL pipeline |
| `data/processed/**/*.csv` | All preprocessed public datasets |
| `tests/` | 108 unit tests — all passing |
| `docs/ARCHITECTURE.md` | System architecture & methodology |
| `README.md` | Project overview |

---

## 🌿 Git Workflow — MANDATORY FOR ALL MEMBERS

> **Never commit directly to `main`.** All work goes into a feature branch, then a Pull Request.

### Step 1 — Create your branch (do this first, before any edits)

```bash
# Clone (if not already done)
git clone https://github.com/adityasingh221204-wq/AAYAM.git
cd AAYAM

# Create and switch to your personal branch
git checkout -b feat/member1-fintech        # Member 1
git checkout -b feat/member2-cybersecurity  # Member 2
git checkout -b feat/member3-ai-ml          # Member 3
git checkout -b feat/member4-platform       # Member 4
```

### Step 2 — Do your work (details per member below)

### Step 3 — Commit and push

```bash
git add -A
git commit -m "[M1] Brief description of what you changed"
git push origin feat/member1-fintech
```

### Step 4 — Open a Pull Request on GitHub

- Go to the repo on GitHub
- Click **"Compare & pull request"**
- Add a short description of your changes
- Request review from at least **one other team member**
- The PR will only be merged after 1 approval and **`python -m pytest tests/` passes**

---

## 👤 Member 1 (Aditya Singh) — FinTech & Data Engineering

### Your files
- `src/engines/economy.py` — financial indicators engine
- `src/engines/simulator.py` — ArthSim scenario simulator
- `src/data/loaders.py` — dataset loader
- `pages/2_Economic_Digital_Twin.py` — Digital Twin UI
- `pages/5_ArthSim.py` — ArthSim UI
- `tests/test_economy_engine.py` — your engine tests
- `tests/test_simulator_engine.py` — your simulator tests

### Work to complete

1. **Enhance the Digital Twin page** (`pages/2_Economic_Digital_Twin.py`):
   - Add a sidebar form that lets users update their full profile (income, expenses, savings, debt, EMIs, skills, education, region)
   - Display the calculated resilience score with a `st.progress()` bar and color-coded category badge
   - Show the `component_scores` breakdown as a horizontal Plotly bar chart
   - List all `risk_factors` as warning alert boxes and `positive_indicators` as success boxes
   - Show `recommendations` as numbered action items

2. **Enhance the ArthSim page** (`pages/5_ArthSim.py`):
   - Let users pick a `scenario_type` from a `st.selectbox` (job_loss, fraud_loss, medical_emergency, business_startup, inflation_shock)
   - Add sliders for income change %, lump sum loss amount, expense change %, and duration
   - Render a dual-line Plotly chart: baseline savings vs. scenario savings over time
   - Show `months_to_depletion` as a highlighted metric card
   - Display the `resilience_shift` with a colored delta indicator

3. **Add a new RBI dataset** (if updated data is available):
   - Add the latest RBI Payment System Indicators bulletin CSV to `data/raw/rbi/`
   - Update `scripts/preprocess_datasets.py` to process it
   - Push the new processed CSV to your branch

4. **Write at least 5 new tests** for any new functionality you add in `tests/test_economy_engine.py`

### Commit prefix: `[M1]`
### Branch: `feat/member1-fintech`

---

## 🛡️ Member 2 (Abhishek Shrivastava) — Cybersecurity & Threat Intelligence

### Your files
- `src/engines/cyber.py` — CyberDrishti engine
- `src/engines/recovery.py` — Recovery Centre engine
- `data/processed/cyber_threats/cert_in_advisories.csv` — CERT-In advisories
- `pages/4_CyberDrishti.py` — threat screener UI
- `pages/7_Trust_Graph.py` — threat graph UI
- `pages/8_Recovery_Centre.py` — recovery playbook UI
- `tests/test_cyber_engine.py` — your engine tests

### Work to complete

1. **Enhance the CyberDrishti page** (`pages/4_CyberDrishti.py`):
   - Add a `st.text_area` for pasting a suspicious SMS/WhatsApp message
   - Display the `risk_score` as a color-coded `st.progress()` bar (red >60, orange >35, yellow >15, green otherwise)
   - Show each `triggered_patterns` entry as an expandable `st.expander` with the code, category, severity, matched terms, and explanation
   - List `safety_guidance` as a numbered checklist with ⚠️ icons

2. **Enhance the Trust Graph page** (`pages/7_Trust_Graph.py`):
   - Build an interactive Plotly network graph using `networkx` showing:
     - Threat nodes (e.g. Digital Arrest, APK Delivery, Reverse UPI)
     - Attack stage nodes (Lure → Credential Harvest → Exfiltration)
     - Defense nodes (1930 Helpline, CERT-In, cybercrime.gov.in)
   - Color threat nodes red, defense nodes green, attack stage nodes amber

3. **Enhance the Recovery Centre page** (`pages/8_Recovery_Centre.py`):
   - Add a `st.selectbox` for incident type selection
   - Render each step as a styled card with priority badge, action title, instructions, and official portal link
   - Add a downloadable checklist button (use `st.download_button` with text content)

4. **Expand the CERT-In advisory dataset**:
   - Add at least 5 new advisory rows to `data/processed/cyber_threats/cert_in_advisories.csv`
   - Source from publicly available CERT-In advisories at https://www.cert-in.org.in/
   - Re-run `scripts/preprocess_datasets.py` and push the updated CSV on your branch

5. **Add at least 5 new threat rules** to `SUSPICIOUS_RULES` in `cyber.py`:
   - Consider: job offer WhatsApp scams, fake KYC update links, lottery winner impersonation, fake RBI freeze notices
   - Each rule must follow the existing structure exactly and have accompanying tests

6. **Write at least 5 new tests** for any new rules or functionality you add

### Commit prefix: `[M2]`
### Branch: `feat/member2-cybersecurity`

---

## 🤖 Member 3 (Aarushi S.) — AI/ML & Opportunity Intelligence

### Your files
- `src/engines/recommendations.py` — opportunity ranking engine
- `data/processed/opportunities/opportunity_catalogue.csv` — opportunity catalogue
- `pages/3_Opportunity_Pathways.py` — opportunity explorer UI
- `pages/6_India_Intelligence.py` — macro analytics UI
- `tests/test_recommendations_recovery_loaders.py` — your tests (shared)

### Work Status: ✅ COMPLETED (See docs/HANDOFF.md)

1. **[x] Enhance the Opportunity Pathways page** (`pages/3_Opportunity_Pathways.py`):
   - Show ranked results as styled cards with:
     - Title, sector, and `fit_tier` badge (color-coded: green = High Alignment, blue = Moderate, grey = Development Opportunity)
     - A Plotly horizontal bar chart showing the 4 sub-scores (skills, affordability, education, uplift)
     - `matched_skills` as green tags, `missing_skills` as amber tags
     - `transparent_reasons` as a 4-item numbered list
   - Add a filter sidebar: filter by `track` (Employment / Enterprise), `sector`, and `location_type`
   - Add a "Can I afford this?" tooltip showing `total_upfront_cost_inr` and whether Mudra loan applies

2. **[x] Enhance the India Intelligence page** (`pages/6_India_Intelligence.py`):
   - Add tabs for: RBI Payments | Fraud Trends | Labour Force | Household Expenditure | Enterprises
   - In the RBI Payments tab, add a `st.selectbox` to filter by payment system (UPI, RTGS, NEFT, etc.)
   - Plot a trend line for the selected payment system's monthly volume
   - In the Labour Force tab, add a bar chart comparing LFPR, WPR, and UR across Urban/Rural sectors

3. **[x] Expand the opportunity catalogue**:
   - Add at least 4 new opportunities to `data/processed/opportunities/opportunity_catalogue.csv`
   - Suggested sectors: Healthcare/ASHA worker support, Logistics/Delivery, Women-led SHG enterprises, PM SVANidhi street vendor scheme
   - Each row must include all 15 existing columns. Refer to existing rows for format.
   - Source income estimates from government scheme documents or NSDC job role standards
   - Push the updated catalogue on your branch

4. **[x] Link opportunities to government schemes**:
   - The `scheme_linkage` column should contain the relevant government scheme (e.g., "PMKVY 4.0 | NSDC", "PM Mudra Yojana | Shishu", "PMEGP")
   - Ensure all 8 existing rows and your new rows have valid scheme linkages

5. **[x] Write at least 5 new tests** for any new opportunities or filtering logic you add (All 113 passing)

### Branch: `feat/aarushi-ai-ml`

---

## 🖥️ Member 4 (Ansh Saini) — UI / UX & Platform

### Your files
- `app.py` — main homepage
- `src/ui/theme.py` — CSS design system
- `src/ui/components.py` — reusable Streamlit widgets
- `src/ui/charts.py` — Plotly chart builders
- `src/utils/config.py` — app constants
- `pages/1_Command_Centre.py` — executive dashboard UI
- `.streamlit/config.toml` — server config

### Work Status: ✅ COMPLETED (feat/member4-platform — 148/148 Tests Passing)

1. **[x] Enhance the Command Centre page** (`pages/1_Command_Centre.py`):
   - Added "System Health" telemetry sidebar showing: 8 verified datasets, 12 career pathways, 148 unit tests passing, and February 2025 bulletin status
   - Added "Quick Threat Screen" widget in sidebar running inline `assess_cyber_risk()` with color-coded risk badge and direct link to CyberDrishti
   - Enhanced macro section with dynamic `st.metric()` cards showing UPI monthly volume (1,610.6 Cr), MoM change (-5.2%), and YoY change (+33.1%)

2. **[x] Polish the Homepage** (`app.py`):
   - Animated entrance effects to module cards with smooth hover lift transitions
   - Collapsible "About AAYAM" `st.expander` detailing academic mission, architectural pillars, and UN SDG alignment (SDG 1, 8, 16)
   - Real-time IST clock in sidebar (`timezone(timedelta(hours=5, minutes=30))`) and 3-step quick-start onboarding

3. **[x] Improve the design system** (`src/ui/theme.py`):
   - `.aayam-badge-tier`, `.aayam-badge-tier-high`, `.aayam-badge-tier-mod`, `.aayam-badge-tier-dev` for alignment fit tiers
   - `.aayam-progress-bar` with gradient fill for suspicion meter and resilience scoring
   - Smooth glassmorphism transitions and responsive card hovers (`transform: translateY(-4px)`)

4. **[x] Chart library completions** (`src/ui/charts.py`):
   - `plot_resilience_gauge(score: float) -> go.Figure` — Plotly gauge indicator (0–100)
   - `plot_opportunity_score_breakdown(opp: dict) -> go.Figure` — horizontal 4-bar score breakdown chart
   - `plot_threat_network(nodes: list, edges: list) -> go.Figure` — Plotly network graph used in `pages/7_Trust_Graph.py`

5. **[x] Add `conftest.py` for test suite**:
   - Created `tests/conftest.py` with shared cross-module fixtures: `demo_profile`, `healthy_profile`, `stressed_profile`, `zero_income_profile`, `base_scenario`, `sample_message_phishing`, `sample_message_digital_arrest`, `sample_message_clean`, `sample_opportunities`, `sample_network_nodes_edges`
   - Added dedicated unit tests in `tests/test_platform_ui.py` (18 new tests, 148 total passing)

6. **[x] Deployment preparation**:
   - Updated `requirements.txt` with `flask>=3.0.0`, `plotly>=5.20.0`, `networkx>=3.2.0`
   - Added `CONTRIBUTING.md` with complete collaboration guide, commit conventions (`[M1]`–`[M4]`), and PR checklists
   - Verified clean application import and startup

### Commit prefix: `[M4]`
### Branch: `feat/member4-platform`

---

## 📋 General Rules for All Members

### Before you start working
```bash
git checkout main
git pull origin main          # get latest
git checkout -b feat/memberX-your-role
```

### When adding a new dataset
1. Put raw files in `data/raw/<source>/` (e.g. `data/raw/nsdc/`)
2. Add processing logic in `scripts/preprocess_datasets.py`
3. Register the dataset in `src/data/loaders.py` → `DATASET_REGISTRY`
4. Add schema columns in `src/data/schemas.py`
5. Commit the processed CSV to `data/processed/<source>/`
6. **Never commit API keys, passwords, or personal data**

### Test requirements
- Run `python -m pytest tests/ -v` before every commit
- All 108 existing tests must continue to pass
- Add at least 5 new tests per feature you build

### Code style
- All functions must have a docstring with Args and Returns
- Use `from src.utils.logging_config import logger` for logging — never `print()`
- Never call `st.set_page_config()` more than once per page
- Always call `apply_theme()` at the top of every page after `set_page_config()`

### Pull Request checklist
- [ ] Branch is up to date with `main` (`git rebase main`)
- [ ] `python -m pytest tests/` passes (108+ tests)
- [ ] New functionality has docstrings
- [ ] `render_data_provenance()` is called for any new data displayed
- [ ] Disclaimers are shown for any new scoring or risk output
- [ ] PR description explains **what** was changed and **why**

---

## 🔗 Quick Links

| Resource | Link |
|---|---|
| Repository | https://github.com/adityasingh221204-wq/AAYAM |
| RBI Payment Indicators | https://www.rbi.org.in/Scripts/PSIUserView.aspx |
| CERT-In Advisories | https://www.cert-in.org.in/s2cMainServlet?pageid=PUBADVAISORY |
| MoSPI Open Data | https://microdata.gov.in/nada/index.php/catalog |
| NSDC Sector Skills | https://nsdcindia.org/sector-skill-councils |
| National Cyber Helpline | 1930 / https://cybercrime.gov.in |
| Streamlit Docs | https://docs.streamlit.io |
| Plotly Python Docs | https://plotly.com/python/ |

---

*This document was prepared by the project coordinator. Questions? Raise a GitHub Issue tagged with your member number.*
