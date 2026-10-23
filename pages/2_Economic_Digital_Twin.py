"""
AAYAM - Page 2: Economic Digital Twin
Interactive personal financial twin modeling income, living costs, debt obligations,
and composite economic resilience.
"""
import streamlit as st
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box, render_footer
)
from src.ui.charts import (
    plot_cashflow_breakdown, plot_resilience_gauge, plot_resilience_components
)
from src.engines.economy import calculate_financial_indicators
from src.utils.formatting import format_inr, format_pct

st.set_page_config(page_title="Economic Digital Twin — AAYAM", page_icon="🧬", layout="wide")
apply_theme()

render_header(
    title="Economic Digital Twin",
    subtitle="Model your financial baseline, analyze liquidity buffers, and evaluate composite resilience.",
    badge_text="Module 2",
    badge_type="indigo"
)

render_alert_box(
    title="Privacy & Data Integrity Notice",
    message="All profile details remain strictly session-local in memory. No financial numbers, passwords, OTPs, or bank account credentials are ever logged, sent to external APIs, or persisted to disk.",
    alert_type="info"
)

# 1. Load Active Session Profile
current_profile = st.session_state.get("user_profile", {})

# 2. Sidebar Profile Update Form (Member 1 Enhanced Specification)
with st.sidebar:
    st.markdown("### ⚙️ Update Twin Profile")
    st.caption("Adjust financial parameters in real-time:")
    with st.form("digital_twin_sidebar_form"):
        take_home = st.number_input(
            "Primary Take-Home (₹/mo)",
            min_value=0.0,
            max_value=2000000.0,
            value=float(current_profile.get("monthly_take_home_income", 35000.0)),
            step=1000.0
        )
        other_income = st.number_input(
            "Other Income (₹/mo)",
            min_value=0.0,
            max_value=1000000.0,
            value=float(current_profile.get("other_monthly_income", 5000.0)),
            step=500.0
        )
        essential_exp = st.number_input(
            "Essential Expenses (₹/mo)",
            min_value=0.0,
            max_value=1000000.0,
            value=float(current_profile.get("essential_monthly_expenses", 20000.0)),
            step=1000.0
        )
        discretionary_exp = st.number_input(
            "Discretionary Exp (₹/mo)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_profile.get("discretionary_expenses", 6000.0)),
            step=500.0
        )
        current_savings = st.number_input(
            "Liquid Savings (₹)",
            min_value=0.0,
            max_value=50000000.0,
            value=float(current_profile.get("current_savings", 50000.0)),
            step=5000.0
        )
        outstanding_debt = st.number_input(
            "Total Debt Balance (₹)",
            min_value=0.0,
            max_value=10000000.0,
            value=float(current_profile.get("outstanding_debt", 75000.0)),
            step=5000.0
        )
        monthly_emi = st.number_input(
            "Monthly EMIs (₹)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_profile.get("monthly_debt_repayments", 4500.0)),
            step=500.0
        )
        emergency_obligations = st.number_input(
            "Emergency Obligations (₹/mo)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_profile.get("emergency_expenses_obligations", 0.0)),
            step=500.0
        )
        
        education_opts = [
            "Secondary (10th)",
            "Higher Secondary (12th)",
            "ITI / Vocational",
            "Diploma",
            "Graduate / B.Com / B.Sc / B.A",
            "B.Tech / BE / STEM Graduate",
            "Post Graduate"
        ]
        curr_edu = current_profile.get("education", "Higher Secondary (12th)")
        edu_idx = education_opts.index(curr_edu) if curr_edu in education_opts else 1
        education = st.selectbox("Education Level", options=education_opts, index=edu_idx)
        
        occupation = st.text_input(
            "Current Role",
            value=str(current_profile.get("occupation", "Salaried / Support Role"))
        )
        
        skills_input = st.text_input(
            "Skills (comma-separated)",
            value=", ".join(current_profile.get("skills", ["Customer Service", "Computer Literacy", "Digital Payments"]))
        )
        
        region_opts = ["Maharashtra", "Tamil Nadu", "Karnataka", "Gujarat", "Uttar Pradesh", "Delhi", "Kerala", "West Bengal", "Other"]
        curr_reg = current_profile.get("region", "Maharashtra")
        reg_idx = region_opts.index(curr_reg) if curr_reg in region_opts else 0
        region = st.selectbox("Region", options=region_opts, index=reg_idx)
        
        btn_update = st.form_submit_button("Apply Changes 🔄", use_container_width=True)
        if btn_update:
            skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
            updated_profile = {
                "monthly_take_home_income": take_home,
                "other_monthly_income": other_income,
                "essential_monthly_expenses": essential_exp,
                "discretionary_expenses": discretionary_exp,
                "current_savings": current_savings,
                "outstanding_debt": outstanding_debt,
                "monthly_debt_repayments": monthly_emi,
                "emergency_expenses_obligations": emergency_obligations,
                "education": education,
                "occupation": occupation,
                "skills": skills_list,
                "region": region,
                "economic_goals": "Build emergency buffer and transition to higher-wage career pathway"
            }
            st.session_state["user_profile"] = updated_profile
            st.success("Twin Profile updated!")
            st.rerun()

# 3. Calculate Indicators on Active Session Profile
active_profile = st.session_state.get("user_profile", current_profile)
indicators = calculate_financial_indicators(active_profile)

# 4. Computed Metrics Output
st.markdown("### 📊 Economic Resilience Assessment")

r_col1, r_col2, r_col3, r_col4 = st.columns(4)

res_score = indicators["resilience_score"]
res_cat = indicators["resilience_category"]
res_badge = "emerald" if res_score >= 70 else ("indigo" if res_score >= 50 else ("amber" if res_score >= 30 else "rose"))

with r_col1:
    render_kpi_card(
        title="Composite Resilience Index",
        value=f"{res_score} / 100",
        subtext=res_cat,
        delta_text=f"{indicators['savings_rate_pct']}% Savings Rate",
        badge_color=res_badge
    )
with r_col2:
    render_kpi_card(
        title="Monthly Net Cash Flow",
        value=format_inr(indicators["monthly_surplus_deficit"]),
        subtext=f"Buffer: {format_inr(indicators['monthly_financial_buffer'])}",
        delta_text="Positive Cashflow" if indicators["monthly_surplus_deficit"] >= 0 else "Operating Deficit",
        badge_color="emerald" if indicators["monthly_surplus_deficit"] >= 0 else "rose"
    )
with r_col3:
    render_kpi_card(
        title="Emergency Runway",
        value=f"{indicators['emergency_fund_months']:.1f} Months",
        subtext=f"Monthly Base: {format_inr(active_profile['essential_monthly_expenses'] + active_profile['monthly_debt_repayments'])}",
        delta_text="6 Mo Recommended",
        badge_color="emerald" if indicators["emergency_fund_months"] >= 6 else "amber"
    )
with r_col4:
    render_kpi_card(
        title="Debt-to-Income (DTI)",
        value=format_pct(indicators["debt_to_income_ratio_pct"]),
        subtext=f"Total Debt: {format_inr(active_profile['outstanding_debt'])}",
        delta_text="Safe Benchmark: <40%",
        badge_color="emerald" if indicators["debt_to_income_ratio_pct"] <= 40 else "rose"
    )

# 5. Resilience Score Progress & Category Badge
st.markdown("---")
prog_col1, prog_col2 = st.columns([3, 1])
with prog_col1:
    st.markdown(f"#### Resilience Gauge: **{res_score} / 100** &bull; <span class='badge badge-{res_badge}'>{res_cat}</span>", unsafe_allow_html=True)
    st.progress(float(min(1.0, max(0.0, res_score / 100.0))))
with prog_col2:
    st.caption(f"Profile Status: **{active_profile.get('occupation', 'Salaried')}** ({active_profile.get('region', 'India')})")
    st.caption("Use the sidebar form to adjust inputs at any time.")

# 6. Visual Breakdown: Cashflow Waterfall + Component Breakdown Chart
st.markdown("---")
c_col1, c_col2 = st.columns([1, 1])

with c_col1:
    st.plotly_chart(
        plot_cashflow_breakdown(
            income=indicators["total_monthly_income"],
            essential=active_profile["essential_monthly_expenses"],
            discretionary=active_profile["discretionary_expenses"],
            emi=active_profile["monthly_debt_repayments"],
            surplus=indicators["monthly_surplus_deficit"]
        ),
        use_container_width=True
    )

with c_col2:
    st.plotly_chart(
        plot_resilience_components(indicators["component_scores"]),
        use_container_width=True
    )

# 7. Risk Factors & Positive Drivers as Distinct Alert Boxes (Member 1 Requirement)
st.markdown("---")
st.markdown("### 🛡️ Diagnostic Findings: Positive Drivers & Risk Factors")

d_col1, d_col2 = st.columns(2)

with d_col1:
    st.markdown("#### ✅ Positive Financial Indicators")
    if indicators["positive_indicators"]:
        for pos in indicators["positive_indicators"]:
            render_alert_box("Positive Indicator", pos, alert_type="success")
    else:
        st.info("No positive drivers identified yet. Increasing savings will unlock positive markers.")

with d_col2:
    st.markdown("#### ⚠️ Resilience Vulnerabilities & Warnings")
    if indicators["risk_factors"]:
        for risk in indicators["risk_factors"]:
            render_alert_box("Resilience Vulnerability", risk, alert_type="warning")
    else:
        render_alert_box("No Critical Vulnerabilities", "Your current cash flow parameters do not exhibit acute distress signals.", alert_type="success")

# 8. Strategic Recommendations as Numbered Action Items
st.markdown("---")
st.markdown("### 🎯 Numbered Action Plan")
if indicators["recommendations"]:
    for idx, rec in enumerate(indicators["recommendations"], start=1):
        st.markdown(
            f"""
            <div class="aayam-card-secondary" style="margin-bottom: 8px;">
                <strong style="color: #10B981; font-size: 1rem;">Action Item {idx}:</strong> 
                <span style="color: #F8FAFC; font-size: 0.92rem; margin-left: 6px;">{rec}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No recommendations needed at this stage.")

render_footer()
