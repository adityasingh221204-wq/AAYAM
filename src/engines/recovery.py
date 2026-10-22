"""
AAYAM - Recovery Centre Engine
Implements canonical contract:
    get_recovery_steps(incident_type: str) -> list[dict]
Provides prioritised, step-by-step incident recovery checklists, evidence preservation,
and verified official Indian escalation routes.
"""
from src.utils.logging_config import logger

INCIDENT_RECOVERY_REGISTRY = {
    "suspicious_payment": {
        "title": "Unauthorized Digital Payment or Fraudulent Debit",
        "steps": [
            {
                "step_number": 1,
                "priority": "Immediate (0 - 15 Mins)",
                "action_title": "Call 1930 & Freeze Transaction on Citizen Financial Cyber Fraud System",
                "instructions": "Immediately dial 1930 (National Cyber Financial Fraud Helpline). Provide your bank account name, victim UPI ID/card number, transaction ID (UTR), amount, and time of debit. The automated system alerts intermediary banks and payment gateways to freeze the stolen funds before cash-out.",
                "official_portal_or_contact": "Toll-free 1930 / https://cybercrime.gov.in",
                "evidence_to_preserve": "Debit SMS, bank notification screenshot, 12-digit UTR/UPI reference number, receiver UPI ID / account number."
            },
            {
                "step_number": 2,
                "priority": "Immediate (0 - 30 Mins)",
                "action_title": "Block Card / Net Banking via Official Bank Emergency Number",
                "instructions": "Open your official mobile banking app or call your bank's published 24x7 fraud helpline to hotlist the compromised debit/credit card or block UPI access on your account.",
                "official_portal_or_contact": "Bank official 24x7 customer care number (printed on reverse of card).",
                "evidence_to_preserve": "Complaint reference number and date/time of call with bank customer service representative."
            },
            {
                "step_number": 3,
                "priority": "Critical (Within 72 Hours)",
                "action_title": "Lodge Formal Written Dispute under RBI Zero Liability Guidelines",
                "instructions": "Submit a formal written fraud dispute form to your home bank branch. Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, if an unauthorized transaction is reported within three working days where fraud is due to third-party breach without customer fault, zero liability applies.",
                "official_portal_or_contact": "Home Bank Branch Grievance Redressal Officer / RBI Banking Ombudsman.",
                "evidence_to_preserve": "Stamped acknowledgement copy of written fraud dispute letter and bank account statement."
            },
            {
                "step_number": 4,
                "priority": "Follow-up (24 - 48 Hours)",
                "action_title": "File Formal Complaint on National Cyber Crime Portal",
                "instructions": "Visit https://cybercrime.gov.in and file a formal financial fraud report under 'Report Cyber Crime'. Upload transaction receipts and communication screenshots to generate an official Cyber Crime Acknowledgement Report (FIR/CSR).",
                "official_portal_or_contact": "https://cybercrime.gov.in",
                "evidence_to_preserve": "Official Complaint Acknowledgement Number (14-digit national cybercrime ID)."
            }
        ]
    },
    "suspected_account_compromise": {
        "title": "Suspected Bank, Email, or UPI Account Takeover",
        "steps": [
            {
                "step_number": 1,
                "priority": "Immediate (0 - 15 Mins)",
                "action_title": "Terminate Active Sessions & Reset Master Credentials",
                "instructions": "Log into your primary email and Google/Apple account from a known clean device. Use 'Sign out of all sessions' / 'Log out of other devices' and immediately change your master passwords.",
                "official_portal_or_contact": "Google Security Checkup / Apple ID Management / Microsoft Security.",
                "evidence_to_preserve": "Screenshots of unrecognized IP addresses, device types, or login locations."
            },
            {
                "step_number": 2,
                "priority": "Immediate (0 - 30 Mins)",
                "action_title": "Deregister & Re-link UPI Apps",
                "instructions": "Inside your UPI applications (BHIM, PhonePe, Google Pay), go to settings and select 'Deregister App' or 'Reset UPI PIN' using your physical debit card.",
                "official_portal_or_contact": "NPCI BHIM Customer Helpline 1800-120-1740.",
                "evidence_to_preserve": "Confirmation SMS of UPI PIN change and device deregistration."
            },
            {
                "step_number": 3,
                "priority": "Critical (1 - 2 Hours)",
                "action_title": "Enable Hardware-Backed or App-Based 2FA",
                "instructions": "Switch 2-factor authentication from SMS-based OTP to an authenticator application (Google Authenticator, Microsoft Authenticator) to prevent SIM-swap bypass.",
                "official_portal_or_contact": "Account security settings.",
                "evidence_to_preserve": "Generated recovery codes securely stored offline (never on cloud notes)."
            }
        ]
    },
    "suspected_phishing": {
        "title": "Suspected Phishing Link or Message Interaction",
        "steps": [
            {
                "step_number": 1,
                "priority": "Immediate (0 - 15 Mins)",
                "action_title": "Close Tab & Clear Browser Cached Secrets",
                "instructions": "Close the deceptive web page immediately. If you entered partial login details or personal numbers, clear browser cookies and history for that session immediately.",
                "official_portal_or_contact": "Browser Security Settings.",
                "evidence_to_preserve": "Screenshot of the phishing URL, sender phone number, and message text before clearing."
            },
            {
                "step_number": 2,
                "priority": "Immediate (0 - 30 Mins)",
                "action_title": "Change Password for Affected Accounts",
                "instructions": "If you entered passwords or credentials on the deceptive page, change the passwords of those actual accounts immediately from a secure browser window.",
                "official_portal_or_contact": "Official bank or email service login portal.",
                "evidence_to_preserve": "Notification of successful password update."
            },
            {
                "step_number": 3,
                "priority": "Follow-up (1 - 2 Hours)",
                "action_title": "Report Phishing URL to CERT-In Incident Response",
                "instructions": "Forward the deceptive link, screenshot, and sender details to incident@cert-in.org.in and report spam on the TRAI DND 3.0 / Chakshu portal (sancharsaathi.gov.in).",
                "official_portal_or_contact": "incident@cert-in.org.in / https://sancharsaathi.gov.in/sfc/",
                "evidence_to_preserve": "Email delivery acknowledgement from CERT-In."
            }
        ]
    },
    "malicious_application_installation": {
        "title": "Malicious Android APK or Remote Access App Installed",
        "steps": [
            {
                "step_number": 1,
                "priority": "Immediate (0 - 5 Mins)",
                "action_title": "Sever Internet Connection (Airplane Mode)",
                "instructions": "Turn on Airplane Mode immediately and turn off Wi-Fi and Bluetooth. This halts any active background data exfiltration, remote accessibility control, or outgoing SMS forwarding.",
                "official_portal_or_contact": "Device quick settings.",
                "evidence_to_preserve": "Application name, package name, icon, and installation date."
            },
            {
                "step_number": 2,
                "priority": "Immediate (0 - 20 Mins)",
                "action_title": "Revoke Device Admin & Accessibility Permissions",
                "instructions": "Go to Settings > Apps > Special App Access > Device Admin Apps and Accessibility. Revoke permissions for any unfamiliar app, then uninstall the application. If uninstallation is blocked, boot into Safe Mode to remove it.",
                "official_portal_or_contact": "Device settings / Safe Mode recovery.",
                "evidence_to_preserve": "Screenshot of suspicious app permissions if accessible."
            },
            {
                "step_number": 3,
                "priority": "Critical (1 Hour)",
                "action_title": "Perform Full Antivirus Scan & Check SMS Forwarding",
                "instructions": "Turn off call forwarding (*#21# and ##002# to cancel all forwarding). Run Google Play Protect scan and a reputable mobile security scanner.",
                "official_portal_or_contact": "Google Play Protect / Telecom USSD codes.",
                "evidence_to_preserve": "Scan summary report."
            }
        ]
    },
    "identity_misuse": {
        "title": "SIM Swap, eSIM Takeover, or Aadhaar Misuse",
        "steps": [
            {
                "step_number": 1,
                "priority": "Immediate (0 - 15 Mins)",
                "action_title": "Notify Telecom Provider if Cellular Service Drops",
                "instructions": "If your mobile phone abruptly shows 'No Service' or 'SIM Not Provisioned' without reason, immediately call your telecom provider from another phone to report suspected unauthorized SIM swap.",
                "official_portal_or_contact": "Airtel (121) / Jio (198/199) / Vi (199).",
                "evidence_to_preserve": "Exact timestamp when cellular connectivity dropped; telecom complaint ticket ID."
            },
            {
                "step_number": 2,
                "priority": "Immediate (0 - 30 Mins)",
                "action_title": "Lock Aadhaar Biometrics on UIDAI Portal",
                "instructions": "Open the mAadhaar app or visit uidai.gov.in > My Aadhaar > Lock/Unlock Biometrics. Locking biometrics prevents unauthorized AePS fingerprint withdrawals.",
                "official_portal_or_contact": "https://resident.uidai.gov.in/aadhaar-lockunlock",
                "evidence_to_preserve": "Screenshot of successful Aadhaar biometrics lock confirmation."
            },
            {
                "step_number": 3,
                "priority": "Critical (1 - 2 Hours)",
                "action_title": "Check Credit Bureau Inquiries for Fraudulent Loans",
                "instructions": "Check your CIBIL/Experian credit report to verify whether fraudsters have applied for instant consumer loans using your PAN and Aadhaar.",
                "official_portal_or_contact": "Official Credit Information Companies (CIBIL/Experian/CRIF).",
                "evidence_to_preserve": "List of unauthorized loan inquiries with lender names."
            }
        ]
    }
}


def get_recovery_steps(incident_type: str) -> list[dict]:
    """
    Retrieve structured incident recovery action steps.
    
    Args:
        incident_type: Canonical incident type key or alias:
            - 'suspicious_payment' / 'payment_fraud'
            - 'suspected_account_compromise' / 'account_compromise'
            - 'suspected_phishing' / 'phishing'
            - 'malicious_application_installation' / 'malicious_apk'
            - 'identity_misuse' / 'sim_swap'
            
    Returns:
        list[dict]: Ordered list of actionable recovery steps.
    """
    clean_type = (incident_type or "").strip().lower().replace("-", "_").replace(" ", "_")
    
    # Alias resolution
    alias_map = {
        "payment": "suspicious_payment",
        "payment_fraud": "suspicious_payment",
        "unauthorized_transaction": "suspicious_payment",
        "upi_fraud": "suspicious_payment",
        "account": "suspected_account_compromise",
        "account_compromise": "suspected_account_compromise",
        "takeover": "suspected_account_compromise",
        "phishing": "suspected_phishing",
        "smishing": "suspected_phishing",
        "apk": "malicious_application_installation",
        "malicious_apk": "malicious_application_installation",
        "malware": "malicious_application_installation",
        "sim_swap": "identity_misuse",
        "esim": "identity_misuse",
        "identity_theft": "identity_misuse",
        "aadhaar_misuse": "identity_misuse"
    }
    
    target_key = alias_map.get(clean_type, clean_type)
    if target_key in INCIDENT_RECOVERY_REGISTRY:
        return INCIDENT_RECOVERY_REGISTRY[target_key]["steps"]
        
    logger.warning(f"Unknown incident type '{incident_type}'. Returning default emergency steps.")
    return INCIDENT_RECOVERY_REGISTRY["suspicious_payment"]["steps"]
