<div align="center">

# 🛡️ AAYAM
### **Adaptive AI for Yojana, Awareness & Market-resilience**

*A high-trust, multi-engine cyber-fintech intelligence platform built for India's digital citizen*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?logo=vercel&style=for-the-badge)](https://aayam.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&style=for-the-badge)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&style=for-the-badge)](https://flask.palletsprojects.com)
[![Tests](https://img.shields.io/badge/Tests-130%20Passing-brightgreen?style=for-the-badge)](tests/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

</div>

---

## 📖 What is AAYAM?

**AAYAM** is a premium, open-source AI-powered intelligence platform that helps everyday Indian citizens — especially those with limited financial literacy — protect themselves from digital fraud, understand their economic resilience, simulate financial shocks, and access government-backed recovery pathways.

Built on **100% verified institutional datasets** (RBI, NPCI, MHA, MoSPI, MSDE, PMMY, DoT), AAYAM is designed to be:

- 🔒 **Zero hallucination** — every figure anchored to official government bulletins
- ⚡ **Real-time** — live calculations, simulations, and threat analysis
- 🎓 **Explainable** — plain-English outputs any citizen can understand
- 🌐 **Deployable** — runs on Vercel in one click

---

## 🏗️ System Architecture

```
AAYAM/
├── api/                        ← Vercel Serverless Entry Point
│   └── index.py                ← WSGI bridge (Flask ↔ Vercel)
│
├── web/                        ← Web Application Layer
│   ├── server.py               ← Flask REST API Server (14 routes + 8 API endpoints)
│   ├── templates/              ← 14 HTML Pages (ultra-premium CSS+JS)
│   │   ├── index.html          ← Landing Hub + Citizen Journey
│   │   ├── command.html        ← Systemic Command Centre
│   │   ├── twin.html           ← Economic Digital Twin
│   │   ├── cyberdrishti.html   ← CyberDrishti Threat Screener
│   │   ├── arthsim.html        ← ArthSim Monte Carlo Simulator
│   │   ├── opportunities.html  ← PMKVY/Mudra Opportunity Pathways
│   │   ├── intelligence.html   ← India Macro & Cyber Intelligence
│   │   ├── trustgraph.html     ← Trust Graph Threat Architecture
│   │   ├── recovery.html       ← 1930 Recovery Centre & Playbooks
│   │   ├── defense.html        ← Report & Architecture Portal
│   │   ├── models.html         ← Live Model Code Playground
│   │   ├── guide.html          ← Citizen How-To Guide
│   │   └── disclaimer.html     ← Ethical Guardrails & Warning
│   └── static/
│       ├── css/style.css       ← Cyber-violet ultra-premium design system
│       └── js/app.js           ← Live calculators, simulators, screeners
│
├── src/                        ← Core Engine Layer
│   ├── engines/
│   │   ├── economy.py          ← Financial Resilience Scorer (DTI, runway, surplus)
│   │   ├── cyber.py            ← 4-Pillar Heuristic Threat Matrix
│   │   ├── simulator.py        ← Monte Carlo Shock Trajectory Engine
│   │   ├── recommendations.py  ← PMKVY/Mudra Opportunity Ranker
│   │   └── recovery.py         ← 1930 Incident Response Playbook Generator
│   ├── data/
│   │   ├── loaders.py          ← Unified dataset loader (8 official datasets)
│   │   └── validators.py       ← Input schema validator
│   └── utils/
│       └── logging_config.py   ← Structured logging
│
├── data/
│   ├── processed/              ← Cleaned CSV datasets (8 official sources)
│   │   ├── rbi/                ← RBI Payment System Indicators (Feb 2025)
│   │   ├── npci/               ← NPCI UPI Ecosystem (Feb 2025)
│   │   ├── mha/                ← MHA NCRP Cybercrime State Data (2024)
│   │   ├── mospi/              ← PLFS Labour Force Survey (2023-24)
│   │   ├── msde/               ← PMKVY 4.0 Job Roles Catalogue
│   │   └── pmmy/               ← Mudra Yojana Loan Rules
│   └── raw/                    ← Original government files
│
├── tests/                      ← 130 Unit Tests (100% passing)
│   ├── conftest.py             ← Shared pytest fixtures
│   ├── test_economy_engine.py
│   ├── test_cyber_engine.py
│   ├── test_simulator_engine.py
│   └── test_recommendations_recovery_loaders.py
│
├── docs/
│   ├── ARCHITECTURE.md         ← Technical architecture deep-dive
│   └── HANDOFF.md              ← Team collaboration documentation
│
├── vercel.json                 ← Vercel deployment configuration
├── requirements.txt            ← Python dependencies
├── runtime.txt                 ← Python 3.12 runtime
└── README.md                   ← This file
```

---

## 🚀 Pages & Modules

| Route | Page | Engine | What It Does |
|:------|:-----|:-------|:-------------|
| `/` | **Landing Hub** | All engines | Scam detector, Financial gauge, 4-Step Citizen Journey |
| `/command` | **Command Centre** | Economy + Cyber | Live system health, quick threat triage, resilience dashboard |
| `/twin` | **Economic Digital Twin** | Economy Engine | Real-time DTI, savings runway, resilience score from income/expense sliders |
| `/cyberdrishti` | **CyberDrishti Screener** | Cyber Engine | 4-pillar threat matrix: Urgency, Authority Spoof, Financial Lure, Malware Vector |
| `/arthsim` | **ArthSim Simulator** | Simulator Engine | Monte Carlo shock trajectory — job loss, cyber fraud, medical emergency, inflation |
| `/opportunities` | **Opportunity Pathways** | Recommender Engine | PMKVY 4.0 job roles, Mudra loan eligibility, skill gap analysis |
| `/intelligence` | **India Intelligence** | Data Layer | Live NPCI UPI telemetry, MHA 1930 state-wise fraud registers, provenance citations |
| `/trustgraph` | **Trust Graph** | Cyber + Graph | Scam network topology, attack vector mapping, trust score visualisation |
| `/recovery` | **1930 Recovery Centre** | Recovery Engine | Golden-hour countdown, incident playbooks, official escalation paths |
| `/defense` | **Report & Architecture** | All | Interactive technical architecture, pipeline animation, data provenance |
| `/models` | **Live Model Playground** | All | Real-time syntax-highlighted code, live JSON output, animated model execution |
| `/guide` | **Citizen Guide** | — | How to use each module, persona walkthroughs |
| `/disclaimer` | **Ethical Guardrails** | — | What AAYAM is NOT for, abuse warnings |

---

## 🧠 Five Core Engines

### 1. 🏦 Economy Engine (`src/engines/economy.py`)
Calculates a **Composite Resilience Score** (0–100) from household financial inputs:
- **Debt-to-Income Ratio (DTI)** — RBI benchmarked threshold
- **Emergency Fund Runway** — months household can survive with zero income
- **Monthly Net Surplus/Deficit** — operational cash flow health
- **Savings Velocity Score** — trajectory toward financial independence

### 2. 🔍 CyberDrishti Engine (`src/engines/cyber.py`)
Screens any text message through a **4-Pillar Heuristic Threat Matrix**:
- **Pillar 1 — Urgency & Coercion**: countdown timers, immediate threats (0–100)
- **Pillar 2 — Authority Impersonation**: CBI, RBI, TRAI, police, bank impersonation
- **Pillar 3 — Financial Lure/Loss**: QR codes, UPI PINs, reverse payments, lottery
- **Pillar 4 — Malware/Phishing Vector**: `.apk` links, screen-share requests, OTP harvesting
- Outputs: `risk_score`, `risk_level`, `primary_threat_vector`, `recommended_action`

### 3. ⚡ ArthSim Simulator (`src/engines/simulator.py`)
Runs **Monte Carlo financial shock simulations** over a configurable horizon (3–24 months):
- **Scenarios**: job loss, cyber fraud loss (₹50,000), medical emergency (₹75,000), inflation spike
- Computes month-by-month savings trajectory with depletion detection
- Outputs actionable guidance based on depletion timeline

### 4. 🚀 Opportunity Engine (`src/engines/recommendations.py`)
Ranks government-backed skill and credit opportunities against citizen profile:
- **PMKVY 4.0** job roles with NSQF certification levels
- **Pradhan Mantri Mudra Yojana** — Shishu (₹50k), Kishore (₹5L), Tarun (₹10L)
- Multi-factor ranking: education match, occupation fit, income gap, regional demand

### 5. 🆘 Recovery Engine (`src/engines/recovery.py`)
Generates structured **Golden-Hour incident response playbooks**:
- Categories: Unauthorized UPI, Digital Arrest, Malicious APK
- 3-step protocols with specific bank hotline numbers and escalation timelines
- Integrated 1930 cybercrime helpline references

---

## 📊 Data Provenance — 8 Verified Official Sources

| Dataset ID | Agency | Dataset | Coverage |
|:-----------|:-------|:--------|:---------|
| DS-RBI-PSI-2025-02 | Reserve Bank of India | Payment System Indicators | Feb 2025 |
| DS-NPCI-UPI-2025-02 | NPCI | UPI Ecosystem Statistics | Feb 2025 |
| DS-MHA-NCRP-2024 | Ministry of Home Affairs (I4C) | National Cybercrime Register | 2024 |
| DS-MOSPI-PLFS-2023-24 | MoSPI | Periodic Labour Force Survey | 2023–24 |
| DS-MSDE-PMKVY-2024 | MSDE | PMKVY 4.0 Job Roles | FY 2024-25 |
| DS-PMMY-MUDRA-2024 | MUDRA / DFS | Mudra Yojana Lending Rules | FY 2024-25 |
| DS-RBI-CPFIR-2024 | Reserve Bank of India | Payments Fraud Registry | FY 2023-24 |
| DS-DOT-TAFCOP-2024 | DoT Sanchar Saathi | SIM Analytics & Telecom | 2024 |

---

## 🖥️ Running Locally

### Prerequisites
- Python 3.12+
- pip

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/adityasingh221204-wq/AAYAM.git
cd AAYAM

# 2. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the web server
python web/server.py

# 5. Open in browser
# → http://localhost:5000
```

### Run Tests

```bash
python -m pytest tests/ -v
# Expected: 130 passed
```

---

## ☁️ Deploying to Vercel (3 Steps)

### Method 1: Vercel Dashboard (Recommended)

1. **Fork or clone** this repository to your GitHub account
2. **Go to [vercel.com](https://vercel.com)** → New Project → Import Git Repository
3. **Select your fork** of `AAYAM` → Vercel auto-detects `vercel.json` → click **Deploy**

That's it. Your live URL will be `https://your-project.vercel.app` within ~90 seconds.

### Method 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# From the project root:
vercel

# Follow prompts → select project → deploy
# For production:
vercel --prod
```

### Environment Variables (None Required)
AAYAM requires **zero API keys or secrets** — all computations are local and data-driven.

---

## 🧪 Test Coverage

```
tests/
├── test_economy_engine.py          (25 tests) — DTI, runway, resilience score edge cases
├── test_cyber_engine.py            (36 tests) — threat matrix, 4 pillars, keyword scoring
├── test_simulator_engine.py        (19 tests) — shock trajectories, depletion detection
└── test_recommendations_recovery_loaders.py (50 tests) — data loading, ranking, playbooks
                                    ─────────
                                    130 total  ✅ 100% passing
```

---

## 🎨 Design System

The UI is built with **vanilla CSS + JavaScript** — zero framework dependencies:

- **Color Palette**: Deep space black `#06070B` + cyber-violet `#9333EA` + electric cyan `#06B6D4`
- **Typography**: Syne (headings) + Inter (body) + Space Grotesk (code/mono)
- **Micro-animations**: Floating sidebar dock, cursor glow aura, glassmorphic cards, scroll-triggered reveals
- **Mobile Responsive**: Fully adaptive down to 360px viewport

---

## 👥 Team

| Member | Domain | Modules |
|:-------|:-------|:--------|
| **Aditya Singh** | FinTech & Economic Models | Economy Engine, ArthSim, Digital Twin, Data ETL |
| **Abhishek Shrivastava** | Cyber Security & Threat Intelligence | CyberDrishti Engine, Recovery Playbooks |
| **Aarushi S.** | AI/ML & Opportunity Intelligence | Recommender Engine, Intelligence Registers |
| **Ansh Saini** | UI/UX & Platform Architecture | Design System, Frontend, Trust Graph, System Health |

---

## ⚠️ Ethical Guardrails

AAYAM is built exclusively for **protective and educational purposes**:

- ✅ **IS FOR**: Identifying scam messages, understanding financial resilience, learning government recovery pathways
- ❌ **IS NOT FOR**: Bypassing security systems, evading law enforcement, financial advice, or any offensive cyber use

All outputs carry explicit uncertainty disclaimers. Citizens are always directed to official government portals (cybercrime.gov.in, rbi.org.in) for authoritative guidance.

See [`/disclaimer`](https://aayam.vercel.app/disclaimer) for the full Ethical Guardrails page.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ for India's Digital Citizens  
**AAYAM** — Protecting Every Rupee, Every Connection

[🌐 Live Demo](https://aayam.vercel.app) · [📖 Guide](https://aayam.vercel.app/guide) · [⚠️ Disclaimer](https://aayam.vercel.app/disclaimer)

</div>
