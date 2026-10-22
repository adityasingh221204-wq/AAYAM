"""
AAYAM — AI-Driven Multi-Dimensional Economic Mobility and Cyber-Financial Intelligence System
Main Application Entry Point
"""
import streamlit as st
import pandas as pd
from src.ui.theme import apply_theme
from src.ui.components import render_header, render_kpi_card, render_alert_box, render_footer
from src.utils.config import APP_NAME, APP_TITLE, APP_TAGLINE, SDG_ALIGNMENT
from src.data.loaders import load_public_dataset

# 1. Page Configuration
st.set_page_config(
    page_title=f"{APP_NAME} — Economic Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Apply Custom Modern Fintech Theme
apply_theme()

# 3. Session State Initialization
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {
        "monthly_take_home_income": 35000.0,
        "other_monthly_income": 5000.0,
        "essential_monthly_expenses": 20000.0,
        "discretionary_expenses": 6000.0,
        "current_savings": 50000.0,
        "outstanding_debt": 75000.0,
        "monthly_debt_repayments": 4500.0,
        "emergency_expenses_obligations": 0.0,
        "education": "Higher Secondary (12th)",
        "occupation": "Salaried / Support Role",
        "region": "Maharashtra",
        "skills": ["Customer Service", "Computer Literacy", "Digital Payments"],
        "economic_goals": "Build emergency buffer and transition to higher-wage career pathway"
    }

# 4. Sidebar Navigation & Global System Telemetry
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #334155; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.6rem;">🛡️</span>
                <span style="font-size: 1.4rem; font-weight: 800; color: #10B981; letter-spacing: -0.02em;">{APP_NAME}</span>
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">{APP_TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### 🎯 System Alignment")
    st.markdown(f"**Primary SDGs:**\n- {SDG_ALIGNMENT[0]}\n- {SDG_ALIGNMENT[1]}")
    
    st.markdown("---")
    st.markdown("### 📊 Verified Sourced Data")
    df_reg = load_public_dataset("source_register")
    if not df_reg.empty:
        st.markdown(f"**Registered Sources:** {len(df_reg)}")
        for _, r in df_reg.iterrows():
            st.markdown(f"- **{r['dataset_name']}** ({r['study_or_release'][:22]}...)")
    else:
        st.caption("Registry indexing active.")
        
    st.markdown("---")
    st.caption("AAYAM v1.0 &bull; Student Decision-Support Prototype")

# 5. Main Hero Section
render_header(
    title="AAYAM: Economic Intelligence & Cyber Resilience",
    subtitle="An integrated decision-support platform uniting personal economic modeling, career mobility, macro trends, and digital threat intelligence.",
    badge_text="System Active",
    badge_type="emerald"
)

render_alert_box(
    title="Core Operating Principle",
    message="AAYAM is an independent economic decision-support and cyber-financial resilience platform. It is not a bank, credit rating agency, licensed financial advisor, guaranteed job board, or official government enforcement portal.",
    alert_type="info"
)

# 6. Global Quick Metric Overview
col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card(
        title="UPI Monthly Vol (RBI)",
        value="16,106 Cr",
        subtext="February 2025 bulletin",
        delta_text="+33% YoY Volume",
        badge_color="emerald"
    )
with col2:
    render_kpi_card(
        title="Reported Fraud Value",
        value="₹287.8 Cr",
        subtext="CPFIR Registry (Feb 2025)",
        delta_text="0.121 bps of value",
        badge_color="amber"
    )
with col3:
    render_kpi_card(
        title="National LFPR (PLFS)",
        value="44.5%",
        subtext="Annual Survey 2023-24",
        delta_text="WPR: 43.1% | UR: 3.2%",
        badge_color="indigo"
    )
with col4:
    render_kpi_card(
        title="Urban MPCE (HCES)",
        value="₹6,459",
        subtext="Average Monthly Per Capita",
        delta_text="Food Share: 39.2%",
        badge_color="indigo"
    )

st.markdown("---")

# 7. Navigation Directory to All 8 Modules
st.markdown("### 🌐 Core System Modules")

mod_col1, mod_col2 = st.columns(2)

with mod_col1:
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #34D399; margin-top: 0;">1. Command Centre</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Executive intelligence overview combining personal resilience KPIs, macro indicators, payment trends, and threat alerts in a single unified dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Launch Command Centre ↗", key="btn_p1"):
        st.switch_page("pages/1_Command_Centre.py")
        
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #818CF8; margin-top: 0;">2. Economic Digital Twin</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Build and inspect your personal financial twin. Calculates cash flow buffers, savings rate, emergency runway months, and composite resilience index.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Configure Digital Twin ↗", key="btn_p2"):
        st.switch_page("pages/2_Economic_Digital_Twin.py")
        
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #38BDF8; margin-top: 0;">3. Opportunity Pathways</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Transparently ranked employment, upskilling, and micro-entrepreneurship pathways aligned with PMKVY 4.0, Mudra loans, and verified skill frameworks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Explore Opportunities ↗", key="btn_p3"):
        st.switch_page("pages/3_Opportunity_Pathways.py")
        
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #FB7185; margin-top: 0;">4. CyberDrishti</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Explainable cyber threat screening centre. Analyze suspicious messages, detect deceptive APK prompts, and examine official CERT-In threat advisories.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Open CyberDrishti ↗", key="btn_p4"):
        st.switch_page("pages/4_CyberDrishti.py")

with mod_col2:
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #FBBF24; margin-top: 0;">5. ArthSim: Scenario Simulator</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Deterministic what-if modeling. Simulate the financial impact of job loss, cyber-fraud losses, training expenses, and inflation across multi-month horizons.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Simulate Scenarios ↗", key="btn_p5"):
        st.switch_page("pages/5_ArthSim.py")
        
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #A78BFA; margin-top: 0;">6. India Intelligence</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Macroeconomic and payment analytics using official data from RBI Payment System Indicators, PLFS 2023-24, HCES 2023-24, and ASUSE 2023-24.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("View India Intelligence ↗", key="btn_p6"):
        st.switch_page("pages/6_India_Intelligence.py")
        
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #2DD4BF; margin-top: 0;">7. Trust Graph</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Interactive graph visualising relationships among cyber threats, delivery channels, financial vulnerabilities, and official defense frameworks.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Inspect Trust Graph ↗", key="btn_p7"):
        st.switch_page("pages/7_Trust_Graph.py")
        
    st.markdown(
        """
        <div class="aayam-card">
            <h4 style="color: #F43F5E; margin-top: 0;">8. Recovery Centre</h4>
            <p style="color: #94A3B8; font-size: 0.9rem;">
                Step-by-step incident response playbook for suspected unauthorized payments, account takeover, phishing, and SIM swap with official 1930 and bank contacts.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Open Recovery Centre ↗", key="btn_p8"):
        st.switch_page("pages/8_Recovery_Centre.py")

# 8. Footer
render_footer()
