# AAYAM — Team Handoff: Member 2 — Cybersecurity & Threat Intelligence

## 🎯 Your Ownership Domain
You own everything related to **cyber threat detection, digital fraud intelligence, and the incident recovery playbook**.

---

## 📁 Files You Own

| File | Purpose |
|---|---|
| `src/engines/cyber.py` | CyberDrishti: explainable threat screening engine |
| `src/engines/recovery.py` | Recovery Centre: structured incident response playbook |
| `data/processed/cyber_threats/cert_in_advisories.csv` | CERT-In advisory dataset |
| `data/processed/cyber_threats/cert_in_advisories.json` | JSON variant for API use |
| `pages/4_CyberDrishti.py` | Live message screening UI page |
| `pages/7_Trust_Graph.py` | Threat relationship graph visualization |
| `pages/8_Recovery_Centre.py` | Incident response playbook page |
| `tests/test_cyber_engine.py` | CyberDrishti engine unit tests (38 tests) |

---

## 🔑 Key Contracts You Must Maintain

### `assess_cyber_risk(text: str, context: dict | None = None) -> dict`
**Required output keys:**
```python
{
  "risk_score": float,          # 0.0 – 100.0
  "risk_level": str,            # "Critical Threat" | "High Suspicion" | "Moderate Caution" | "Low Risk"
  "is_suspicious": bool,
  "triggered_patterns": list,   # Each item: {code, category, severity_points, explanation, matched_terms}
  "reason_codes": list[str],
  "attack_chain_stage": str,
  "safety_guidance": list[str],
  "disclaimer": str
}
```
- **Never raises exceptions** — always returns a valid dict, even for None/empty/non-string input

### `get_recovery_steps(incident_type: str) -> list[dict]`
**Required step keys:** `step_number`, `priority`, `action_title`, `instructions`, `official_portal_or_contact`, `evidence_to_preserve`

**Supported canonical types:**
- `suspicious_payment` (alias: `payment_fraud`, `upi_fraud`)
- `suspected_account_compromise` (alias: `account_compromise`, `takeover`)
- `suspected_phishing` (alias: `phishing`, `smishing`)
- `malicious_application_installation` (alias: `malicious_apk`, `apk`, `malware`)
- `identity_misuse` (alias: `sim_swap`, `esim`, `identity_theft`)

---

## 🧠 Threat Rule Architecture (`SUSPICIOUS_RULES` in `cyber.py`)

Each rule has:
- `code`: unique string ID
- `category`: human-readable threat category
- `weight`: integer contribution to risk score (scores sum and cap at 100)
- `keywords`: list of regex patterns (case-insensitive)
- `explanation`: public-facing explanation of the threat

**Current rule codes and weights:**

| Code | Category | Weight |
|---|---|---|
| `DIGITAL_ARREST_IMPERSONATION` | Extortion/Impersonation | 35 |
| `REMOTE_ACCESS_TOOL_PROMPT` | Device Takeover | 30 |
| `REVERSE_UPI_QR_SCAM` | Payment Fraud | 25 |
| `MALICIOUS_APK_DELIVERY` | Malware/APK | 25 |
| `CREDENTIAL_OTP_HARVESTING` | Credential Theft | 25 |
| `URGENT_DISCONNECTION_THREAT` | Social Engineering | 20 |
| `TASK_BASED_WORK_FROM_HOME_SCAM` | Employment Fraud | 20 |
| `UNTRUSTED_SHORTENED_URL` | Phishing Link | 15 |

---

## 🧪 Running Your Tests
```bash
python -m pytest tests/test_cyber_engine.py -v
```
Expected: **38 tests, all passing**

---

## 🔧 Extension Areas
1. **Add new threat patterns:** Add a new entry to `SUSPICIOUS_RULES` list in `cyber.py`. Follow the existing pattern structure exactly.
2. **Hindi/Hinglish expansion:** Add Devanagari-aware regex patterns for common fraud phrases in regional languages
3. **Trust Graph enrichment:** Add real-time CERT-In advisories to the `7_Trust_Graph.py` node data
4. **TRAI Chakshu integration:** When Chakshu API becomes public, integrate live spam number lookups

---

## ⚠️ Known Limitations
- Heuristic keyword detection only — **not** an ML classifier; no semantic understanding
- Will not detect sophisticated obfuscated threats (deliberate misspellings, Unicode substitution)
- CERT-In advisories are manually curated snapshots; not a live API feed
- Recovery steps are a best-effort educational playbook, not legal advice

---

## 📋 Official Reference Contacts (Verified)
| Resource | Contact |
|---|---|
| National Cyber Helpline | **1930** |
| Cyber Crime Portal | https://cybercrime.gov.in |
| CERT-In Incident Report | incident@cert-in.org.in |
| TRAI CHAKSHU Spam | https://sancharsaathi.gov.in/sfc/ |
| NPCI BHIM Helpline | 1800-120-1740 |
| UIDAI Aadhaar Lock | https://resident.uidai.gov.in |
