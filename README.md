# AAYAM — Deliverables for Member 2 — Cybersecurity & Threat Intelligence

## 📦 What is inside this package
Expanded CyberDrishti with 5 new threat rules (KYC, KBC lottery, RBI freeze, Tax refund, TRAI spoof, Hindi/Hinglish detection), progress meter, pattern expanders, numbered safety checklist, 2025 CERT-In advisories, downloadable incident recovery checklist, and 35 passing unit tests.

### Included Files:
- `src/engines/cyber.py`
- `pages/4_CyberDrishti.py`
- `pages/7_Trust_Graph.py`
- `pages/8_Recovery_Centre.py`
- `data/processed/cyber_threats/cert_in_advisories.csv`
- `data/processed/cyber_threats/cert_in_advisories.json`
- `tests/test_cyber_engine.py`

---

## 🚀 How to Apply and Push to GitHub

### Method A — One-Click Script (Windows)
Double-click `apply_and_push.bat` (or run `./apply_and_push.ps1` in PowerShell).
It will automatically create your branch, stage the files, commit with your prefix, and push to GitHub!

### Method B — Manual Git Terminal Commands
Open your terminal in the root of your cloned `AAYAM` repository and run:

```bash
# 1. Ensure you are on the latest main
git checkout main
git pull origin main

# 2. Extract this ZIP into your AAYAM directory (overwrite matching files)

# 3. Create and switch to your feature branch
git checkout -b feat/member2-cybersecurity

# 4. Verify tests pass
python -m pytest tests/

# 5. Stage and commit your changes
git add -A
git commit -m "[M2] Implement module features, UI components, datasets, and tests"

# 6. Push to your branch on GitHub
git push -u origin feat/member2-cybersecurity

# 7. Open a Pull Request on GitHub:
# Go to https://github.com/adityasingh221204-wq/AAYAM
# Click "Compare & pull request" for feat/member2-cybersecurity -> main
```
