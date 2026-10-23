"""
AAYAM - Page 5: ArthSim: Economic Scenario Simulator
Interactive deterministic what-if modeling for income shocks, fraud losses, and recovery runways.
"""
import streamlit as st
import pandas as pd
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.ui.charts import plot_scenario_trajectories
from src.engines.simulator import simulate_economic_scenario
from src.utils.formatting import format_inr, format_pct

st.set_page_config(page_title="ArthSim — AAYAM", page_icon="⚡", layout="wide")
apply_theme()

render_header(
    title="ArthSim: Economic Scenario Simulator",
    subtitle="Simulate financial resilience trajectories under income loss, fraud shocks, or enterprise ventures.",
    badge_text="Module 5",
    badge_type="amber"
)

render_alert_box(
    title="Simulation Methodology",
    message="ArthSim applies deterministic, multi-period cash flow equations to test baseline stability. Projections represent stress-test scenarios, not guarantees or certified actuarial forecasts.",
    alert_type="info"
)

# 1. Load Active Profile
profile = st.session_state.get("user_profile", {})

# 2. Scenario Configuration Controls (Member 1 Enhanced Specification)
st.markdown("### 🎛️ Scenario Simulation Parameters")

scenario_options = {
    "job_loss": "Temporary Job Loss: 100% income drop with recovery runway",
    "fraud_loss": "Cyber Fraud Shock: Instant ₹50,000 unauthorized loss",
    "medical_emergency": "Medical Emergency: ₹75,000 lump sum + ₹8,000 monthly care",
    "business_startup": "Micro-Enterprise Startup: ₹45,000 capital + ₹5,000 monthly cost",
    "inflation_shock": "Inflation Shock: Living costs rise by 20%",
    "custom": "Custom Scenario (Full Parameter Control)"
}

selected_key = st.selectbox(
    "Choose Shock / Investment Scenario Type:",
    options=list(scenario_options.keys()),
    format_func=lambda k: scenario_options[k]
)

# Preset initial values based on selection
if selected_key == "fraud_loss":
    def_lump = 50000.0
    def_inc_pct = 0.0
    def_exp_pct = 0.0
    def_new_exp = 0.0
    def_delay = 0
elif selected_key == "job_loss":
    def_lump = 0.0
    def_inc_pct = -100.0
    def_exp_pct = 0.0
    def_new_exp = 0.0
    def_delay = 3
elif selected_key == "medical_emergency":
    def_lump = 75000.0
    def_inc_pct = 0.0
    def_exp_pct = 10.0
    def_new_exp = 8000.0
    def_delay = 0
elif selected_key == "business_startup":
    def_lump = 45000.0
    def_inc_pct = 20.0
    def_exp_pct = 0.0
    def_new_exp = 5000.0
    def_delay = 2
elif selected_key == "inflation_shock":
    def_lump = 0.0
    def_inc_pct = 0.0
    def_exp_pct = 20.0
    def_new_exp = 0.0
    def_delay = 0
else:
    def_lump = 0.0
    def_inc_pct = 0.0
    def_exp_pct = 0.0
    def_new_exp = 0.0
    def_delay = 0

c1, c2, c3 = st.columns(3)
with c1:
    lump_sum_loss = st.slider(
        "Immediate Lump-Sum Deduction (₹)",
        min_value=0.0,
        max_value=250000.0,
        value=float(def_lump),
        step=5000.0,
        help="One-off financial shock, such as fraud theft or medical bill."
    )
    duration_months = st.slider(
        "Simulation Time Horizon (Months)",
        min_value=3,
        max_value=36,
        value=12,
        help="Duration to project future savings balances."
    )

with c2:
    income_change_pct = st.slider(
        "Monthly Income Adjustment (%)",
        min_value=-100.0,
        max_value=100.0,
        value=float(def_inc_pct),
        step=5.0,
        help="-100% represents complete job loss; +20% represents promotion or business revenue."
    )
    recovery_delay = st.slider(
        "Income Recovery Delay (Months)",
        min_value=0,
        max_value=12,
        value=int(def_delay),
        help="Number of months of complete shock before partial (50%) income recovery occurs."
    )

with c3:
    expense_change_pct = st.slider(
        "Living Cost Change (%)",
        min_value=-50.0,
        max_value=50.0,
        value=float(def_exp_pct),
        step=5.0,
        help="Percentage change in living costs due to inflation or austerity."
    )
    new_monthly_expense = st.slider(
        "New Recurring Outflow (₹/mo)",
        min_value=0.0,
        max_value=50000.0,
        value=float(def_new_exp),
        step=1000.0,
        help="Ongoing new expenditure (e.g. loan EMI, equipment lease)."
    )

scenario_dict = {
    "scenario_type": selected_key,
    "duration_months": duration_months,
    "income_change_pct": income_change_pct,
    "lump_sum_loss_inr": lump_sum_loss,
    "expense_change_pct": expense_change_pct,
    "new_monthly_expense_inr": new_monthly_expense,
    "recovery_delay_months": recovery_delay
}

# 3. Execute Simulation via Canonical Engine
sim_results = simulate_economic_scenario(profile, scenario_dict)

# 4. Display Simulation KPIs
st.markdown("---")
st.markdown("### 📊 Scenario Stress-Test Indicators")

k1, k2, k3, k4 = st.columns(4)

net_impact = sim_results["net_financial_impact_inr"]
impact_color = "emerald" if net_impact >= 0 else "rose"

with k1:
    render_kpi_card(
        title="Net Wealth Impact",
        value=format_inr(net_impact),
        subtext=f"At Month {duration_months}",
        delta_text="Capital Accrual" if net_impact >= 0 else "Net Financial Loss",
        badge_color=impact_color
    )
with k2:
    depletion = sim_results["months_to_depletion"]
    if depletion:
        dep_val = f"Month {depletion}"
        dep_sub = "Liquid reserves exhaust"
        dep_color = "rose"
    else:
        dep_val = "Never"
        dep_sub = "Reserves remain positive"
        dep_color = "emerald"
        
    render_kpi_card(
        title="Months to Depletion",
        value=dep_val,
        subtext=dep_sub,
        delta_text="Zero Liquidity Event" if depletion else "Solvent Horizon",
        badge_color=dep_color
    )
with k3:
    res_shift = sim_results["resilience_shift"]
    shift_sign = "+" if res_shift > 0 else ""
    shift_color = "emerald" if res_shift >= 0 else "rose"
    render_kpi_card(
        title="Resilience Shift",
        value=f"{shift_sign}{res_shift} pts",
        subtext=f"{sim_results['baseline_resilience_score']} → {sim_results['scenario_resilience_score']}",
        delta_text=f"{shift_sign}{res_shift} pts shift",
        badge_color=shift_color
    )
with k4:
    rec_month = sim_results["recovery_months"]
    rec_val = f"Month {rec_month}" if rec_month else "Pending"
    render_kpi_card(
        title="Capital Recovery",
        value=rec_val,
        subtext="To pre-shock savings level",
        delta_text="Restored" if rec_month else "Unrecovered in Horizon",
        badge_color="emerald" if rec_month else "amber"
    )

# Highlight alert for depletion
if depletion:
    render_alert_box(
        title=f"Critical Liquidity Event: Capital Exhaustion at Month {depletion}",
        message=f"Under this shock scenario, your liquid reserves will reach ₹0 by Month {depletion}. Immediate contingency planning, credit line access, or emergency budget cutbacks are required before this horizon.",
        alert_type="danger"
    )

# 5. Side-by-side Trajectory Chart
st.markdown("---")
st.markdown("### 📈 Savings Balance Trajectory: Baseline vs. Scenario")
st.plotly_chart(
    plot_scenario_trajectories(
        baseline_traj=sim_results["baseline_trajectory"],
        scenario_traj=sim_results["scenario_trajectory"],
        duration=duration_months
    ),
    use_container_width=True
)

# 6. Detailed Monthly Comparison Table
with st.expander("🔍 View Month-by-Month Financial Ledger Table"):
    df_b = pd.DataFrame(sim_results["baseline_trajectory"])
    df_s = pd.DataFrame(sim_results["scenario_trajectory"])
    
    df_merged = pd.DataFrame({
        "Month": df_b["month"],
        "Baseline Net Cashflow (₹)": df_b["net_cashflow"],
        "Baseline Savings (₹)": df_b["savings_balance"],
        "Scenario Net Cashflow (₹)": df_s["net_cashflow"],
        "Scenario Savings (₹)": df_s["savings_balance"],
        "Monthly Difference (₹)": df_s["savings_balance"] - df_b["savings_balance"]
    })
    st.dataframe(df_merged, use_container_width=True, hide_index=True)

# 7. Documented Assumptions
st.markdown("#### Documented Simulation Assumptions")
for a in sim_results["assumptions"]:
    st.caption(f"&bull; {a}")

render_footer()
