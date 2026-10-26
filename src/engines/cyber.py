"""
AAYAM - CyberDrishti: Explainable Cybersecurity Intelligence Engine
Implements canonical contract:
    assess_cyber_risk(text: str, context: dict | None = None) -> dict
Provides deterministic, explainable screening for phishing, deceptive payment prompts,
malicious APKs, digital arrest impersonation, and credential traps.
"""
import re
from src.utils.logging_config import logger


# Pattern Dictionary with standardized reason codes and severity weights
SUSPICIOUS_RULES = [
    {
        "code": "DIGITAL_ARREST_IMPERSONATION",
        "category": "Extortion / Impersonation",
        "weight": 35,
        "keywords": [
            r"digital arrest", r"cbi officer", r"narcotics parcel", r"ed summons",
            r"cyber crime branch", r"police warrant", r"court verification account",
            r"skype interrogation", r"customs seized"
        ],
        "explanation": "High-severity impersonation of central investigative agencies or police demanding funds to avoid arrest."
    },
    {
        "code": "REMOTE_ACCESS_TOOL_PROMPT",
        "category": "Device Takeover",
        "weight": 30,
        "keywords": [
            r"anydesk", r"rustdesk", r"teamviewer", r"quicksupport",
            r"share screen", r"9 digit code", r"install screen app", r"customer support will connect"
        ],
        "explanation": "Request to install remote screen-sharing software, enabling full observation and takeover of banking apps."
    },
    {
        "code": "REVERSE_UPI_QR_SCAM",
        "category": "Payment Fraud",
        "weight": 25,
        "keywords": [
            r"enter upi pin to receive", r"scan qr to get money", r"scan to receive payment",
            r"collect request approved", r"pin dalte hi paise milenge", r"enter pin for credit"
        ],
        "explanation": "Deceptive payment manipulation: Entering a UPI PIN always debits funds from the payer, never credits them."
    },
    {
        "code": "MALICIOUS_APK_DELIVERY",
        "category": "Malware / APK",
        "weight": 25,
        "keywords": [
            r"\.apk", r"install app from link", r"download bill app",
            r"bijli vibhag apk", r"electricity app", r"update app via whatsapp"
        ],
        "explanation": "Distribution of untrusted Android APK files capable of intercepting SMS OTPs and reading screen contents."
    },
    {
        "code": "CREDENTIAL_OTP_HARVESTING",
        "category": "Credential Theft",
        "weight": 25,
        "keywords": [
            r"share otp", r"send 6 digit code", r"verify your password",
            r"card number and cvv", r"netbanking login", r"pin share karein"
        ],
        "explanation": "Solicitation of multi-factor authentication secrets (OTPs, PINs, CVVs), violating fundamental banking security protocols."
    },
    {
        "code": "URGENT_DISCONNECTION_THREAT",
        "category": "Social Engineering",
        "weight": 20,
        "keywords": [
            r"power cut tonight", r"electricity disconnected", r"bijli cut",
            r"within 2 hours", r"account blocked today", r"kyc expiring today",
            r"immediate action required", r"sim card will be deactivated"
        ],
        "explanation": "Manufactured artificial urgency designed to bypass critical thinking and provoke panicked compliance."
    },
    {
        "code": "TASK_BASED_WORK_FROM_HOME_SCAM",
        "category": "Employment Fraud",
        "weight": 20,
        "keywords": [
            r"part time job", r"earn 3000.*daily", r"like youtube videos",
            r"rate hotels.*earn", r"telegram task", r"prepaid task", r"deposit to unlock commission"
        ],
        "explanation": "Prepaid task scheme masquerading as legitimate part-time employment, requiring upfront deposits to release phantom earnings."
    },
    {
        "code": "UNTRUSTED_SHORTENED_URL",
        "category": "Phishing Link",
        "weight": 15,
        "keywords": [
            r"bit\.ly", r"tinyurl\.com", r"is\.gd", r"cutt\.ly", r"t\.co",
            r"http://(?!(www\.)?[a-zA-Z0-9-]+\.(gov\.in|nic\.in|rbi\.org\.in|npci\.org\.in))"
        ],
        "explanation": "Shortened or non-HTTPS hyperlink concealing destination domain, frequently used to disguise credential harvesting portals."
    },
    {
        "code": "KYC_DOCUMENT_EXPIRY_PHISHING",
        "category": "Credential Theft / KYC",
        "weight": 25,
        "keywords": [
            r"kyc.*expired", r"update.*aadhaar.*pan", r"pan card block",
            r"sim card block.*kyc", r"kyc update link", r"turant kyc karein",
            r"kyc verify karein"
        ],
        "explanation": "Fake regulatory KYC update notice threatening immediate blockage of bank account or SIM card unless credentials or documents are submitted."
    },
    {
        "code": "LOTTERY_PRIZE_IMPERSONATION",
        "category": "Advance Fee Fraud",
        "weight": 25,
        "keywords": [
            r"kbc lottery", r"winner.*crore", r"lucky draw winner",
            r"claim your prize", r"pay processing fee.*lottery", r"paise jeete hain",
            r"lottery number.*win"
        ],
        "explanation": "Advance-fee lottery or prize deception demanding an upfront tax or processing charge to release non-existent jackpot funds."
    },
    {
        "code": "FAKE_RBI_COURT_FREEZE_NOTICE",
        "category": "Legal Extortion",
        "weight": 30,
        "keywords": [
            r"rbi.*freeze.*account", r"anti money laundering.*notice",
            r"financial crime investigation", r"supreme court order.*freeze",
            r"khata freeze ho gaya", r"rbi audit notice"
        ],
        "explanation": "Fraudulent regulatory or judicial freeze threat coercing victims into transferring funds into external verification accounts."
    },
    {
        "code": "INCOME_TAX_REFUND_SCAM",
        "category": "Tax Phishing",
        "weight": 20,
        "keywords": [
            r"tax refund.*approved", r"income tax refund.*rs", r"click to claim refund",
            r"itr.*refund.*pending", r"claim refund link", r"tax return credit"
        ],
        "explanation": "Deceptive tax refund notification urging users to click malicious hyperlinks or submit banking login details to receive phantom refunds."
    },
    {
        "code": "TRAI_SANCHAR_SAATHI_SPOOF",
        "category": "Authority Impersonation",
        "weight": 25,
        "keywords": [
            r"trai.*mobile disconnection", r"dot.*deactivate.*mobile",
            r"department of telecommunications.*disconnect", r"sanchar saathi.*violation",
            r"sim band ho jayegi", r"telecom department notice"
        ],
        "explanation": "Impersonation of telecom regulator (TRAI/DoT) falsely claiming mobile numbers are linked to illegal activities and face instant disconnection."
    }
]


def assess_cyber_risk(text: str, context: dict | None = None) -> dict:
    """
    Scan text content (SMS, message, WhatsApp text, email) for cyber-financial threat patterns.
    
    Args:
        text: The suspicious message or communication string.
        context: Optional contextual parameters (e.g. sender, channel, medium).
        
    Returns:
        dict: Standardized assessment including score, level, matched rules, and actionable mitigations.
    """
    if not text or not isinstance(text, str):
        return {
            "risk_score": 0.0,
            "risk_level": "Minimal Risk",
            "is_suspicious": False,
            "triggered_patterns": [],
            "reason_codes": [],
            "attack_chain_stage": "None",
            "safety_guidance": ["No text provided for analysis."],
            "disclaimer": "CyberDrishti provides deterministic heuristic indicators for educational screening."
        }
        
    lowered = text.lower()
    raw_score = 0
    triggered = []
    reason_codes = []
    
    for rule in SUSPICIOUS_RULES:
        matched_keywords = []
        for kw_pattern in rule["keywords"]:
            if re.search(kw_pattern, lowered, re.IGNORECASE):
                matched_keywords.append(kw_pattern)
                
        if matched_keywords:
            raw_score += rule["weight"]
            reason_codes.append(rule["code"])
            triggered.append({
                "code": rule["code"],
                "category": rule["category"],
                "severity_points": rule["weight"],
                "explanation": rule["explanation"],
                "matched_terms": matched_keywords[:3]
            })
            
    # Normalize score to 0 - 100
    risk_score = min(100.0, float(raw_score))
    
    # Risk Level Categorization
    if risk_score >= 60.0:
        risk_level = "Critical Threat"
        is_suspicious = True
        chain_stage = "Active Exploitation / Financial Exfiltration"
    elif risk_score >= 35.0:
        risk_level = "High Suspicion"
        is_suspicious = True
        chain_stage = "Credential & Access Harvesting"
    elif risk_score >= 15.0:
        risk_level = "Moderate Caution"
        is_suspicious = True
        chain_stage = "Social Engineering / Initial Lure"
    else:
        risk_level = "Low Risk"
        is_suspicious = False
        chain_stage = "No Malicious Chain Detected"
        
    # Compile incident-specific safety guidance
    guidance = []
    if "DIGITAL_ARREST_IMPERSONATION" in reason_codes:
        guidance.append("DISCONNECT IMMEDIATELY: Indian government agencies, police, and CBI never arrest citizens via video calls or ask for funds.")
        guidance.append("File an emergency report immediately on the National Cyber Crime Portal (cybercrime.gov.in) or call 1930.")
        
    if "REMOTE_ACCESS_TOOL_PROMPT" in reason_codes:
        guidance.append("NEVER share 9-digit codes or install AnyDesk/TeamViewer at the request of an incoming caller.")
        guidance.append("If installed, immediately enable Airplane Mode and uninstall the remote desktop application.")
        
    if "REVERSE_UPI_QR_SCAM" in reason_codes:
        guidance.append("GOLDEN UPI RULE: Entering UPI PIN is strictly for DEDUCTING money from your account, never for receiving money.")
        guidance.append("Decline the collect request inside your UPI app (Google Pay, PhonePe, Paytm, BHIM).")
        
    if "MALICIOUS_APK_DELIVERY" in reason_codes:
        guidance.append("DO NOT TAP or download any .apk attachment sent via SMS, WhatsApp, or Telegram.")
        guidance.append("Only install mobile banking applications verified through Google Play Store or Apple App Store.")
        
    if "CREDENTIAL_OTP_HARVESTING" in reason_codes:
        guidance.append("NEVER disclose 4 or 6-digit SMS OTPs, UPI PINs, or card CVVs to anyone under any pretext.")
        
    # 4-Pillar Threat Matrix (0 - 100% per pillar)
    urgency_score = min(100, int(sum(t["severity_points"] * 3.5 for t in triggered if t["code"] in ["URGENT_DISCONNECTION_THREAT"])))
    financial_score = min(100, int(sum(t["severity_points"] * 2.8 for t in triggered if t["code"] in ["REVERSE_UPI_QR_SCAM", "TASK_BASED_WORK_FROM_HOME_SCAM", "INCOME_TAX_REFUND_SCAM"])))
    authority_score = min(100, int(sum(t["severity_points"] * 2.8 for t in triggered if t["code"] in ["DIGITAL_ARREST_IMPERSONATION", "TRAI_SANCHAR_SAATHI_SPOOF", "KYC_DOCUMENT_EXPIRY_PHISHING"])))
    payload_score = min(100, int(sum(t["severity_points"] * 2.8 for t in triggered if t["code"] in ["MALICIOUS_APK_DELIVERY", "REMOTE_ACCESS_TOOL_PROMPT", "CREDENTIAL_OTP_HARVESTING", "UNTRUSTED_SHORTENED_URL"])))

    is_benign_banking = bool(re.search(r"(credited|debited|available balance|otp for logging|bank never calls|txn successful)", lowered))
    
    # Verdict determinations
    if risk_score >= 60.0:
        verdict = "CRITICAL_THREAT"
        verdict_title = "CRITICAL THREAT / DANGEROUS SCAM"
        verdict_badge = "rose"
        primary_threat = triggered[0]["category"] if triggered else "Severe Extortion Scam"
        summary_explanation = f"Critical threat detected: Communication exhibits {primary_threat} indicators. High risk of financial loss."
    elif risk_score >= 35.0:
        verdict = "HIGH_SUSPICION"
        verdict_title = "HIGH SUSPICION / LIKELY SCAM"
        verdict_badge = "amber"
        primary_threat = triggered[0]["category"] if triggered else "Deceptive Phishing Attempt"
        summary_explanation = f"Suspicious communication: Multiple red flags identified ({primary_threat}). Strong probability of fraud."
    elif risk_score >= 15.0:
        verdict = "MODERATE_CAUTION"
        verdict_title = "MODERATE CAUTION / SUSPICIOUS"
        verdict_badge = "amber"
        primary_threat = triggered[0]["category"] if triggered else "Unverified Communication"
        summary_explanation = "Moderate caution advised: Contains artificial urgency or unverified links. Verify sender independently."
    else:
        verdict = "SAFE_BENIGN"
        verdict_title = "VERIFIED SAFE / BENIGN NOTIFICATION" if is_benign_banking else "NO THREAT DETECTED"
        verdict_badge = "emerald"
        primary_threat = "Legitimate Banking / Safe Message" if is_benign_banking else "Normal Communication"
        summary_explanation = "No known attack patterns, extortion triggers, or malicious URLs were found in this text. Message appears safe."

    triggered_flags = [f"{t['category']}: {t['explanation']}" for t in triggered]
    recommended_action = guidance[0] if guidance else "Standard digital hygiene: Do not share OTPs or banking PINs with anyone."

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "is_suspicious": is_suspicious,
        "triggered_patterns": triggered,
        "reason_codes": reason_codes,
        "attack_chain_stage": chain_stage,
        "safety_guidance": guidance,
        "disclaimer": "CyberDrishti is an explainable heuristic security screening tool for educational resilience. It is not an antivirus or warranty of digital safety.",
        "threat_matrix": {
            "urgency_coercion": urgency_score,
            "financial_trigger": financial_score,
            "authority_impersonation": authority_score,
            "technical_payload": payload_score
        },
        "verdict": verdict,
        "verdict_title": verdict_title,
        "verdict_badge": verdict_badge,
        "risk_badge": verdict_badge,
        "primary_threat_vector": primary_threat,
        "summary_explanation": summary_explanation,
        "triggered_flags": triggered_flags,
        "recommended_action": recommended_action
    }
