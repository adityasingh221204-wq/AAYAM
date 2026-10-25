"""
AAYAM - Page 4: CyberDrishti
Explainable cybersecurity threat screening and public advisory intelligence.
"""
import streamlit as st
import pandas as pd
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.engines.cyber import assess_cyber_risk
from src.data.loaders import load_public_dataset

st.set_page_config(page_title="CyberDrishti — AAYAM", page_icon="🛡️", layout="wide")
apply_theme()

render_header(
    title="CyberDrishti: Threat Intelligence & Text Screening",
    subtitle="Explainable pattern analysis of suspicious messages, deceptive APK lures, and official CERT-In advisories.",
    badge_text="Module 4",
    badge_type="rose"
)

render_alert_box(
    title="Safety & Confidentiality Warning",
    message="NEVER paste real passwords, OTPs, PINs, bank account numbers, or complete credit card digits into any screening field. CyberDrishti performs pattern recognition on text phrasing and URLs only.",
    alert_type="warning"
)

tab_scanner, tab_library = st.tabs(["🔍 Threat & Message Scanner", "📚 CERT-In Threat Advisory Library"])

with tab_scanner:
    st.markdown("### 💬 Communication Screening")
    st.write("Paste an unsolicited SMS, WhatsApp notification, job offer, or electricity bill notice to analyze social engineering patterns.")
    
    sample_text = st.selectbox(
        "Or load an illustrative threat sample to test:",
        options=[
            "Custom text entry",
            "Electricity Bill Scam: 'Dear consumer your electricity power will be disconnected tonight at 9:30 pm from bijli vibhag because previous month bill was not updated. Please immediately install update apk from link http://bit.ly/bijli-apk to avoid power cut.'",
            "Reverse UPI Scam: 'Sir I am buying your sofa on OLX. I have sent QR code. Please scan QR code and enter your 6-digit UPI PIN to receive ₹15,000 in your bank account immediately.'",
            "Remote Screen Sharing Fraud: 'Hello from SBI Card customer support. Your card points expiring today. Please install AnyDesk from Play Store and share the 9-digit code so our executive can credit ₹8,500.'",
            "Digital Arrest Extortion: 'This is CBI Officer Sharma calling via Skype video call. A narcotics parcel addressed in your name was intercepted by Customs. You are placed under digital arrest until you transfer funds to court verification account.'"
        ]
    )
    
    if sample_text == "Custom text entry":
        input_msg = st.text_area("Message Text to Screen", height=120, placeholder="Paste suspicious SMS, email text, or chat message here...")
    else:
        input_msg = st.text_area("Message Text to Screen", value=sample_text, height=120)
        
    if st.button("Screen Message for Deceptive Patterns 🛡️", key="btn_screen"):
        if input_msg.strip():
            result = assess_cyber_risk(input_msg)
            st.session_state["cyber_screen_result"] = result
        else:
            st.warning("Please enter or paste text to screen.")

    # Display results if available
    res = st.session_state.get("cyber_screen_result")
    if res:
        st.markdown("---")
        st.markdown("### 📊 Screening Results")
        
        score = res["risk_score"]
        level = res["risk_level"]
        badge_color = "rose" if score >= 60 else ("amber" if score >= 35 else ("indigo" if score >= 15 else "emerald"))

        # Threat Progress Bar & Risk Badge
        st.markdown(
            f"""
            <div style="margin: 12px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; color: #F8FAFC; font-size: 1.05rem;">Suspicion Meter: {score:.0f} / 100</span>
                    <span class="badge badge-{badge_color}">{level}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.progress(float(min(1.0, max(0.0, score / 100.0))))

        c1, c2, c3 = st.columns(3)
        with c1:
            render_kpi_card(
                title="Threat Suspicion Index",
                value=f"{score:.0f} / 100",
                subtext="Heuristic Risk Weight",
                delta_text=level,
                badge_color=badge_color
            )
        with c2:
            render_kpi_card(
                title="Patterns Identified",
                value=str(len(res["triggered_patterns"])),
                subtext=f"Reason Codes: {len(res['reason_codes'])}",
                delta_text="Multi-Factor Check",
                badge_color=badge_color
            )
        with c3:
            render_kpi_card(
                title="Attack Chain Stage",
                value=res["attack_chain_stage"],
                subtext="MITRE / Cyber Kill Chain Stage",
                delta_text="Exploitation Phase",
                badge_color=badge_color
            )
            
        if res["is_suspicious"]:
            render_alert_box(
                title=f"Suspicious Indicators Detected ({level})",
                message=f"This message demonstrates characteristics consistent with <strong>{level}</strong>. Do not click links, install external APKs, or enter UPI PINs.",
                alert_type="danger" if score >= 50 else "warning"
            )
            
        # Breakdown of patterns as Expandable components (Member 2 Specification)
        st.markdown("#### 🔍 Triggered Threat Pattern Details")
        if res["triggered_patterns"]:
            for idx, pat in enumerate(res["triggered_patterns"], start=1):
                with st.expander(f"Pattern {idx}: {pat['code']} — {pat['category']} (+{pat['severity_points']} pts)", expanded=True):
                    st.markdown(f"**Pattern Code:** `{pat['code']}` &bull; **Category:** `{pat['category']}` &bull; **Severity Contribution:** `+{pat['severity_points']} pts`")
                    st.markdown(f"**Explanation:** {pat['explanation']}")
                    st.markdown(f"**Matched Term Snippets:** `{'`, `'.join(pat['matched_terms'])}`")
        else:
            st.info("No overt high-risk phrasing recognized by baseline heuristics.")
            
        # Actionable Safety Guidance as Numbered Checklist with ⚠️ icons (Member 2 Specification)
        st.markdown("#### 🛡️ Prioritised Safety Guidance Checklist")
        for idx, g in enumerate(res["safety_guidance"], start=1):
            st.markdown(
                f"""
                <div style="background-color: rgba(30, 41, 59, 0.7); border-left: 3px solid #FBBF24; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px;">
                    ⚠️ <strong>{idx}.</strong> <span style="color: #F8FAFC; margin-left: 4px;">{g}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.caption(f"_{res['disclaimer']}_")

with tab_library:
    st.markdown("### 📚 CERT-In Cyber Threat Advisories")
    df_cert = load_public_dataset("cert_in_advisories")
    
    if not df_cert.empty:
        # Category Filter
        categories = ["All Categories"] + sorted(list(df_cert["category"].unique()))
        selected_cat = st.selectbox("Filter by Threat Vector", categories)
        
        filtered_df = df_cert if selected_cat == "All Categories" else df_cert[df_cert["category"] == selected_cat]
        
        for _, adv in filtered_df.iterrows():
            with st.expander(f"{adv['title']} — Severity: {adv['severity']}", expanded=True):
                st.markdown(f"**Advisory ID:** `{adv['advisory_id']}` &bull; **Published:** `{adv['published_date']}`")
                st.markdown(f"**Attack Vector:** {adv['attack_vector']}")
                st.markdown(f"**Financial Impact:** <span style='color: #FB7185;'>{adv['financial_impact']}</span>", unsafe_allow_html=True)
                st.markdown(f"**Mitigation Steps:** <span style='color: #34D399;'>{adv['mitigation_steps']}</span>", unsafe_allow_html=True)
                st.markdown(f"[Official Reference Link ↗]({adv['reference_url']})")
                
        render_data_provenance("Official Cybersecurity Advisories", "CERT-In & I4C", "2024", "https://www.cert-in.org.in/")
    else:
        st.warning("CERT-In advisories dataset is unavailable.")

render_footer()
