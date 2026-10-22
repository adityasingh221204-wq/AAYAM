# AAYAM — Architecture & Methodology

## System Overview

AAYAM follows a **strict layered architecture** separating data, business logic, and presentation concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  app.py (Home)  +  pages/1..8_*.py (Streamlit Multi-Page)  │
└──────────────────────┬──────────────────────────────────────┘
                       │ calls
┌──────────────────────▼──────────────────────────────────────┐
│                   UI COMPONENT LAYER                        │
│   src/ui/theme.py  |  components.py  |  charts.py           │
└──────────────────────┬──────────────────────────────────────┘
                       │ calls
┌──────────────────────▼──────────────────────────────────────┐
│                    ENGINE LAYER                             │
│  economy.py | cyber.py | recommendations.py                 │
│  simulator.py | recovery.py                                 │
└──────────────────────┬──────────────────────────────────────┘
                       │ calls
┌──────────────────────▼──────────────────────────────────────┐
│                     DATA LAYER                              │
│   src/data/loaders.py | validators.py | schemas.py          │
│   data/processed/**/*.csv  |  data/reference/*.csv          │
└─────────────────────────────────────────────────────────────┘
```

---

## Engine Methodology

### 1. Economic Digital Twin (`economy.py`)

**Composite Economic Resilience Score (0–100)**:

| Component | Max Points | Formula |
|---|---|---|
| Emergency Fund Runway | 35 pts | `min(35, (emergency_months / 6.0) * 35)` |
| Net Cash Flow Surplus | 30 pts | `min(30, (surplus / (0.20 × income)) × 30)` |
| Debt Burden Health | 25 pts | `25` at DTI ≤20%, linear decay to 0 at DTI >60% |
| Income Stability Base | 10 pts | `10` if income > 0, else `0` |

**Risk Classification:**
- ≥75 → High Resilience
- 50–74 → Moderate Resilience
- 30–49 → Financially Vulnerable
- <30 → Critical Stress

### 2. CyberDrishti Engine (`cyber.py`)

**Rule-based keyword pattern matching** (deterministic, explainable):

- Each rule has a `weight` (integer risk score contribution)
- Raw score = sum of triggered rule weights
- Final `risk_score` = `min(100, raw_score)`
- Thresholds: ≥60 Critical, ≥35 High, ≥15 Moderate, <15 Low

**Design principle:** Explainability over accuracy. Every triggered flag comes with a `code`, `explanation`, and `safety_guidance`. Users can verify the reason for any alert.

### 3. Opportunity Ranking Engine (`recommendations.py`)

**Multi-factor transparent ranking:**

```
match_score = skill_pts (max 40) 
            + affordability_pts (max 25) 
            + education_pts (max 15) 
            + income_uplift_pts (max 20)
```

Government micro-loan recognition: If user savings cover ≥25% of required capital, the opportunity is marked "Affordable via Mudra/PMEGP" (18/25 pts), reflecting RBI Mudra Yojana margin money norms.

### 4. ArthSim Simulator (`simulator.py`)

**Deterministic trajectory model:**
- Month-by-month cash flow simulation over 3–60 months
- Lump-sum loss applied at Month 0 (before Month 1)
- Optional partial income recovery modeled at `recovery_delay_months`
- Savings floor is 0 (cannot go negative)
- Conservative assumptions: no investment yield, no compounding inflation

### 5. Recovery Centre (`recovery.py`)

**Structured incident registry** with 5 canonical incident types mapped to prioritized action steps. Each step includes:
- Time priority tier (Immediate / Critical / Follow-up)
- Step-by-step instructions
- Official portal URL
- Evidence preservation checklist

---

## Data Pipeline

```
Raw Source (Excel/Web)
        │
        ▼
scripts/preprocess_datasets.py
        │
        ├─ PLFS data → data/processed/plfs/
        ├─ HCES data → data/processed/hces/
        ├─ ASUSE data → data/processed/asuse/
        ├─ RBI PSI data → data/processed/rbi/
        ├─ CERT-In advisories → data/processed/cyber_threats/
        ├─ Opportunity catalogue → data/processed/opportunities/
        └─ Source register → data/reference/
        │
        ▼
src/data/loaders.py  ──→  validate (validators.py)  ──→  pd.DataFrame
```

All CSVs are committed to the repository. No runtime network calls are made to external APIs.

---

## Transparency & Explainability Principles

1. **Every score has a visible formula.** No black-box scoring.
2. **Every recommendation shows its reasons.** The `transparent_reasons` list in opportunity ranking shows exact sub-scores.
3. **Every threat flag shows the matched pattern.** `matched_terms` and `explanation` are always surfaced in the UI.
4. **Every data point cites its source.** `render_data_provenance()` is required on all data-driven sections.
5. **Disclaimers are mandatory.** Every engine returns a `disclaimer` string; the UI surfaces it prominently.

---

## Limitations & Known Gaps

| Area | Limitation | Impact |
|---|---|---|
| Resilience Score | No credit bureau integration | Score is self-reported, not verified |
| CyberDrishti | Keyword-only (no NLP) | Sophisticated obfuscated threats not detected |
| Opportunity Salaries | Indicative ranges only | Actual wages vary by employer and location |
| RBI Data | Manual extraction, no live API | Data lags until next manual update |
| PLFS/HCES/ASUSE | Annual surveys only | No sub-annual granularity available |
| Simulator | No stochastic modeling | Doesn't reflect real-world uncertainty |
| Session State | Browser-session only | User profile not persisted across sessions |
