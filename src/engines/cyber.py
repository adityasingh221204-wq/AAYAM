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
        
    if not guidance:
        guidance.append("Verify unknown communications independently using contact numbers published on official provider portals.")
        guidance.append("Never click unverified links received from unknown senders.")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "is_suspicious": is_suspicious,
        "triggered_patterns": triggered,
        "reason_codes": reason_codes,
        "attack_chain_stage": chain_stage,
        "safety_guidance": guidance,
        "disclaimer": "CyberDrishti is an explainable heuristic security screening tool for educational resilience. It is not an antivirus or warranty of digital safety."
    }
