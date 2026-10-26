# Contributing to AAYAM

Thank you for contributing to **AAYAM** (*AI-Driven Multi-Dimensional Economic Mobility and Cyber-Financial Intelligence System*).

This document outlines team conventions, role responsibilities, branching strategies, commit standards, and testing procedures for collaborative development.

---

## 👥 1. Team Roles & Ownership Matrix

| Member | Role | Branch Name | Primary Files & Responsibilities |
|---|---|---|---|
| **Member 1** (Aditya Singh) | FinTech & Data Engineering | `feat/member1-fintech` | `src/engines/economy.py`, `src/engines/simulator.py`, `pages/2_Economic_Digital_Twin.py`, `pages/5_ArthSim.py`, RBI datasets, `tests/test_economy_engine.py`, `tests/test_simulator_engine.py` |
| **Member 2** (Abhishek Shrivastava) | Cybersecurity & Threat Intelligence | `feat/member2-cybersecurity` | `src/engines/cyber.py`, `src/engines/recovery.py`, `pages/4_CyberDrishti.py`, `pages/7_Trust_Graph.py`, `pages/8_Recovery_Centre.py`, CERT-In datasets, `tests/test_cyber_engine.py` |
| **Member 3** (Aarushi S.) | AI/ML & Opportunity Intelligence | `feat/aarushi-ai-ml` | `src/engines/recommendations.py`, `pages/3_Opportunity_Pathways.py`, `pages/6_India_Intelligence.py`, Opportunity Catalogue, `tests/test_recommendations_recovery_loaders.py` |
| **Member 4** (Ansh Saini) | UI / UX & Platform | `feat/member4-platform` | `app.py`, `pages/1_Command_Centre.py`, `src/ui/theme.py`, `src/ui/components.py`, `src/ui/charts.py`, `tests/conftest.py`, `tests/test_platform_ui.py`, `requirements.txt`, `CONTRIBUTING.md` |

---

## 🌿 2. Git Workflow Rules

> **CRITICAL RULE:** Never push or merge directly to `main`. All work must be conducted on dedicated feature branches.

### Step-by-Step Workflow:

1. **Pull Latest Main**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Branch from Main**:
   ```bash
   git checkout -b feat/member4-platform
   ```

3. **Stage and Commit Using Prefixes**:
   ```bash
   git add -A
   git commit -m "[M4] Add System Health telemetry and threat network chart"
   ```

4. **Verify Tests**:
   ```bash
   python -m pytest tests/ -v
   ```
   *Ensure all 148+ unit tests pass without errors or warnings.*

5. **Push and Open a Pull Request**:
   ```bash
   git push origin feat/member4-platform
   ```
   *Open a PR on GitHub targeted to `main` with detailed summary of changes.*

---

## 💬 3. Commit Message Convention

All commits must include the member prefix indicating domain ownership:

* `[M1]` — FinTech calculations, Digital Twin, ArthSim simulator, economy unit tests.
* `[M2]` — CyberDrishti rules, CERT-In advisories, Recovery Centre, cyber unit tests.
* `[M3]` — Opportunity pathways, ranking heuristics, government scheme linkages, macro analytics.
* `[M4]` — UI components, CSS design system, chart builders, platform telemetry, test fixtures.

**Examples:**
* `[M4] Implement plot_threat_network and unify knowledge graph visualization`
* `[M4] Add Command Centre System Health sidebar and inline Quick Threat Screen`
* `[M4] Create tests/conftest.py with standardized cross-module test fixtures`

---

## 🧪 4. Testing & Code Quality Standards

1. **Pytest Suite**:
   * All pull requests must pass the complete test suite:
     ```bash
     python -m pytest tests/ -v
     ```
   * Tests must be non-flaky and execute in under 5 seconds.
2. **Shared Fixtures**:
   * Use fixtures declared in `tests/conftest.py` (`demo_profile`, `healthy_profile`, `stressed_profile`, `base_scenario`, `sample_message_phishing`, `sample_opportunities`, etc.).
3. **Documentation**:
   * Every function must feature clear docstrings documenting `Args` and `Returns`.
4. **Data Provenance**:
   * Any component rendering government data must invoke `render_data_provenance()` with source title, publisher, reference period, and official URL.
5. **Legal & Ethical Disclaimers**:
   * All recommendations, credit scoring, or fraud screening interfaces must display clear educational disclaimers.

---

## 🚀 5. Local Development Commands

### Streamlit Multi-Page Application:
```bash
# Install dependencies
pip install -r requirements.txt

# Regenerate processed datasets (if raw files were updated)
python scripts/preprocess_datasets.py

# Launch Streamlit application
streamlit run app.py
```
App opens at: `http://localhost:8501`

### Modern Flask Web Server (Alternative Frontend & REST API):
```bash
python web/server.py
```
Server opens at: `http://localhost:5000`

---

## 📋 6. Pull Request Review Checklist

Before requesting review:
- [ ] Working branch is up-to-date with `main`.
- [ ] `python -m pytest tests/ -v` passes 100% (all 148+ unit tests passing).
- [ ] No temporary, scratch, or binary test dumps committed.
- [ ] Design system tokens (`apply_theme()`) applied consistently across all modified pages.
- [ ] Data provenance and academic prototype disclaimers remain visible.
- [ ] At least one other team member has reviewed and approved the pull request.
