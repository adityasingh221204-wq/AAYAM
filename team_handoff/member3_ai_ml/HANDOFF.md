# AAYAM — Team Handoff: Member 3 — AI/ML & Opportunity Intelligence

## 🎯 Your Ownership Domain
You own everything related to **career opportunity ranking, multi-factor recommendation scoring, and the India macroeconomic intelligence layer**.

---

## 📁 Files You Own

| File | Purpose |
|---|---|
| `src/engines/recommendations.py` | `rank_opportunities()` — explainable multi-factor scoring |
| `data/processed/opportunities/opportunity_catalogue.csv` | Curated 8-pathway opportunity dataset |
| `data/processed/opportunities/opportunity_catalogue.json` | JSON variant |
| `pages/3_Opportunity_Pathways.py` | Ranked pathway explorer UI |
| `pages/6_India_Intelligence.py` | Macro analytics and payment trends page |
| `tests/test_recommendations_recovery_loaders.py` | Recommendations engine tests (partial ownership) |

---

## 🔑 Key Contracts You Must Maintain

### `rank_opportunities(profile: dict, opportunities: list[dict]) -> list[dict]`

**Input profile keys used:**
- `education` (str): e.g. `"Higher Secondary (12th)"`
- `skills` (list[str] or comma-separated str)
- `current_savings` (float)
- `monthly_take_home_income` (float)

**Each opportunity dict required keys:**
- `opportunity_id`, `title`, `required_skills` (comma-sep str)
- `required_education`, `estimated_monthly_income_min_inr`, `estimated_monthly_income_max_inr`
- `capital_required_inr`, `training_cost_inr`

**Output:** Sorted list (descending `match_score_pct`), each entry adds:
```python
{
  "match_score_pct": float,        # 0.0 – 100.0
  "fit_tier": str,                 # "High Alignment" | "Moderate Alignment" | "Development Opportunity"
  "matched_skills": list[str],
  "missing_skills": list[str],
  "affordability_status": str,
  "total_upfront_cost_inr": float,
  "projected_monthly_uplift_inr": float,
  "score_breakdown": dict,         # skills/affordability/education/uplift sub-scores
  "transparent_reasons": list[str] # 4-item human-readable justification
}
```

---

## 📊 Scoring Architecture

| Factor | Max Points | Logic |
|---|---|---|
| Skill Match | 40 pts | `matched_skills / required_skills` ratio × 40 |
| Financial Affordability | 25 pts | Savings vs total upfront cost; Mudra loan eligibility at 25% margin |
| Education Prerequisite | 15 pts | EDUCATION_LEVELS hierarchy comparison |
| Income Uplift Potential | 20 pts | `(midpoint - current_income) / current_income` scaled |
| **Total** | **100 pts** | |

**Education hierarchy** (`EDUCATION_LEVELS` in recommendations.py):
```
none(0) < primary(1) < secondary 10th(2) < higher secondary 12th/ITI(3) < diploma(4) < graduate(5) < B.Tech(6) < PG(7)
```

---

## 📋 Current Opportunity Catalogue (8 Pathways)

| ID | Title | Track | Sector |
|---|---|---|---|
| OPP-EMP-001 | Data Analytics & BI Analyst | Employment | Technology |
| OPP-EMP-002 | Cybersecurity Operations Analyst | Employment | Cybersecurity |
| OPP-EMP-003 | Banking Correspondent (BC Agent) | Employment | Financial Services |
| OPP-ENT-004 | CSC / Digital Seva Kendra | Enterprise | Digital Services |
| OPP-ENT-005 | Solar Rooftop Installation Technician | Enterprise | Renewable Energy |
| OPP-ENT-006 | Agri Value Addition Micro-Enterprise | Enterprise | Agriculture |
| OPP-EMP-007 | EV Technician & Battery Diagnostics | Employment | Electric Vehicles |
| OPP-EMP-008 | Accounts & Payroll Executive | Employment | Finance |

---

## 🧪 Running Your Tests
```bash
python -m pytest tests/test_recommendations_recovery_loaders.py::TestRankOpportunitiesStructure tests/test_recommendations_recovery_loaders.py::TestRankOpportunitiesScoring -v
```

---

## 🔧 Extension Areas
1. **Expand opportunity catalogue:** Add new rows to `opportunity_catalogue.csv`. Must include all 15 columns (see existing schema).
2. **PMKVY 4.0 linkage:** Cross-reference NSDC sector skill council job roles with catalogue entries via `scheme_linkage` column
3. **Geographic filtering:** Add location-aware filtering using `location_type` (Urban / Rural / Both) and `data/reference/geography_mapping.csv`
4. **ML-based matching:** Replace the deterministic score with a learned ranking model once sufficient user interaction data is available
5. **Nudge integration:** Surface "1 skill gap to unlock High Alignment" prompts when a user is 1–2 skills away from a top pathway

---

## ⚠️ Known Limitations
- Salary ranges are indicative based on public job portals and government scheme documents — not guaranteed
- Skill matching is exact string match (case-insensitive); does not understand synonyms yet (e.g., "Python" ≠ "Python 3")
- No live job listing integration; catalogue is static
- Mudra loan eligibility assumes standard 10–25% margin money requirement; actual bank discretion varies
