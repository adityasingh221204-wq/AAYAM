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
from src.ui.charts import plot_cashflow_breakdown
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

# 1. Load or Initialize Session Profile
current_profile = st.session_state.get("user_profile", {})

# 2. Input Form Layout (2 Columns)
with st.form("digital_twin_form"):
    st.markdown("### 📥 Profile Parameters")
    f_col1, f_col2 = st.columns(2)
    
    with f_col1:
        st.markdown("#### Cash Inflows & Liquid Assets")
        take_home = st.number_input(
            "Primary Monthly Take-Home Income (₹)",
            min_value=0.0,
            max_value=2000000.0,
            value=float(current_profile.get("monthly_take_home_income", 35000.0)),
            step=1000.0,
            help="Net post-tax salary or primary business withdrawal."
        )
        other_income = st.number_input(
            "Secondary / Other Monthly Income (₹)",
            min_value=0.0,
            max_value=1000000.0,
            value=float(current_profile.get("other_monthly_income", 5000.0)),
            step=500.0,
            help="Rental, freelance, seasonal, or family remittances."
        )
        current_savings = st.number_input(
            "Current Liquid Savings & Deposits (₹)",
            min_value=0.0,
            max_value=50000000.0,
            value=float(current_profile.get("current_savings", 50000.0)),
            step=5000.0,
            help="Immediate accessible bank balance and liquid deposits."
        )
        
        st.markdown("#### Career & Demographic Context")
        education = st.selectbox(
            "Highest Educational Attainment",
            options=[
                "Secondary (10th)",
                "Higher Secondary (12th)",
                "ITI / Vocational",
                "Diploma",
                "Graduate / B.Com / B.Sc / B.A",
                "B.Tech / BE / STEM Graduate",
                "Post Graduate"
            ],
            index=1
        )
        occupation = st.text_input(
            "Current Occupation / Role",
            value=str(current_profile.get("occupation", "Salaried / Support Role"))
        )
        skills_input = st.text_input(
            "Key Skills (comma-separated)",
            value=", ".join(current_profile.get("skills", ["Customer Service", "Computer Literacy", "Digital Payments"]))
        )

    with f_col2:
        st.markdown("#### Living Expenses & Obligations")
        essential_exp = st.number_input(
            "Essential Monthly Living Outflows (₹)",
            min_value=0.0,
            max_value=1000000.0,
            value=float(current_profile.get("essential_monthly_expenses", 20000.0)),
            step=1000.0,
            help="Rent, groceries, utilities, children school fees, healthcare."
        )
        discretionary_exp = st.number_input(
            "Discretionary Monthly Expenses (₹)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_profile.get("discretionary_expenses", 6000.0)),
            step=500.0,
            help="Dining out, entertainment, subscriptions, personal lifestyle."
        )
        
        st.markdown("#### Debt Liabilities")
        outstanding_debt = st.number_input(
            "Total Outstanding Debt (₹)",
            min_value=0.0,
            max_value=10000000.0,
            value=float(current_profile.get("outstanding_debt", 75000.0)),
            step=5000.0,
            help="Total principal remaining on personal, credit card, or vehicle loans."
        )
        monthly_emi = st.number_input(
            "Total Monthly Debt Repayments / EMIs (₹)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_profile.get("monthly_debt_repayments", 4500.0)),
            step=500.0,
            help="Combined monthly EMI obligations."
        )
        emergency_obligations = st.number_input(
            "Other Fixed Monthly Obligations (₹)",
            min_value=0.0,
            max_value=500000.0,
            value=float(current_profile.get("emergency_expenses_obligations", 0.0)),
            step=500.0,
            help="Dependent family medical support or ongoing recurring commitments."
        )
        region = st.selectbox(
            "Geographic Region",
            options=["Maharashtra", "Tamil Nadu", "Karnataka", "Gujarat", "Uttar Pradesh", "Delhi", "Kerala", "West Bengal", "Other"],
            index=0
        )
        
    submitted = st.form_submit_button("Update Economic Twin & Recalculate 🔄")
    
    if submitted:
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
        st.success("Economic Twin updated successfully!")

# 3. Calculate Indicators on Active Session Profile
active_profile = st.session_state["user_profile"]
indicators = calculate_financial_indicators(active_profile)

# 4. Computed Metrics Output
st.markdown("---")
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
        subtext=f"Baseline Outflow: {format_inr(active_profile['essential_monthly_expenses'] + active_profile['monthly_debt_repayments'])}/mo",
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

# 5. Visual Cash Flow Waterfall
st.markdown("---")
cf_col1, cf_col2 = st.columns([3, 2])

with cf_col1:
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

with cf_col2:
    st.markdown("#### Scoring Components")
    pts = indicators["component_scores"]
    st.markdown(f"- **Emergency Runway Buffer:** `{pts['emergency_runway_points']:.1f} / 35.0 pts`")
    st.markdown(f"- **Net Cash Flow Health:** `{pts['cashflow_surplus_points']:.1f} / 30.0 pts`")
    st.markdown(f"- **Debt Burden Manageability:** `{pts['debt_health_points']:.1f} / 25.0 pts`")
    st.markdown(f"- **Income Base Stability:** `{pts['stability_points']:.1f} / 10.0 pts`")
    
    st.markdown("#### Positive Drivers")
    for pos in indicators["positive_indicators"]:
        st.markdown(f"✅ <span style='font-size: 0.88rem; color: #34D399;'>{pos}</span>", unsafe_allow_html=True)
        
    if indicators["risk_factors"]:
        st.markdown("#### Resilience Vulnerabilities")
        for risk in indicators["risk_factors"]:
            st.markdown(f"⚠️ <span style='font-size: 0.88rem; color: #FBBF24;'>{risk}</span>", unsafe_allow_html=True)

# 6. Strategic Recommendations
st.markdown("---")
st.markdown("### 🎯 Decision-Support Recommendations")
for rec in indicators["recommendations"]:
    st.markdown(f"&bull; {rec}")

render_footer()
