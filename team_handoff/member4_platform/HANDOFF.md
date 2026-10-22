# AAYAM — Team Handoff: Member 4 — Platform, UI/UX & DevOps

## 🎯 Your Ownership Domain
You own everything related to **the Streamlit application, UI design system, page layout, deployment, and GitHub collaboration infrastructure**.

---

## 📁 Files You Own

| File | Purpose |
|---|---|
| `app.py` | Main entry point — homepage with 8-module navigation |
| `src/ui/theme.py` | `apply_theme()` — dark fintech CSS injection |
| `src/ui/components.py` | Reusable UI widgets (header, KPI card, alert, footer) |
| `src/ui/charts.py` | Plotly chart builders (cashflow, RBI growth, fraud trends) |
| `src/utils/config.py` | App constants, SDG alignment, region list |
| `src/utils/formatting.py` | `format_inr()`, `format_pct()` helpers |
| `src/utils/logging_config.py` | Centralized structured logger |
| `.streamlit/config.toml` | Streamlit server configuration |
| `requirements.txt` | Python package dependencies |
| `runtime.txt` | Python version pin for Streamlit Cloud |
| `pages/1_Command_Centre.py` | Executive dashboard |
| `pages/6_India_Intelligence.py` | Macro analytics |
| All other `pages/*.py` | UI rendering for each module |

---

## 🔑 Key UI Component Contracts

### `apply_theme()` → `None`
- Injects global dark fintech CSS via `st.markdown(..., unsafe_allow_html=True)`
- Must be called at the top of **every page**, immediately after `st.set_page_config()`

### `render_header(title, subtitle, badge_text, badge_type)` → `None`
- `badge_type`: `"emerald"` | `"amber"` | `"rose"` | `"indigo"` | `"sky"`

### `render_kpi_card(title, value, subtext, delta_text, badge_color)` → `None`
- Renders a bordered dark card with colored badge accent
- Use inside `st.columns()` for side-by-side metrics

### `render_alert_box(title, message, alert_type)` → `None`
- `alert_type`: `"info"` | `"warning"` | `"success"` | `"error"`

### `render_data_provenance(dataset, provider, period, url)` → `None`
- Always include below any chart or table using public data

### `render_footer()` → `None`
- Call at the bottom of every page

---

## 🎨 Design System Tokens

The theme is a **dark fintech aesthetic** (background `#0F172A`, surface `#1E293B`).

**Core color palette:**
```css
--emerald: #10B981   /* Primary brand / success */
--indigo:  #818CF8   /* Secondary accent */
--amber:   #FBBF24   /* Warning / attention */
--rose:    #FB7185   /* Danger / critical */
--sky:     #38BDF8   /* Information */
--slate-text: #94A3B8 /* Body text */
--foreground: #F8FAFC /* Headings */
```

**CSS classes available:**
- `.aayam-card` — primary glass card
- `.aayam-card-secondary` — lighter inner card
- `.badge` + `.badge-emerald` / `.badge-rose` / `.badge-amber` etc.
- `.section-heading` — styled `h3`

---

## 🚀 Running the Application

```bash
# Start the Streamlit development server
streamlit run app.py

# It will open at: http://localhost:8501
```

**Multi-page navigation** is automatic — Streamlit discovers all files in `pages/` by filename prefix order (1_, 2_, 3_ ...).

---

## 🐙 Git Workflow for 4-Member Collaboration

### Branch Naming Convention
```
feat/member1-economy-twin
feat/member2-cyberdrishti-rules
feat/member3-opportunity-catalogue
feat/member4-ui-improvements
```

### Merge Policy
- All PRs require 1 reviewer approval before merging to `main`
- Run `python -m pytest tests/` before opening any PR
- Never push directly to `main`

### Commit Format
```
[M1] Add inflation stress-test scenario to ArthSim
[M2] Expand CERT-In advisory dataset with Q1 2025 entries
[M3] Add EV sector opportunity pathways
[M4] Fix dark mode card border on mobile viewport
```

---

## 📦 Deployment (Streamlit Community Cloud — Free)

1. Push the repo to GitHub (public or private)
2. Log in at https://share.streamlit.io
3. Set **Main file path:** `app.py`
4. Set **Python version:** `3.12` (per `runtime.txt`)
5. No secrets required — all data is local CSVs

> **Important:** Ensure `data/processed/` directory and all CSV files are committed to the repo. Streamlit Cloud clones the full repo.

---

## 🔧 Extension Areas
1. **Mobile responsiveness:** Add `st.columns([1])` fallback for small screens
2. **Page transition animations:** CSS `@keyframes` for card entrance
3. **Export to PDF:** Add `streamlit-pdf` or a download button with `reportlab` for each module
4. **User settings persistence:** Replace `st.session_state` with a lightweight JSON file or SQLite for cross-session persistence
5. **Deployment to Hugging Face Spaces:** Alternative to Streamlit Cloud with GPU access if ML models are added

---

## ⚠️ Known Limitations
- `st.switch_page()` requires Streamlit ≥ 1.26; check if deployment target matches
- Session state resets on browser refresh — user profile must be re-entered each session
- Plotly charts are interactive client-side; no server-side rendering
- `unsafe_allow_html=True` is required for the custom CSS theme — this is intentional and safe for local/controlled deployment

---

## 📋 Dependency Manifest (`requirements.txt`)
```
streamlit>=1.28
pandas>=2.0
plotly>=5.18
networkx>=3.2
openpyxl>=3.1
scikit-learn>=1.3
pytest>=7.4
```

Update this file whenever you add a new `import` in the codebase.
