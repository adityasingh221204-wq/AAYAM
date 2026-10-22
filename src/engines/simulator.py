"""
AAYAM - ArthSim: Economic Scenario Simulator Engine
Implements canonical contract:
    simulate_economic_scenario(profile: dict, scenario: dict) -> dict
Models deterministic multi-month trajectories under income loss, fraud shock,
business investments, and inflation stress.
"""
from src.engines.economy import calculate_financial_indicators
from src.utils.logging_config import logger


def simulate_economic_scenario(profile: dict, scenario: dict) -> dict:
    """
    Simulate economic trajectories over time comparing baseline vs shock scenario.
    
    Args:
        profile: User profile dictionary.
        scenario: Scenario parameters:
            - scenario_type: str ("fraud_loss", "job_loss", "income_shock", "medical_emergency", "business_startup", "custom")
            - income_change_pct: float (e.g. -30.0 for 30% salary cut, -100.0 for job loss)
            - lump_sum_loss_inr: float (one-time financial shock, e.g. 50000.0)
            - expense_change_pct: float (e.g. 15.0 for inflation)
            - new_monthly_expense_inr: float (recurring addition, e.g. 5000.0)
            - duration_months: int (time horizon, default 12, max 60)
            - recovery_delay_months: int (months before income begins recovery, default 0)
            
    Returns:
        dict: Side-by-side trajectory records, depletion timelines, and resilience comparisons.
    """
    baseline_indicators = calculate_financial_indicators(profile)
    
    # Extract baseline figures
    b_income = baseline_indicators["total_monthly_income"]
    b_expenses = baseline_indicators["total_monthly_outflows"]
    b_savings = max(0.0, float(profile.get("current_savings") or 0.0))
    
    # Extract scenario adjustments
    s_type = scenario.get("scenario_type", "custom")
    duration = min(60, max(3, int(scenario.get("duration_months", 12))))
    income_change_pct = float(scenario.get("income_change_pct", 0.0))
    lump_sum_loss = max(0.0, float(scenario.get("lump_sum_loss_inr", 0.0)))
    expense_change_pct = float(scenario.get("expense_change_pct", 0.0))
    new_monthly_expense = max(0.0, float(scenario.get("new_monthly_expense_inr", 0.0)))
    recovery_delay = max(0, int(scenario.get("recovery_delay_months", 0)))
    
    # Compute modified scenario cash flows
    s_income_mod = max(0.0, b_income * (1.0 + income_change_pct / 100.0))
    s_expenses_mod = max(0.0, b_expenses * (1.0 + expense_change_pct / 100.0)) + new_monthly_expense
    
    baseline_traj = []
    scenario_traj = []
    
    curr_b_savings = b_savings
    curr_s_savings = max(0.0, b_savings - lump_sum_loss)
    
    months_to_depletion = None
    recovered_month = None
    
    for m in range(1, duration + 1):
        # Month 1-based simulation
        # Baseline step
        b_net = b_income - b_expenses
        curr_b_savings = max(0.0, curr_b_savings + b_net)
        
        baseline_traj.append({
            "month": m,
            "income": round(b_income, 2),
            "expenses": round(b_expenses, 2),
            "net_cashflow": round(b_net, 2),
            "savings_balance": round(curr_b_savings, 2)
        })
        
        # Scenario step (with optional recovery after delay)
        if recovery_delay > 0 and m > recovery_delay:
            # Gradual 50% recovery of lost income
            active_s_income = s_income_mod + (b_income - s_income_mod) * 0.50
        else:
            active_s_income = s_income_mod
            
        s_net = active_s_income - s_expenses_mod
        curr_s_savings = max(0.0, curr_s_savings + s_net)
        
        if curr_s_savings == 0.0 and months_to_depletion is None and b_savings > 0:
            months_to_depletion = m
            
        if curr_s_savings >= b_savings and recovered_month is None and m > 1:
            recovered_month = m
            
        scenario_traj.append({
            "month": m,
            "income": round(active_s_income, 2),
            "expenses": round(s_expenses_mod, 2),
            "net_cashflow": round(s_net, 2),
            "savings_balance": round(curr_s_savings, 2)
        })
        
    final_b_savings = baseline_traj[-1]["savings_balance"]
    final_s_savings = scenario_traj[-1]["savings_balance"]
    net_impact = round(final_s_savings - final_b_savings, 2)
    
    # Scenario Profile indicators
    scenario_profile = dict(profile)
    scenario_profile["monthly_take_home_income"] = s_income_mod
    scenario_profile["current_savings"] = max(0.0, b_savings - lump_sum_loss)
    scenario_profile["essential_monthly_expenses"] = s_expenses_mod
    
    scenario_indicators = calculate_financial_indicators(scenario_profile)
    resilience_shift = round(scenario_indicators["resilience_score"] - baseline_indicators["resilience_score"], 1)
    
    assumptions = [
        f"Deterministic simulation over a {duration}-month horizon.",
        f"Lump-sum loss of ₹{lump_sum_loss:,.0f} deducted immediately in Month 1." if lump_sum_loss > 0 else "No immediate lump-sum capital deduction.",
        f"Monthly income adjusted by {income_change_pct:+.1f}%." if income_change_pct != 0 else "Base income remains stable.",
        f"Monthly living outflows adjusted by {expense_change_pct:+.1f}% plus ₹{new_monthly_expense:,.0f} fixed additions." if (expense_change_pct != 0 or new_monthly_expense > 0) else "Living outflows remain at current baseline.",
        "Zero investment yield or inflation compounding applied over horizon to preserve conservative safety margins."
    ]
    
    return {
        "scenario_type": s_type,
        "duration_months": duration,
        "baseline_trajectory": baseline_traj,
        "scenario_trajectory": scenario_traj,
        "months_to_depletion": months_to_depletion,
        "recovery_months": recovered_month,
        "net_financial_impact_inr": net_impact,
        "initial_savings_loss_inr": round(lump_sum_loss, 2),
        "baseline_resilience_score": baseline_indicators["resilience_score"],
        "scenario_resilience_score": scenario_indicators["resilience_score"],
        "resilience_shift": resilience_shift,
        "baseline_indicators": baseline_indicators,
        "scenario_indicators": scenario_indicators,
        "assumptions": assumptions,
        "disclaimer": "ArthSim provides deterministic illustrative projections for decision-support and stress-testing. Actual financial outcomes vary with economic conditions and unexpected obligations."
    }
