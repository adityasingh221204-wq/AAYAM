# AAYAM — Team Handoff: Member 1 — FinTech & Data Engineering

## 🎯 Your Ownership Domain
You own everything related to **economic data, financial modeling, and the personal Digital Twin engine**.

---

## 📁 Files You Own

| File | Purpose |
|---|---|
| `src/engines/economy.py` | Core financial indicator & resilience scoring engine |
| `src/engines/simulator.py` | ArthSim: deterministic multi-month scenario simulator |
| `src/data/loaders.py` | Canonical dataset loader contract |
| `src/data/validators.py` | Schema validation logic |
| `src/data/schemas.py` | Column schema definitions |
| `src/data/preprocessing.py` | ETL pre-processing helpers |
| `scripts/preprocess_datasets.py` | Full ETL pipeline script |
| `pages/2_Economic_Digital_Twin.py` | User-facing Digital Twin configuration page |
| `pages/5_ArthSim.py` | Scenario simulation page |
| `data/processed/rbi/` | RBI Payment System Indicators CSVs |
| `data/processed/plfs/` | PLFS 2023-24 Labour Force indicators |
| `data/processed/hces/` | HCES 2023-24 Consumption expenditure indicators |
| `data/processed/asuse/` | ASUSE 2023-24 Unincorporated enterprises indicators |
| `data/reference/source_register.csv` | Verified public data source registry |
| `tests/test_economy_engine.py` | Economy engine unit tests (37 tests) |
| `tests/test_simulator_engine.py` | ArthSim simulator unit tests (16 tests) |

---

## 🔑 Key Contracts You Must Maintain

### `calculate_financial_indicators(profile: dict) -> dict`
- **Input:** User profile dict (see `src/engines/economy.py` docstring for all keys)
- **Output:** Dict with resilience_score, emergency_fund_months, savings_rate_pct, risk_factors, recommendations, etc.
- **Never break:** All required keys must always be present in output, even with an empty/invalid profile

### `simulate_economic_scenario(profile: dict, scenario: dict) -> dict`
- **Input:** Profile dict + scenario dict (scenario_type, income_change_pct, lump_sum_loss_inr, duration_months)
- **Output:** baseline_trajectory, scenario_trajectory (list of dicts with month, income, expenses, net_cashflow, savings_balance)
- **Duration clamped:** Always 3–60 months

### `load_public_dataset(dataset_name: str) -> pd.DataFrame`
- **Always returns a DataFrame** (empty on error, never raises exceptions to the UI)
- Registered aliases (e.g. `"rbi"`, `"plfs"`, `"frauds"`) must continue to resolve

---

## 📊 Data Sources (All Public, All Free)

| Dataset | Source | File |
|---|---|---|
| Payment System Indicators | RBI (Feb 2025 Bulletin) | `data/processed/rbi/payment_systems_monthly.csv` |
| Domestic Payment Frauds | RBI CPFIR | `data/processed/rbi/domestic_payment_frauds.csv` |
| Labour Force (PLFS) | MoSPI 2023-24 | `data/processed/plfs/plfs_indicators_2023_24.csv` |
| Household Expenditure (HCES) | MoSPI 2023-24 | `data/processed/hces/hces_indicators_2023_24.csv` |
| Unincorporated Enterprises (ASUSE) | MoSPI 2023-24 | `data/processed/asuse/asuse_indicators_2023_24.csv` |

To re-run ETL: `python scripts/preprocess_datasets.py`

---

## 🧪 Running Your Tests
```bash
python -m pytest tests/test_economy_engine.py tests/test_simulator_engine.py -v
```
Expected: **53 tests, all passing**

---

## 🔧 Extension Areas
1. **Monthly RBI data update:** When RBI publishes a new bulletin, add the new rows to `payment_systems_monthly.csv` and re-run validators
2. **Resilience score v2:** Consider adding income stability factor (salaried vs. gig) as a new component
3. **PMKVY scheme linkage:** Attach government scheme IDs to financial gaps for better recommendation integration
4. **State-level PLFS disaggregation:** Currently uses All India aggregates; can be expanded to state-level with the full PLFS microdata

---

## ⚠️ Known Limitations
- Resilience score is **not** a credit score — emphasize this in any user-facing text
- Simulator uses **deterministic, zero-compounding** model; no stochastic Monte Carlo yet
- PLFS data is annual; monthly granularity not available from MoSPI
- RBI data manually extracted from bulletin; no public API available
