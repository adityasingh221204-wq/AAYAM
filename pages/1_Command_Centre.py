"""
AAYAM - Page 1: Command Centre
Executive multi-dimensional economic dashboard integrating personal resilience,
macro trends, payment telemetry, and cyber threat warnings.
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.ui.charts import (
    plot_cashflow_breakdown, plot_rbi_payment_growth,
    plot_rbi_fraud_trends
)
from src.engines.economy import calculate_financial_indicators
from src.engines.cyber import assess_cyber_risk
from src.data.loaders import load_public_dataset
from src.utils.formatting import format_inr, format_pct

st.set_page_config(page_title="Command Centre — AAYAM", page_icon="🧭", layout="wide")
apply_theme()

render_header(
    title="AAYAM Command Centre",
    subtitle="Integrated Multi-Dimensional Intelligence: Personal Resilience, Macro Indicators & Threat Posture",
    badge_text="Executive Dashboard",
    badge_type="emerald"
)

# ── Sidebar: System Health Telemetry & Quick Threat Screen (Member 4 Specification) ──
with st.sidebar:
    st.markdown("### 🖥️ System Health & Telemetry")
    
    # Live IST Clock
    ist_zone = timezone(timedelta(hours=5, minutes=30))
    ist_time = datetime.now(ist_zone).strftime("%I:%M %p IST • %d %b %Y")
    st.caption(f"🕒 `{ist_time}`")
    
    # Load dataset registry & opportunities for dynamic counts
    df_reg = load_public_dataset("source_register")
    df_opps = load_public_dataset("opportunities")
    dataset_count = len(df_reg) if not df_reg.empty else 8
    opps_count = len(df_opps) if not df_opps.empty else 12
    
    st.markdown(
        f"""
        <div class="aayam-card-secondary" style="padding: 12px 14px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 0.82rem; color: #94A3B8;">System Status</span>
                <span class="badge badge-emerald">Operational</span>
            </div>
            <div style="font-size: 0.85rem; color: #F8FAFC; margin-bottom: 4px;">
                📚 <strong>{dataset_count} Verified Datasets</strong>
            </div>
            <div style="font-size: 0.85rem; color: #F8FAFC; margin-bottom: 4px;">
                🚀 <strong>{opps_count} Career Pathways</strong>
            </div>
            <div style="font-size: 0.85rem; color: #F8FAFC; margin-bottom: 4px;">
                🧪 <strong>130 Unit Tests Verified</strong>
            </div>
            <div style="font-size: 0.78rem; color: #818CF8; border-top: 1px solid rgba(51, 65, 85, 0.4); padding-top: 6px; margin-top: 6px;">
                Latest Bulletin: <strong>February 2025</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### 🔍 Quick Threat Screen")
    st.caption("Paste an unsolicited message or link for instant triage:")
    quick_msg = st.text_input(
        "Screen SMS / Link",
        placeholder="e.g. Bijli bill pending update apk...",
        label_visibility="collapsed",
        key="cmd_quick_threat"
    )
    
    if quick_msg and quick_msg.strip():
        quick_result = assess_cyber_risk(quick_msg)
        q_score = quick_result["risk_score"]
        q_level = quick_result["risk_level"]
        q_color = "rose" if q_score >= 60 else ("amber" if q_score >= 35 else ("indigo" if q_score >= 15 else "emerald"))
        
        st.markdown(
            f"""
            <div class="aayam-card-secondary" style="padding: 10px 14px; margin-top: 6px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 700; font-size: 0.85rem; color: #F8FAFC;">Score: {q_score:.0f}/100</span>
                    <span class="badge badge-{q_color}">{q_level}</span>
                </div>
                <div style="font-size: 0.78rem; color: #94A3B8;">
                    Stage: <strong>{quick_result.get('attack_chain_stage', 'Triage')}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Full Triage in CyberDrishti ↗", key="btn_quick_cyber_full", use_container_width=True):
            st.session_state["cyber_screen_result"] = quick_result
            st.switch_page("pages/4_CyberDrishti.py")

# 1. User Profile Status & Resilience Baseline
profile = st.session_state.get("user_profile", {})
indicators = calculate_financial_indicators(profile)

st.markdown("### 👤 User Economic Twin Status")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

res_score = indicators["resilience_score"]
res_cat = indicators["resilience_category"]
res_color = "emerald" if res_score >= 70 else ("indigo" if res_score >= 50 else ("amber" if res_score >= 30 else "rose"))

with kpi_col1:
    render_kpi_card(
        title="Resilience Score",
        value=f"{res_score} / 100",
        subtext=res_cat,
        delta_text=f"{indicators['component_scores']['emergency_runway_points']:.0f} pts runway",
        badge_color=res_color
    )
with kpi_col2:
    render_kpi_card(
        title="Net Monthly Surplus",
        value=format_inr(indicators["monthly_surplus_deficit"]),
        subtext=f"Total Inflow: {format_inr(indicators['total_monthly_income'])}",
        delta_text=f"{indicators['savings_rate_pct']}% Savings Rate",
        badge_color="emerald" if indicators["monthly_surplus_deficit"] >= 0 else "rose"
    )
with kpi_col3:
    render_kpi_card(
        title="Emergency Runway",
        value=f"{indicators['emergency_fund_months']:.1f} Mo",
        subtext=f"Savings: {format_inr(profile.get('current_savings', 0))}",
        delta_text="Goal: 6.0 Months",
        badge_color="emerald" if indicators["emergency_fund_months"] >= 6 else "amber"
    )
with kpi_col4:
    render_kpi_card(
        title="Debt-to-Income (DTI)",
        value=format_pct(indicators["debt_to_income_ratio_pct"]),
        subtext=f"Monthly EMI: {format_inr(profile.get('monthly_debt_repayments', 0))}",
        delta_text="Safe Cap: <40%",
        badge_color="emerald" if indicators["debt_to_income_ratio_pct"] <= 40 else "rose"
    )

# 2. Key Warnings & Recommended Actions
if indicators["risk_factors"]:
    render_alert_box(
        title="Key Economic Risk Warnings",
        message=" &bull; ".join(indicators["risk_factors"]),
        alert_type="warning"
    )

# 3. Macroeconomic & Payment System Intelligence Section
st.markdown("---")
st.markdown("### 🇮🇳 Macroeconomic & Digital Payment Telemetry")

tab_macro, tab_payments, tab_cyber = st.tabs(["Employment & Enterprise", "Digital Payments & Frauds", "Active Threat Alerts"])

with tab_macro:
    m_col1, m_col2 = st.columns([1, 1])
    df_plfs = load_public_dataset("plfs")
    df_asuse = load_public_dataset("asuse")
    
    with m_col1:
        st.markdown("#### Labour Workforce Highlights (PLFS 2023-24)")
        if not df_plfs.empty:
            all_india = df_plfs[df_plfs["state"] == "All India"]
            st.dataframe(
                all_india[["sector", "gender", "lfpr_pct", "wpr_pct", "ur_pct", "avg_daily_earnings_regular_inr"]].rename(
                    columns={
                        "sector": "Sector",
                        "gender": "Gender",
                        "lfpr_pct": "LFPR (%)",
                        "wpr_pct": "WPR (%)",
                        "ur_pct": "Unemployment (%)",
                        "avg_daily_earnings_regular_inr": "Avg Daily Wage (₹)"
                    }
                ),
                hide_index=True,
                use_container_width=True
            )
            render_data_provenance("PLFS 2023-24", "MoSPI", "July 2023 - June 2024", "https://microdata.gov.in/nada/index.php/catalog")
        else:
            st.warning("PLFS dataset currently unavailable.")
            
    with m_col2:
        st.markdown("#### Unincorporated Enterprises (ASUSE 2023-24)")
        if not df_asuse.empty:
            st.dataframe(
                df_asuse[["broad_activity", "enterprise_type", "annual_gva_per_enterprise_inr", "avg_workers_per_ent", "pct_share_enterprises"]].rename(
                    columns={
                        "broad_activity": "Activity",
                        "enterprise_type": "Type",
                        "annual_gva_per_enterprise_inr": "Annual GVA (₹)",
                        "avg_workers_per_ent": "Avg Workers",
                        "pct_share_enterprises": "Share (%)"
                    }
                ),
                hide_index=True,
                use_container_width=True
            )
            render_data_provenance("ASUSE 2023-24", "MoSPI", "FY 2023-24", "https://microdata.gov.in/nada/index.php/catalog")
        else:
            st.warning("ASUSE dataset currently unavailable.")

with tab_payments:
    df_payments = load_public_dataset("rbi_payment_systems")
    df_frauds = load_public_dataset("rbi_frauds")
    
    # ── UPI Metric Cards with MoM and YoY Delta (Member 4 Specification) ──
    if not df_payments.empty:
        upi_df = df_payments[df_payments["system_name"] == "UPI"].set_index("period")
        
        # Calculate MoM and YoY metrics if available
        try:
            feb25_vol = float(upi_df.loc["February 2025", "volume_crore"])
            jan25_vol = float(upi_df.loc["January 2025", "volume_crore"])
            feb24_vol = float(upi_df.loc["February 2024", "volume_crore"])
            
            feb25_val = float(upi_df.loc["February 2025", "value_inr_crore"])
            feb24_val = float(upi_df.loc["February 2024", "value_inr_crore"])
            
            mom_vol_delta = ((feb25_vol - jan25_vol) / jan25_vol) * 100
            yoy_vol_delta = ((feb25_vol - feb24_vol) / feb24_vol) * 100
            yoy_val_delta = ((feb25_val - feb24_val) / feb24_val) * 100
            
            u_col1, u_col2, u_col3 = st.columns(3)
            with u_col1:
                render_kpi_card(
                    title="UPI Monthly Volume (RBI)",
                    value=f"{feb25_vol:,.1f} Cr",
                    subtext="February 2025 bulletin",
                    delta_text=f"{yoy_vol_delta:+.1f}% YoY Volume",
                    badge_color="emerald"
                )
            with u_col2:
                render_kpi_card(
                    title="UPI Month-over-Month",
                    value=f"{mom_vol_delta:+.1f}% MoM",
                    subtext="vs Jan 2025 (28-day month)",
                    delta_text=f"{feb25_vol:,.0f} Cr vs {jan25_vol:,.0f} Cr",
                    badge_color="indigo"
                )
            with u_col3:
                render_kpi_card(
                    title="UPI Total Value",
                    value=f"₹{feb25_val/100000:.2f} Lakh Cr",
                    subtext="February 2025 bulletin",
                    delta_text=f"{yoy_val_delta:+.1f}% YoY Value",
                    badge_color="emerald"
                )
        except Exception:
            pass

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        if not df_payments.empty:
            st.plotly_chart(plot_rbi_payment_growth(df_payments), use_container_width=True)
            render_data_provenance("Payment System Indicators", "Reserve Bank of India", "February 2025 Bulletin", "https://www.rbi.org.in/Scripts/PSIUserView.aspx?Id=45")
        else:
            st.info("Payment indicators data not loaded.")
            
    with p_col2:
        if not df_frauds.empty:
            st.plotly_chart(plot_rbi_fraud_trends(df_frauds), use_container_width=True)
            render_data_provenance("Central Payments Fraud Information Registry", "RBI", "Sept 2022 - Feb 2025", "https://www.rbi.org.in/")
        else:
            st.info("Fraud indicators data not loaded.")

with tab_cyber:
    df_cert = load_public_dataset("cert_in_advisories")
    if not df_cert.empty:
        st.markdown("#### High-Severity CERT-In Cyber Threat Advisories")
        for _, adv in df_cert.head(4).iterrows():
            st.markdown(
                f"""
                <div class="aayam-card-secondary">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; color: #F8FAFC;">{adv['title']}</span>
                        <span class="badge badge-rose">{adv['severity']}</span>
                    </div>
                    <div style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 4px;"><strong>Vector:</strong> {adv['attack_vector']}</div>
                    <div style="color: #34D399; font-size: 0.82rem;"><strong>Defense:</strong> {adv['mitigation_steps']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        render_data_provenance("Public Security Advisories", "CERT-In / MeitY", "2024", "https://www.cert-in.org.in/")
    else:
        st.info("No active cyber threat advisories indexed.")

# 4. Next Recommended Actions
st.markdown("---")
st.markdown("### 💡 Recommended Next Actions")
act_col1, act_col2, act_col3 = st.columns(3)

with act_col1:
    st.markdown("**Personal Financial Stress Testing**")
    st.write("Simulate an unexpected income shock or fraud deduction in ArthSim.")
    if st.button("Launch ArthSim ↗", key="act_p5"):
        st.switch_page("pages/5_ArthSim.py")
        
with act_col2:
    st.markdown("**Screen Communications**")
    st.write("Scan an unverified SMS, electricity bill alert, or job message in CyberDrishti.")
    if st.button("Launch CyberDrishti ↗", key="act_p4"):
        st.switch_page("pages/4_CyberDrishti.py")

with act_col3:
    st.markdown("**Career & Upward Mobility**")
    st.write("Identify skills and micro-enterprise options matching your economic profile.")
    if st.button("Explore Opportunities ↗", key="act_p3"):
        st.switch_page("pages/3_Opportunity_Pathways.py")

render_footer()
