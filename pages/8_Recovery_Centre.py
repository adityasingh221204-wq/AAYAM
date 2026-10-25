"""
AAYAM - Page 8: Recovery Centre
Incident-specific triage, immediate mitigation steps, official Indian escalation routes,
and statutory evidence preservation protocols.
"""
import streamlit as st
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.engines.recovery import get_recovery_steps

st.set_page_config(page_title="Recovery Centre — AAYAM", page_icon="🚑", layout="wide")
apply_theme()

render_header(
    title="Cyber-Financial Recovery Centre",
    subtitle="Actionable, incident-specific triage checklists, evidence preservation, and official escalation pathways.",
    badge_text="Module 8",
    badge_type="rose"
)

render_alert_box(
    title="Statutory Scope Disclaimer",
    message="AAYAM provides actionable recovery guidance and evidence checklists. AAYAM cannot directly reverse bank transactions, freeze third-party accounts, or file FIRs on your behalf. Follow the official escalation routes immediately.",
    alert_type="warning"
)

# 1. Incident Selector
incident_choice = st.selectbox(
    "Select Cyber-Financial Incident Scenario:",
    options=[
        "Unauthorized Digital Payment or Fraudulent Debit",
        "Suspected Account Compromise (UPI / Net Banking / Email)",
        "Suspected Phishing Link or Deceptive Form Interaction",
        "Malicious Application / APK Installed on Device",
        "SIM Swap, eSIM Takeover, or Aadhaar Misuse"
    ]
)

# Map human-readable option to canonical key
incident_key_map = {
    "Unauthorized Digital Payment or Fraudulent Debit": "suspicious_payment",
    "Suspected Account Compromise (UPI / Net Banking / Email)": "suspected_account_compromise",
    "Suspected Phishing Link or Deceptive Form Interaction": "suspected_phishing",
    "Malicious Application / APK Installed on Device": "malicious_application_installation",
    "SIM Swap, eSIM Takeover, or Aadhaar Misuse": "identity_misuse"
}

canonical_key = incident_key_map[incident_choice]
steps = get_recovery_steps(canonical_key)

# 2. Top Emergency Action Contacts
st.markdown("### 🚨 Verified Emergency Helplines")
e1, e2, e3 = st.columns(3)

with e1:
    render_kpi_card(
        title="National Helpline",
        value="📞 1930",
        subtext="Citizen Financial Cyber Fraud System",
        delta_text="Call within 2 hours",
        badge_color="rose"
    )
with e2:
    render_kpi_card(
        title="Official Cybercrime Portal",
        value="🌐 cybercrime.gov.in",
        subtext="National Cyber Crime Reporting Portal",
        delta_text="File Formal Complaint",
        badge_color="indigo"
    )
with e3:
    render_kpi_card(
        title="Lost Mobile / SIM Blocking",
        value="📲 Sanchar Saathi",
        subtext="sancharsaathi.gov.in / Chakshu",
        delta_text="Telecom Department",
        badge_color="emerald"
    )

st.markdown("---")
st.markdown(f"### 📋 Step-by-Step Response Playbook: {incident_choice}")

for step in steps:
    priority_color = "rose" if "Immediate" in step["priority"] else ("amber" if "Critical" in step["priority"] else "indigo")
    
    st.markdown(
        f"""
        <div class="aayam-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: #F8FAFC;">Step {step['step_number']}: {step['action_title']}</h4>
                <span class="badge badge-{priority_color}">{step['priority']}</span>
            </div>
            <div style="color: #CBD5E1; font-size: 0.92rem; line-height: 1.5; margin-bottom: 12px;">
                {step['instructions']}
            </div>
            <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.82rem; border-top: 1px solid #334155; padding-top: 8px;">
                <div style="color: #818CF8;">
                    <strong>Official Channel / Authority:</strong> {step['official_portal_or_contact']}
                </div>
                <div style="color: #FBBF24;">
                    <strong>Evidence to Preserve:</strong> {step['evidence_to_preserve']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 3. Interactive Evidence Checklist Tool
st.markdown("---")
st.markdown("### 🗂️ Victim Evidence Preservation Checklist")
st.write("Ensure you record and screenshot the following items before resetting passwords or uninstalling apps:")

c_col1, c_col2 = st.columns(2)
with c_col1:
    c_debit_sms = st.checkbox("12-digit UTR number and Debit SMS notification")
    c_fraud_upi = st.checkbox("Beneficiary UPI ID or receiving bank account details")
    c_screenshots = st.checkbox("Screenshots of chat / call logs with fraudster")
with c_col2:
    c_bank_call = st.checkbox("Bank customer care complaint ticket number and call timestamp")
    c_ack_1930 = st.checkbox("1930 Helpline registration reference SMS")
    c_cyber_fir = st.checkbox("National Cyber Crime Reporting Portal Acknowledgement (14 digits)")

# Downloadable Incident Checklist (Member 2 Specification)
checklist_text = f"""=====================================================
AAYAM CYBER-FINANCIAL INCIDENT RESPONSE CHECKLIST
Incident Type: {incident_choice}
National Cyber Helpline: 1930 | Official Portal: https://cybercrime.gov.in
=====================================================

ACTION PROTOCOL:
"""
for s in steps:
    checklist_text += f"\n[ ] Step {s['step_number']}: {s['action_title']} ({s['priority']})\n"
    checklist_text += f"    Instructions: {s['instructions']}\n"
    checklist_text += f"    Official Channel: {s['official_portal_or_contact']}\n"
    checklist_text += f"    Evidence to Preserve: {s['evidence_to_preserve']}\n"

checklist_text += f"""
=====================================================
VICTIM EVIDENCE CHECKLIST:
[ {'X' if c_debit_sms else ' '} ] 12-digit UTR number and Debit SMS notification
[ {'X' if c_fraud_upi else ' '} ] Beneficiary UPI ID or receiving bank account details
[ {'X' if c_screenshots else ' '} ] Screenshots of chat / call logs with fraudster
[ {'X' if c_bank_call else ' '} ] Bank customer care complaint ticket number and call timestamp
[ {'X' if c_ack_1930 else ' '} ] 1930 Helpline registration reference SMS
[ {'X' if c_cyber_fir else ' '} ] National Cyber Crime Reporting Portal Acknowledgement (14 digits)
=====================================================
Generated via AAYAM Cyber-Financial Recovery Centre
Notice: Decision-support guidance for statutory escalation under RBI Zero Liability rules.
"""

st.download_button(
    label="📥 Download Incident Response Checklist (.txt)",
    data=checklist_text,
    file_name=f"AAYAM_Recovery_Checklist_{canonical_key}.txt",
    mime="text/plain",
    use_container_width=True
)

# 4. RBI Circular Summary Box
st.markdown("---")
render_alert_box(
    title="RBI Customer Liability Circular (DBR.No.Leg.BC.78/09.07.005/2017-18)",
    message="""
    Under Reserve Bank of India directions on 'Customer Protection — Limiting Liability of Customers in Unauthorised Electronic Banking Transactions':
    <br>&bull; <strong>Zero Liability:</strong> If the unauthorized transaction is due to contributory fraud/negligence on the part of the bank, or third-party breach where customer notifies the bank within <strong>three working days</strong>.
    <br>&bull; <strong>Limited Liability:</strong> If reported between 4 to 7 working days, maximum customer liability is capped (₹5,000 for basic savings/accounts; ₹10,000 for regular savings).
    <br>&bull; <strong>Reversal Timeline:</strong> The bank must shadow-reverse or credit the disputed amount within <strong>10 working days</strong> of complaint.
    """,
    alert_type="info"
)

render_data_provenance(
    dataset_name="Customer Liability Guidelines & Standard Operating Procedures",
    publisher="Reserve Bank of India & Indian Cybercrime Coordination Centre (I4C)",
    reference_period="Statutory Circulars",
    source_url="https://www.rbi.org.in/"
)

render_footer()
