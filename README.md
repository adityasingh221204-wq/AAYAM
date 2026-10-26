# AAYAM
## AI-Driven Multi-Dimensional Economic Mobility and Cyber-Financial Intelligence System

> **A student decision-support prototype** — not financial advice, not a credit rating system, not an official government portal.

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io)
[![Tests](https://img.shields.io/badge/Tests-148%20passing-brightgreen)](#testing)
[![Data](https://img.shields.io/badge/Data-Public%20%26%20Verified-orange)](#data-sources)
[![SDG](https://img.shields.io/badge/SDG-1%20%7C%208%20%7C%2016-purple)](https://sdgs.un.org/goals)

---

## 🎯 What AAYAM Does

AAYAM is an integrated eight-module decision-support platform built for low-to-middle income individuals in India. It combines:

| Module | Function |
|---|---|
| **Command Centre** | Unified executive dashboard: personal KPIs + macro indicators + threat alerts + live system health telemetry |
| **Economic Digital Twin** | Build your personal financial twin; calculate resilience score, emergency runway, DTI |
| **Opportunity Pathways** | Transparently ranked career, upskilling, and micro-enterprise pathways |
| **CyberDrishti** | Explainable screening of suspicious messages, APK prompts, and UPI fraud patterns |
| **ArthSim** | What-if scenario simulator: income shock, fraud loss, inflation over 3–60 months |
| **India Intelligence** | RBI Payment Systems, PLFS, HCES, ASUSE macroeconomic analytics |
| **Trust Graph** | Interactive Plotly knowledge graph of cyber threat relationships and statutory defense frameworks |
| **Recovery Centre** | Step-by-step incident response playbook with verified official contacts |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+ installed
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/adityasingh221204-wq/AAYAM.git
cd AAYAM

# Install dependencies
pip install -r requirements.txt

# Initialise all processed datasets
python scripts/preprocess_datasets.py

# Launch the Streamlit application
streamlit run app.py
```

The app opens at **http://localhost:8501**

Alternative modern Flask web server & REST API:
```bash
python web/server.py
```
Opens at **http://localhost:5000**

---

## 🗂️ Project Structure

```
AAYAM/
├── app.py                          # Main Streamlit entry point
├── pages/                          # 8 multi-page modules + guide
│   ├── 0_System_Guide.py
│   ├── 1_Command_Centre.py
│   ├── 2_Economic_Digital_Twin.py
│   ├── 3_Opportunity_Pathways.py
│   ├── 4_CyberDrishti.py
│   ├── 5_ArthSim.py
│   ├── 6_India_Intelligence.py
│   ├── 7_Trust_Graph.py
│   └── 8_Recovery_Centre.py
├── src/
│   ├── engines/                    # Core processing engines
│   │   ├── economy.py              # Financial indicator & resilience engine
│   │   ├── cyber.py                # CyberDrishti threat screening engine
│   │   ├── recommendations.py      # Opportunity ranking engine
│   │   ├── simulator.py            # ArthSim scenario simulation engine
│   │   └── recovery.py             # Incident response playbook engine
│   ├── data/                       # Data layer
│   │   ├── loaders.py              # Canonical dataset loader
│   │   ├── validators.py           # Schema validators
│   │   ├── schemas.py              # Column schema definitions
│   │   └── preprocessing.py       # ETL helpers
│   ├── ui/                         # UI components
│   │   ├── theme.py                # Dark fintech CSS theme
│   │   ├── components.py           # Reusable widgets
│   │   └── charts.py               # Plotly chart builders & threat graph
│   └── utils/                      # Utilities
│       ├── config.py               # App constants
│       ├── formatting.py           # INR/% formatters
│       └── logging_config.py       # Centralized logger
├── data/
│   ├── processed/                  # Pre-processed CSVs (committed to repo)
│   │   ├── rbi/                    # RBI Payment System Indicators
│   │   ├── plfs/                   # Labour Force Survey
│   │   ├── hces/                   # Household Consumption Expenditure
│   │   ├── asuse/                  # Unincorporated Enterprises Survey
│   │   ├── cyber_threats/          # CERT-In advisories & state cyber fraud
│   │   └── opportunities/          # Opportunity catalogue (12 pathways)
│   ├── reference/                  # Source register & geography mapping
│   └── raw/                        # Raw source files
├── scripts/
│   └── preprocess_datasets.py      # Full ETL pipeline
├── tests/
│   ├── conftest.py                 # Unified cross-module test fixtures
│   ├── test_economy_engine.py      # Economy engine tests
│   ├── test_cyber_engine.py        # CyberDrishti tests
│   ├── test_simulator_engine.py    # ArthSim tests
│   ├── test_recommendations_recovery_loaders.py  # Recommendation/recovery/loader tests
│   └── test_platform_ui.py         # Platform, UI, and chart builder tests
├── web/                            # Modern Flask REST API & Web UI
│   ├── server.py                   # Flask server
│   ├── static/                     # CSS, JS, and image assets
│   └── templates/                  # Jinja2 HTML templates
├── docs/                           # Architecture and cross-team handoffs
│   ├── ARCHITECTURE.md
│   └── HANDOFF.md
├── CONTRIBUTING.md                 # Collaboration, branching & PR guidelines
├── TEAM_COLLABORATION.md           # Role allocations & sprint guide
├── requirements.txt
├── runtime.txt
└── .streamlit/config.toml
```

---

## 🧪 Testing

```bash
# Run the full test suite
python -m pytest tests/ -v

# Run individual module tests
python -m pytest tests/test_economy_engine.py -v
python -m pytest tests/test_cyber_engine.py -v
python -m pytest tests/test_simulator_engine.py -v
python -m pytest tests/test_recommendations_recovery_loaders.py -v
python -m pytest tests/test_platform_ui.py -v
```

**Current status: 148 tests — all passing (100% green)**

---

## 📊 Data Sources

All data used by AAYAM is **publicly available, non-personal, non-proprietary** official Indian government statistical data.

| Dataset | Source | Coverage | License |
|---|---|---|---|
| Payment System Indicators | Reserve Bank of India (RBI) | Feb 2025 Bulletin | Public domain |
| Domestic Payment Fraud (CPFIR) | Reserve Bank of India (RBI) | Sept 2022–Feb 2025 | Public domain |
| Periodic Labour Force Survey (PLFS) | MoSPI | Annual 2023–24 | Open Government Data |
| Household Consumption Expenditure Survey (HCES) | MoSPI | 2023–24 | Open Government Data |
| Annual Survey of Unincorporated Sector Enterprises (ASUSE) | MoSPI | 2023–24 | Open Government Data |
| CERT-In Security Advisories | Ministry of Electronics & IT | 2024–25 | Public domain |
| Opportunity Catalogue | AAYAM compiled (NSDC/PMKVY/MoMSME sources) | 2024–25 (12 pathways) | CC BY-NC-SA |
| State Cybercrime Risk Telemetry | MHA / National Cybercrime Portal (1930) | 2024–25 | Public domain |
| NPCI UPI Ecosystem Telemetry | NPCI | 2024–25 | Public domain |

---

## 🛡️ SDG Alignment

| Goal | Contribution |
|---|---|
| **SDG 1 — No Poverty** | Economic resilience scoring and emergency fund guidance for low-income households |
| **SDG 8 — Decent Work** | Transparent opportunity pathway ranking linked to PMKVY 4.0 and government schemes |
| **SDG 16 — Peace & Justice** | Digital fraud detection and incident recovery supporting safe digital financial inclusion |

---

## ⚠️ Disclaimers

1. **Not financial advice.** AAYAM indicators are for educational decision-support modeling only.
2. **Not a credit score.** The Resilience Score has no regulatory standing.
3. **Not an official government portal.** Official helplines and portals are linked but AAYAM is independent.
4. **Not an antivirus.** CyberDrishti is a heuristic educational screening tool.
5. **Indicative salary ranges** in the opportunity catalogue are compiled from public sources and are not guaranteed.

---

## 👥 Team & Collaboration

See [CONTRIBUTING.md](CONTRIBUTING.md) and [TEAM_COLLABORATION.md](TEAM_COLLABORATION.md) for role-specific instructions.

| Role | Domain | Member Name | Branch |
|---|---|---|---|
| Member 1 | FinTech & Data Engineering | **Aditya Singh** | `feat/member1-fintech` |
| Member 2 | Cybersecurity & Threat Intelligence | **Abhishek Shrivastava** | `feat/member2-cybersecurity` |
| Member 3 | AI/ML & Opportunity Intelligence | **Aarushi S.** | `feat/aarushi-ai-ml` |
| Member 4 | UI / UX & Platform | **Ansh Saini** | `feat/member4-platform` |

---

## 📄 License

This project is submitted as an academic prototype. Data sources are credited under their respective public licenses. The compiled analysis and application code are released for educational use.
