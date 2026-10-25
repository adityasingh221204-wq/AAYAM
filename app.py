"""
AAYAM — AI-Driven Multi-Dimensional Economic Mobility and Cyber-Financial Intelligence System
Main Application Entry Point
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
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

# 4. Sidebar — Branding, Clock, System Health
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 10px 0 20px 0; border-bottom: 1px solid rgba(51,65,85,0.4); margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.8rem;">🛡️</span>
                <span style="font-size: 1.5rem; font-weight: 900; background: linear-gradient(135deg, #10B981, #34D399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.02em;">{APP_NAME}</span>
            </div>
            <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px; font-style: italic;">{APP_TAGLINE}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Live IST Clock
    ist_zone = timezone(timedelta(hours=5, minutes=30))
    ist_time = datetime.now(ist_zone).strftime("%d %b %Y  •  %I:%M %p IST")
    st.markdown(f"🕒 `{ist_time}`")
    
    st.markdown("---")
    st.markdown("### 🎯 SDG Alignment")
    st.markdown(f"- {SDG_ALIGNMENT[0]}\n- {SDG_ALIGNMENT[1]}")
    
    st.markdown("---")
    st.markdown("### 📊 Data Registry")
    df_reg = load_public_dataset("source_register")
    if not df_reg.empty:
        st.markdown(f"**{len(df_reg)} Verified Sources**")
        for _, r in df_reg.iterrows():
            st.markdown(f"- {r['dataset_name'][:35]}…")
    
    st.markdown("---")
    st.caption("AAYAM v2.0  •  128 Tests Passing  •  Academic Prototype")

# 5. Hero Section
st.markdown(
    f"""
    <div class="aayam-hero">
        <div style="position: relative; z-index: 1;">
            <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 10px;">
                <h1 style="margin: 0; font-size: 2.4rem; font-weight: 900; color: #F8FAFC; letter-spacing: -0.03em;">
                    AAYAM
                </h1>
                <span class="badge badge-emerald" style="animation: pulse-glow 2s ease-in-out infinite;">System Active</span>
            </div>
            <p style="margin: 0; font-size: 1.1rem; color: #CBD5E1; max-width: 700px; line-height: 1.5;">
                AI-Driven Multi-Dimensional Economic Mobility & Cyber-Financial Intelligence — 
                uniting personal economic modeling, career pathways, macro analytics, and digital threat defense.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 6. How-to-Use Toggle (Collapsible Guide)
with st.expander("📖  How to Use AAYAM — Quick Start Guide", expanded=False):
    st.markdown(
        """
        <div style="padding: 8px 0;">
            <div class="guide-step">
                <span class="guide-step-num">1</span>
                <strong style="color: #F8FAFC;">Set Up Your Financial Twin</strong>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 36px;">
                    Navigate to <strong>Economic Digital Twin</strong> → fill in your monthly income, expenses, savings, and debt in the sidebar form → click <em>Apply Changes</em> to generate your personalized resilience score and financial indicators.
                </p>
            </div>
            <div class="guide-step">
                <span class="guide-step-num">2</span>
                <strong style="color: #F8FAFC;">Explore Career & Enterprise Opportunities</strong>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 36px;">
                    Open <strong>Opportunity Pathways</strong> → use the filter sidebar to narrow by track (Employment / Micro-Enterprise), sector, and location → each card shows a transparent 4-factor match score, required skills, and Mudra loan eligibility.
                </p>
            </div>
            <div class="guide-step">
                <span class="guide-step-num">3</span>
                <strong style="color: #F8FAFC;">Screen Suspicious Messages</strong>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 36px;">
                    Go to <strong>CyberDrishti</strong> → paste any suspicious SMS, WhatsApp message, or APK prompt into the text area → the engine analyzes it against 13+ threat rules and returns an explainable risk score with safety guidance.
                </p>
            </div>
            <div class="guide-step">
                <span class="guide-step-num">4</span>
                <strong style="color: #F8FAFC;">Stress-Test Your Finances</strong>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 36px;">
                    Use <strong>ArthSim</strong> → select a scenario (job loss, fraud, medical emergency) → adjust severity sliders → view the projected savings trajectory and months-to-depletion over your chosen horizon.
                </p>
            </div>
            <div class="guide-step">
                <span class="guide-step-num">5</span>
                <strong style="color: #F8FAFC;">Monitor Macroeconomic Trends</strong>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 36px;">
                    Open <strong>India Intelligence</strong> → switch between 5 tabs (RBI Payments, Fraud Trends, Labour Force, Household Expenditure, Enterprises) → interactive charts show UPI volumes, sector-level employment, and consumption patterns.
                </p>
            </div>
            <div class="guide-step">
                <span class="guide-step-num">6</span>
                <strong style="color: #F8FAFC;">Respond to Fraud Incidents</strong>
                <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 36px;">
                    If compromised, go to <strong>Recovery Centre</strong> → select your incident type → follow the prioritized step-by-step playbook (golden 2-hour window, RBI 72-hour zero-liability dispute). Download a checklist for offline use.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# 7. Quick Macro Metrics
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

# 8. Module Navigation — Premium Cards
st.markdown("### 🌐 Core System Modules")
st.caption("Click any module to launch it.")

MODULES = [
    {
        "num": "01", "title": "Command Centre", "icon": "🧭",
        "color": "#34D399",
        "desc": "Executive intelligence overview — personal resilience KPIs, macro payment trends, and real-time threat posture.",
        "btn": "Launch Command Centre", "page": "pages/1_Command_Centre.py"
    },
    {
        "num": "02", "title": "Economic Digital Twin", "icon": "🧬",
        "color": "#818CF8",
        "desc": "Build your personal financial twin. Calculate cash flow, savings rate, emergency runway, and composite resilience.",
        "btn": "Configure Digital Twin", "page": "pages/2_Economic_Digital_Twin.py"
    },
    {
        "num": "03", "title": "Opportunity Pathways", "icon": "🚀",
        "color": "#38BDF8",
        "desc": "Transparently ranked employment, upskilling, and micro-enterprise pathways with PMKVY 4.0 and Mudra linkages.",
        "btn": "Explore Opportunities", "page": "pages/3_Opportunity_Pathways.py"
    },
    {
        "num": "04", "title": "CyberDrishti", "icon": "🔍",
        "color": "#FB7185",
        "desc": "Explainable cyber threat screening — analyze suspicious SMS, APK prompts, and UPI fraud patterns.",
        "btn": "Open CyberDrishti", "page": "pages/4_CyberDrishti.py"
    },
    {
        "num": "05", "title": "ArthSim Simulator", "icon": "⚡",
        "color": "#FBBF24",
        "desc": "What-if financial modeling — simulate job loss, cyber-fraud, medical emergencies over 3–60 month horizons.",
        "btn": "Simulate Scenarios", "page": "pages/5_ArthSim.py"
    },
    {
        "num": "06", "title": "India Intelligence", "icon": "📊",
        "color": "#A78BFA",
        "desc": "5-tab macro dashboard — RBI Payment Systems, CPFIR fraud metrics, PLFS, HCES, and ASUSE analytics.",
        "btn": "View Intelligence", "page": "pages/6_India_Intelligence.py"
    },
    {
        "num": "07", "title": "Trust Graph", "icon": "🕸️",
        "color": "#2DD4BF",
        "desc": "Interactive network graph mapping cyber threat vectors, delivery channels, and official defense frameworks.",
        "btn": "Inspect Trust Graph", "page": "pages/7_Trust_Graph.py"
    },
    {
        "num": "08", "title": "Recovery Centre", "icon": "🆘",
        "color": "#F43F5E",
        "desc": "Time-critical incident response — golden 2-hour window playbooks with 1930 and bank contacts.",
        "btn": "Open Recovery Centre", "page": "pages/8_Recovery_Centre.py"
    },
]

# Render in 2 columns
left_modules = MODULES[:4]
right_modules = MODULES[4:]

mod_col1, mod_col2 = st.columns(2)

for col, mods in [(mod_col1, left_modules), (mod_col2, right_modules)]:
    with col:
        for m in mods:
            st.markdown(
                f"""
                <div class="module-card">
                    <span class="module-num">{m['num']}</span>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span style="font-size: 1.3rem;">{m['icon']}</span>
                        <h4 style="color: {m['color']}; margin: 0; font-size: 1.1rem; font-weight: 700;">{m['title']}</h4>
                    </div>
                    <p style="color: #94A3B8; font-size: 0.88rem; margin: 0; line-height: 1.45;">{m['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"{m['btn']} →", key=f"btn_{m['num']}"):
                st.switch_page(m['page'])

# 9. About AAYAM & SDG Alignment (Collapsible)
with st.expander("ℹ️  About AAYAM — Academic Mission, Architecture & SDG Alignment", expanded=False):
    st.markdown(
        f"""
        ### 🇮🇳 What is AAYAM?
        **AAYAM** (*AI-Driven Multi-Dimensional Economic Mobility and Cyber-Financial Intelligence System*) is an academic, open-source decision-support platform built for the Indian socio-economic landscape.
        
        It bridges the critical gap between **economic mobility** (upskilling, livelihood security, micro-enterprise) and **cyber-financial defense** (phishing detection, APK threat screening, fraud response).
        
        #### 🏛️ Architectural Pillars:
        1. **Personal Economic Twin & ArthSim Simulator:** Deterministic multi-period modeling of cash flows, liquidity runways, and shock stress-testing.
        2. **Opportunity Pathways Engine:** Transparent, 4-factor scoring matching profiles against NSQF, PMKVY 4.0, and MSME opportunities with verified Mudra loan linkages.
        3. **CyberDrishti & Trust Graph:** Rule-based explainable threat screening against deceptive SMS/APKs, paired with a NetworkX knowledge graph and CERT-In advisories.
        4. **Recovery Centre:** Incident response playbooks prioritizing the golden 2-hour window and RBI 72-hour zero-liability dispute protocols.
        5. **India Macroeconomic Intelligence:** Real-time integration of official data from RBI Payment Systems, MoSPI PLFS (Labour), HCES (Consumption), and ASUSE (Informal Enterprises).

        #### 🎯 UN Sustainable Development Goals (SDGs):
        - **{SDG_ALIGNMENT[0]}:** Promoting sustained, inclusive economic growth and productive employment through explainable pathway guidance.
        - **{SDG_ALIGNMENT[1]}:** Strengthening socio-economic resilience by defending citizen financial assets against predatory cyber attacks.
        
        #### 👥 Team:
        | Member | Domain |
        |---|---|
        | **Aditya Singh** | FinTech & Data Engineering |
        | **Abhishek Shrivastava** | Cybersecurity & Threat Intelligence |
        | **Aarushi S.** | AI/ML & Opportunity Intelligence |
        | **Ansh Saini** | UI / UX & Platform |
        """
    )

render_alert_box(
    title="Core Operating Principle",
    message="AAYAM is an independent economic decision-support and cyber-financial resilience platform. It is not a bank, credit rating agency, licensed financial advisor, guaranteed job board, or official government enforcement portal.",
    alert_type="info"
)

# 10. Footer
render_footer()
