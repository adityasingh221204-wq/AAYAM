"""
AAYAM - Economic & Financial Twin Engine
Implements canonical contract:
    calculate_financial_indicators(profile: dict) -> dict
Calculates cash flow, emergency buffers, debt burdens, and composite resilience index.
"""
from src.data.validators import validate_financial_profile
from src.utils.logging_config import logger


def calculate_financial_indicators(profile: dict) -> dict:
    """
    Calculate transparent financial indicators and economic resilience metrics.
    
    Args:
        profile: Dictionary containing user financial fields:
            - monthly_take_home_income (float, default 0.0)
            - other_monthly_income (float, default 0.0)
            - essential_monthly_expenses (float, default 0.0)
            - discretionary_expenses (float, default 0.0)
            - current_savings (float, default 0.0)
            - outstanding_debt (float, default 0.0)
            - monthly_debt_repayments (float, default 0.0)
            - emergency_expenses_obligations (float, default 0.0)
            - education (str, optional)
            - occupation (str, optional)
            - region (str, optional)
            
    Returns:
        dict: Detailed financial indicator dictionary.
    """
    if not isinstance(profile, dict):
        logger.warning("Invalid profile passed; defaulting to empty profile.")
        profile = {}
        
    is_valid, validation_errors = validate_financial_profile(profile)
    
    # Safe float extraction with non-negative constraints
    take_home = max(0.0, float(profile.get("monthly_take_home_income") or 0.0))
    other_income = max(0.0, float(profile.get("other_monthly_income") or 0.0))
    essential_exp = max(0.0, float(profile.get("essential_monthly_expenses") or 0.0))
    discretionary_exp = max(0.0, float(profile.get("discretionary_expenses") or 0.0))
    current_savings = max(0.0, float(profile.get("current_savings") or 0.0))
    debt = max(0.0, float(profile.get("outstanding_debt") or 0.0))
    emi_payments = max(0.0, float(profile.get("monthly_debt_repayments") or 0.0))
    emergency_obligations = max(0.0, float(profile.get("emergency_expenses_obligations") or 0.0))
    
    # 1. Total Cash Flows
    total_income = take_home + other_income
    total_living_expenses = essential_exp + discretionary_exp
    total_outflows = total_living_expenses + emi_payments + emergency_obligations
    net_surplus_deficit = total_income - total_outflows
    
    # 2. Savings Rate (% of total income)
    if total_income > 0:
        savings_rate_pct = round((max(0.0, net_surplus_deficit) / total_income) * 100.0, 1)
    else:
        savings_rate_pct = 0.0
        
    # 3. Emergency Fund Runway (Months)
    monthly_runway_base = essential_exp + emi_payments
    if monthly_runway_base > 0:
        emergency_fund_months = round(current_savings / monthly_runway_base, 2)
    elif current_savings > 0:
        emergency_fund_months = 12.0  # Safe cap if zero expenses
    else:
        emergency_fund_months = 0.0
        
    # 4. Debt Burden Ratio (Debt service to income)
    if total_income > 0:
        dti_pct = round((emi_payments / total_income) * 100.0, 1)
    else:
        dti_pct = 100.0 if emi_payments > 0 else 0.0
        
    # 5. Financial Buffer (Unallocated surplus after essentials & EMI)
    monthly_buffer = total_income - (essential_exp + emi_payments)
    
    # 6. Composite Economic Resilience Score (0 - 100 Scale)
    # Factor A: Emergency Fund Runway (Max 35 pts for 6+ months)
    pts_emergency = min(35.0, (emergency_fund_months / 6.0) * 35.0)
    
    # Factor B: Net Cash Flow Surplus (Max 30 pts for 20%+ savings rate)
    if total_income > 0 and net_surplus_deficit > 0:
        pts_surplus = min(30.0, (net_surplus_deficit / (0.20 * total_income)) * 30.0)
    elif total_income > 0 and net_surplus_deficit <= 0:
        # Deficit penalization
        deficit_ratio = abs(net_surplus_deficit) / total_income
        pts_surplus = max(0.0, 10.0 - (deficit_ratio * 20.0))
    else:
        pts_surplus = 5.0
        
    # Factor C: Debt Burden Health (Max 25 pts for DTI < 25%, 0 pts if DTI > 50%)
    if dti_pct <= 20.0:
        pts_debt = 25.0
    elif dti_pct <= 40.0:
        pts_debt = 25.0 - ((dti_pct - 20.0) / 20.0) * 15.0  # 25 down to 10
    elif dti_pct <= 60.0:
        pts_debt = max(2.0, 10.0 - ((dti_pct - 40.0) / 20.0) * 8.0)
    else:
        pts_debt = 0.0
        
    # Factor D: Income Stability Base (Max 10 pts)
    pts_stability = 10.0 if total_income > 0 else 0.0
    
    resilience_score = round(pts_emergency + pts_surplus + pts_debt + pts_stability, 1)
    
    # Classification
    if resilience_score >= 75.0:
        resilience_category = "High Resilience"
    elif resilience_score >= 50.0:
        resilience_category = "Moderate Resilience"
    elif resilience_score >= 30.0:
        resilience_category = "Financially Vulnerable"
    else:
        resilience_category = "Critical Stress"
        
    # Narrative Risk Factors & Positive Indicators
    risk_factors = []
    positive_indicators = []
    recommendations = []
    
    if net_surplus_deficit < 0:
        risk_factors.append(f"Operating at a monthly deficit of ₹{abs(net_surplus_deficit):,.0f}. Depleting capital reserves each month.")
        recommendations.append("Audit discretionary expenditures and defer non-essential outlays until positive cash flow is established.")
    else:
        positive_indicators.append(f"Generating positive monthly cash flow surplus of ₹{net_surplus_deficit:,.0f} ({savings_rate_pct}% savings rate).")
        
    if emergency_fund_months < 1.0:
        risk_factors.append("Emergency fund covers less than 1 month of essential expenses. High vulnerability to income shocks or medical emergencies.")
        recommendations.append("Prioritize building a minimum 3-month liquid emergency fund in a high-interest savings or liquid mutual fund.")
    elif emergency_fund_months >= 6.0:
        positive_indicators.append(f"Strong liquidity buffer: {emergency_fund_months:.1f} months of essential expenses secured.")
    else:
        recommendations.append(f"Expand emergency fund from {emergency_fund_months:.1f} months toward the 6.0-month recommended baseline.")
        
    if dti_pct > 40.0:
        risk_factors.append(f"Debt-to-Income (DTI) ratio is {dti_pct}%, exceeding the prudent 40% threshold.")
        recommendations.append("Avoid taking additional consumer credit; consider debt avalanche/snowball repayment strategies.")
    elif debt > 0:
        positive_indicators.append(f"Manageable debt obligations (DTI: {dti_pct}%).")
    else:
        positive_indicators.append("Debt-free balance sheet: 0% debt-service burden.")
        
    if total_income == 0:
        risk_factors.append("Zero current income recorded. Immediate focus required on active livelihood or income replacement.")
        recommendations.append("Explore Opportunity Pathways for fast-track upskilling, freelancing, or employment matching.")

    return {
        "total_monthly_income": round(total_income, 2),
        "total_monthly_expenses": round(total_living_expenses, 2),
        "total_monthly_outflows": round(total_outflows, 2),
        "monthly_surplus_deficit": round(net_surplus_deficit, 2),
        "savings_rate_pct": savings_rate_pct,
        "emergency_fund_months": emergency_fund_months,
        "debt_to_income_ratio_pct": dti_pct,
        "monthly_financial_buffer": round(monthly_buffer, 2),
        "resilience_score": resilience_score,
        "resilience_category": resilience_category,
        "component_scores": {
            "emergency_runway_points": round(pts_emergency, 1),
            "cashflow_surplus_points": round(pts_surplus, 1),
            "debt_health_points": round(pts_debt, 1),
            "stability_points": round(pts_stability, 1)
        },
        "risk_factors": risk_factors,
        "positive_indicators": positive_indicators,
        "recommendations": recommendations,
        "validation_errors": validation_errors,
        "disclaimer": "AAYAM financial indicators are decision-support measures for scenario modeling and educational planning, not professional financial advice or credit scoring."
    }
