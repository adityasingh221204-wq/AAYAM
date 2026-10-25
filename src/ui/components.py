"""
AAYAM - Reusable UI Components
Standardized cards, headers, alert boxes, provenance footers, and interactive modals.
"""
import streamlit as st
from src.utils.config import APP_NAME, APP_TAGLINE, SDG_ALIGNMENT


@st.dialog("📖 How to Use AAYAM — Interactive System Guide", width="large")
def show_how_to_use_dialog():
    """Interactive modal guide explaining system architecture, workflows, and navigation."""
    st.markdown(
        """
        <div style="margin-bottom: 14px;">
            <p style="color: #94A3B8; font-size: 0.92rem; margin: 0;">
                Welcome to <strong>AAYAM</strong> (AI-Driven Multi-Dimensional Economic Mobility & Cyber-Financial Intelligence).
                Use the tabs below to explore system workflows, module capabilities, and recommended journeys.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    t1, t2, t3, t4 = st.tabs(["🚀 Quick Start", "🧭 8 Modules Directory", "💡 User Workflows", "🛡️ Privacy & Guardrails"])
    
    with t1:
        st.markdown(
            """
            #### ⚡ 3-Step Quick Start
            
            1. **Configure Your Financial Baseline (Module 2)**
               - Open **Economic Digital Twin** from the sidebar.
               - Enter monthly take-home income, essential expenses, liquid savings, and EMIs.
               - Click **Apply Changes** to calculate your *Resilience Score (0–100)*, Emergency Runway months, and Debt-to-Income (DTI) ratio.
            
            2. **Explore Matched Pathways & Stress-Test (Modules 3 & 5)**
               - Navigate to **Opportunity Pathways** to view AI-ranked wage-employment and micro-enterprise options matched to your profile with PMKVY 4.0 and Mudra linkages.
               - Head to **ArthSim** to stress-test your resilience against adverse shocks (job loss, medical emergency, or cyber fraud).
            
            3. **Screen Digital Threats & Respond (Modules 4, 7 & 8)**
               - In **CyberDrishti**, paste any suspicious SMS, WhatsApp message, or APK prompt to get an instant, explainable threat evaluation.
               - In **Trust Graph**, visualize attack vectors and official defense frameworks.
               - In **Recovery Centre**, follow prioritized incident response playbooks (golden 2-hour window and 1930 reporting).
            """
        )
        
    with t2:
        st.markdown(
            """
            #### 🧭 Module-by-Module Capabilities
            
            | Module | Focus Area | Key Features & Datasets Used |
            |---|---|---|
            | **1. Command Centre** | Executive Telemetry | Unified overview combining your resilience score, macro payment stats, and security posture. |
            | **2. Economic Digital Twin** | Personal Finance Twin | Evaluates liquidity buffers, savings rate, emergency runway, and DTI benchmark. |
            | **3. Opportunity Pathways** | Economic Mobility | 4-factor scoring matching profiles against NSQF, PMKVY 4.0, and MSME opportunities with Mudra loans. |
            | **4. CyberDrishti** | Threat Screening | 13+ rule-based heuristic threat detection with explainable risk breakdown and CERT-In advisories. |
            | **5. ArthSim Simulator** | Scenario Simulation | Deterministic multi-period modeling of income shocks, cyber losses, inflation, and recovery times. |
            | **6. India Intelligence** | Macro Analytics | Official institutional telemetry from RBI (Payments, Frauds), MoSPI (PLFS, HCES, ASUSE), and MHA (1930). |
            | **7. Trust Graph** | Threat Architecture | Interactive NetworkX knowledge graph mapping threat delivery channels, vulnerabilities, and defenses. |
            | **8. Recovery Centre** | Incident Playbooks | Step-by-step incident response for unauthorized UPI, card skimming, SIM swap, and account takeover. |
            """
        )
        
    with t3:
        st.markdown(
            """
            #### 💡 Tailored User Workflows
            
            * **👤 Profile A: Aspiring Worker or Up-skiller**
              - *Path:* Digital Twin → Opportunity Pathways → India Intelligence (Labour tab)
              - *Goal:* Identify career pathways that offer an income uplift, check government subsidy eligibility, and verify regional labour demand.
            
            * **🛡️ Profile B: Citizen Facing Suspicious Message or Call**
              - *Path:* CyberDrishti → Trust Graph → Recovery Centre
              - *Goal:* Verify if an unsolicited SMS (e.g. tax refund, electricity bill, digital arrest) is fraudulent and understand the delivery vector.
            
            * **📊 Profile C: Household Planning Financial Security**
              - *Path:* Digital Twin → ArthSim → India Intelligence (Consumption tab)
              - *Goal:* Benchmark household consumption against NSSO fractiles, simulate emergency scenarios, and optimize liquidity runways.
            """
        )
        
    with t4:
        st.markdown(
            """
            #### 🛡️ Privacy, Safety & Ethical Guardrails
            
            * **Zero Persistent Sensitive Data:** All profile inputs are strictly session-local in your browser's runtime memory.
            * **No Passwords or Credentials:** AAYAM never asks for, stores, or transmits bank account numbers, UPI MPINs, OTPs, or passwords.
            * **Transparent AI & Explainability:** All opportunity matches and threat scores show clear mathematical breakdowns and decision factors.
            * **Official Source Anchoring:** Data is cross-referenced exclusively with authenticated institutional releases (RBI, MoSPI, CERT-In, MHA, NSDC).
            * **Academic Prototype Disclaimer:** AAYAM is an academic decision-support prototype; it does not provide certified legal, investment, or credit advice.
            """
        )
        
    st.markdown("---")
    if st.button("Close Guide ✖", use_container_width=True):
        st.rerun()


def render_header(
    title: str,
    subtitle: str,
    badge_text: str | None = None,
    badge_type: str = "emerald",
    show_guide_btn: bool = True
):
    """
    Render consistent page header with metadata badge, description,
    and an interactive 'How to Use' modal button.
    """
    badge_html = ""
    if badge_text:
        badge_html = f'<span class="badge badge-{badge_type}">{badge_text}</span>'

    col_title, col_action = st.columns([4, 1.2])

    with col_title:
        st.markdown(
            f"""
            <div style="margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px; flex-wrap: wrap;">
                    <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">{title}</h1>
                    {badge_html}
                </div>
                <p style="margin: 0; font-size: 1.0rem; color: #94A3B8; line-height: 1.4;">{subtitle}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_action:
        if show_guide_btn:
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            clean_key = f"hdr_guide_{title.lower().replace(' ', '_')[:16]}"
            if st.button("📖 How to Use", key=clean_key, use_container_width=True):
                show_how_to_use_dialog()


def render_kpi_card(title: str, value: str, subtext: str = "", delta_text: str = "", badge_color: str = "emerald"):
    """Render a styled fintech KPI card inside a Streamlit column."""
    delta_html = ""
    if delta_text:
        delta_html = f'<div style="margin-top: 8px;"><span class="badge badge-{badge_color}">{delta_text}</span></div>'
        
    st.markdown(
        f"""
        <div class="kpi-container">
            <div>
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            <div>
                <div class="kpi-subtext">{subtext}</div>
                {delta_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_alert_box(title: str, message: str, alert_type: str = "info"):
    """
    Render a styled alert banner.
    alert_type: 'info', 'warning', 'danger', 'success'
    """
    colors = {
        "info": ("rgba(99, 102, 241, 0.15)", "#818CF8", "ℹ️"),
        "success": ("rgba(16, 185, 129, 0.15)", "#34D399", "✅"),
        "warning": ("rgba(245, 158, 11, 0.15)", "#FBBF24", "⚠️"),
        "danger": ("rgba(244, 63, 94, 0.15)", "#FB7185", "🚨")
    }
    bg, fg, icon = colors.get(alert_type, colors["info"])
    
    st.markdown(
        f"""
        <div style="background-color: {bg}; border-left: 4px solid {fg}; padding: 14px 18px; border-radius: 8px; margin: 14px 0; border: 1px solid {bg};">
            <div style="font-weight: 700; color: {fg}; font-size: 0.94rem; margin-bottom: 4px;">{icon} {title}</div>
            <div style="color: #F8FAFC; font-size: 0.86rem; line-height: 1.45;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_data_provenance(dataset_name: str, publisher: str, reference_period: str, source_url: str):
    """Render source transparency note indicating data origin and verification."""
    st.markdown(
        f"""
        <div class="provenance-box">
            <strong>Data Provenance:</strong> {dataset_name} &bull; 
            <strong>Publisher:</strong> {publisher} &bull; 
            <strong>Period:</strong> {reference_period} &bull; 
            <a href="{source_url}" target="_blank" style="color: #818CF8; text-decoration: none; font-weight: 600;">[Official Source ↗]</a>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_empty_state(message: str, action_text: str | None = None, target_page: str | None = None):
    """Render empty or unconfigured state with guidance."""
    st.markdown(
        f"""
        <div class="aayam-card" style="text-align: center; padding: 40px 24px;">
            <div style="font-size: 2.2rem; margin-bottom: 12px;">📊</div>
            <h3 style="color: #F8FAFC; margin-bottom: 8px;">No Profile Data Configured</h3>
            <p style="color: #94A3B8; font-size: 0.92rem; max-width: 520px; margin: 0 auto 18px auto; line-height: 1.5;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if action_text and target_page:
        if st.button(action_text):
            st.switch_page(target_page)


def render_footer():
    """Render student prototype disclaimer and SDG mission footer."""
    st.markdown(
        f"""
        <div class="aayam-footer">
            <strong>{APP_NAME}</strong> — {APP_TAGLINE}<br>
            Student Decision-Support Prototype for Academic & Research Evaluation &bull;
            Aligned with <strong>{SDG_ALIGNMENT[0]}</strong> and <strong>{SDG_ALIGNMENT[1]}</strong>.<br>
            <em>Notice: AAYAM is an educational decision-support prototype. It does not provide certified financial, legal, credit, or banking advice.</em>
        </div>
        """,
        unsafe_allow_html=True
    )
