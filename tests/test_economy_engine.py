"""
Tests for AAYAM Economy Engine (src/engines/economy.py)
Covers: financial indicators, resilience scoring, risk classification, edge cases.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engines.economy import calculate_financial_indicators


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def healthy_profile():
    return {
        "monthly_take_home_income": 80000.0,
        "other_monthly_income": 10000.0,
        "essential_monthly_expenses": 25000.0,
        "discretionary_expenses": 8000.0,
        "current_savings": 500000.0,
        "outstanding_debt": 0.0,
        "monthly_debt_repayments": 0.0,
        "emergency_expenses_obligations": 0.0,
    }


@pytest.fixture
def stressed_profile():
    return {
        "monthly_take_home_income": 25000.0,
        "other_monthly_income": 0.0,
        "essential_monthly_expenses": 22000.0,
        "discretionary_expenses": 5000.0,
        "current_savings": 5000.0,
        "outstanding_debt": 120000.0,
        "monthly_debt_repayments": 6000.0,
        "emergency_expenses_obligations": 2000.0,
    }


@pytest.fixture
def demo_profile():
    """Default session demo profile used in app.py."""
    return {
        "monthly_take_home_income": 35000.0,
        "other_monthly_income": 5000.0,
        "essential_monthly_expenses": 20000.0,
        "discretionary_expenses": 6000.0,
        "current_savings": 50000.0,
        "outstanding_debt": 75000.0,
        "monthly_debt_repayments": 4500.0,
        "emergency_expenses_obligations": 0.0,
    }


@pytest.fixture
def zero_income_profile():
    return {
        "monthly_take_home_income": 0.0,
        "other_monthly_income": 0.0,
        "essential_monthly_expenses": 15000.0,
        "discretionary_expenses": 0.0,
        "current_savings": 30000.0,
        "outstanding_debt": 0.0,
        "monthly_debt_repayments": 0.0,
        "emergency_expenses_obligations": 0.0,
    }


# ─── Return Structure Tests ───────────────────────────────────────────────────

class TestReturnStructure:
    """Verify that the function always returns a complete, well-formed dict."""

    def test_returns_dict(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        assert isinstance(result, dict)

    def test_required_keys_present(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        required_keys = [
            "total_monthly_income", "total_monthly_expenses", "total_monthly_outflows",
            "monthly_surplus_deficit", "savings_rate_pct", "emergency_fund_months",
            "debt_to_income_ratio_pct", "monthly_financial_buffer", "resilience_score",
            "resilience_category", "component_scores", "risk_factors",
            "positive_indicators", "recommendations", "validation_errors", "disclaimer",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_component_scores_structure(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        cs = result["component_scores"]
        assert "emergency_runway_points" in cs
        assert "cashflow_surplus_points" in cs
        assert "debt_health_points" in cs
        assert "stability_points" in cs

    def test_empty_profile_does_not_crash(self):
        result = calculate_financial_indicators({})
        assert isinstance(result, dict)
        assert "resilience_score" in result

    def test_none_profile_does_not_crash(self):
        result = calculate_financial_indicators(None)
        assert isinstance(result, dict)

    def test_non_dict_profile_does_not_crash(self):
        result = calculate_financial_indicators("not a dict")
        assert isinstance(result, dict)


# ─── Cash Flow Calculation Tests ─────────────────────────────────────────────

class TestCashFlowCalculations:
    def test_total_income_is_sum(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        assert result["total_monthly_income"] == pytest.approx(90000.0, abs=1.0)

    def test_net_surplus_computed_correctly(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        # income=90k, outflows = 25k+8k = 33k → surplus = 57k
        assert result["monthly_surplus_deficit"] == pytest.approx(57000.0, abs=10.0)

    def test_savings_rate_above_zero_with_surplus(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        assert result["savings_rate_pct"] > 0

    def test_deficit_when_stressed(self, stressed_profile):
        result = calculate_financial_indicators(stressed_profile)
        assert result["monthly_surplus_deficit"] < 0

    def test_negative_income_clamped_to_zero(self):
        profile = {"monthly_take_home_income": -5000.0}
        result = calculate_financial_indicators(profile)
        assert result["total_monthly_income"] == 0.0


# ─── Emergency Fund Tests ─────────────────────────────────────────────────────

class TestEmergencyFund:
    def test_strong_fund_healthy_profile(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        assert result["emergency_fund_months"] >= 6.0

    def test_low_fund_stressed_profile(self, stressed_profile):
        result = calculate_financial_indicators(stressed_profile)
        assert result["emergency_fund_months"] < 1.0

    def test_zero_savings_gives_zero_months(self):
        profile = {"monthly_take_home_income": 30000.0, "current_savings": 0.0,
                   "essential_monthly_expenses": 10000.0}
        result = calculate_financial_indicators(profile)
        assert result["emergency_fund_months"] == 0.0


# ─── Debt-to-Income Tests ─────────────────────────────────────────────────────

class TestDebtToIncome:
    def test_dti_zero_when_no_debt(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        assert result["debt_to_income_ratio_pct"] == 0.0

    def test_dti_correct_for_demo_profile(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        # EMI=4500, income=40000 → 11.25%
        assert result["debt_to_income_ratio_pct"] == pytest.approx(11.25, abs=0.5)

    def test_dti_high_when_excessive_emi(self):
        profile = {"monthly_take_home_income": 20000.0, "monthly_debt_repayments": 12000.0}
        result = calculate_financial_indicators(profile)
        assert result["debt_to_income_ratio_pct"] == pytest.approx(60.0, abs=0.5)

    def test_dti_100_when_zero_income_with_debt(self):
        profile = {"monthly_debt_repayments": 5000.0, "monthly_take_home_income": 0.0}
        result = calculate_financial_indicators(profile)
        assert result["debt_to_income_ratio_pct"] == 100.0


# ─── Resilience Score Tests ───────────────────────────────────────────────────

class TestResilienceScore:
    def test_score_in_range(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        assert 0.0 <= result["resilience_score"] <= 100.0

    def test_healthy_profile_high_resilience(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        assert result["resilience_score"] >= 70.0
        assert result["resilience_category"] == "High Resilience"

    def test_stressed_profile_vulnerable(self, stressed_profile):
        result = calculate_financial_indicators(stressed_profile)
        assert result["resilience_score"] < 50.0
        assert result["resilience_category"] in ("Financially Vulnerable", "Critical Stress")

    def test_component_scores_do_not_exceed_max(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        cs = result["component_scores"]
        assert cs["emergency_runway_points"] <= 35.0
        assert cs["cashflow_surplus_points"] <= 30.0
        assert cs["debt_health_points"] <= 25.0
        assert cs["stability_points"] <= 10.0


# ─── Risk Factor & Recommendation Tests ──────────────────────────────────────

class TestRiskNarratives:
    def test_deficit_generates_risk_factor(self, stressed_profile):
        result = calculate_financial_indicators(stressed_profile)
        assert len(result["risk_factors"]) > 0

    def test_healthy_profile_has_positive_indicators(self, healthy_profile):
        result = calculate_financial_indicators(healthy_profile)
        assert len(result["positive_indicators"]) > 0

    def test_recommendations_is_list(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        assert isinstance(result["recommendations"], list)

    def test_disclaimer_non_empty(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        assert isinstance(result["disclaimer"], str)
        assert len(result["disclaimer"]) > 20

    def test_zero_income_triggers_income_risk(self, zero_income_profile):
        result = calculate_financial_indicators(zero_income_profile)
        combined = " ".join(result["risk_factors"]).lower()
        assert "income" in combined

    def test_high_dti_triggers_debt_risk(self):
        profile = {
            "monthly_take_home_income": 30000.0,
            "monthly_debt_repayments": 18000.0,
            "essential_monthly_expenses": 10000.0
        }
        res = calculate_financial_indicators(profile)
        assert res["debt_to_income_ratio_pct"] == 60.0
        assert any("debt" in r.lower() or "dti" in r.lower() for r in res["risk_factors"])

    def test_short_runway_triggers_runway_recommendation(self):
        profile = {
            "monthly_take_home_income": 40000.0,
            "essential_monthly_expenses": 25000.0,
            "current_savings": 5000.0
        }
        res = calculate_financial_indicators(profile)
        assert res["emergency_fund_months"] < 1.0
        assert any("emergency" in rec.lower() for rec in res["recommendations"])

    def test_component_scores_keys_present(self, demo_profile):
        result = calculate_financial_indicators(demo_profile)
        expected_keys = {"emergency_runway_points", "cashflow_surplus_points", "debt_health_points", "stability_points"}
        assert set(result["component_scores"].keys()) == expected_keys

    def test_positive_savings_rate_bounded(self):
        profile = {
            "monthly_take_home_income": 50000.0,
            "essential_monthly_expenses": 15000.0,
            "discretionary_expenses": 5000.0
        }
        res = calculate_financial_indicators(profile)
        assert 0.0 <= res["savings_rate_pct"] <= 100.0
        assert res["savings_rate_pct"] == 60.0

    def test_negative_input_sanitization(self):
        profile = {
            "monthly_take_home_income": -1000.0,
            "essential_monthly_expenses": -500.0,
            "current_savings": -100.0
        }
        res = calculate_financial_indicators(profile)
        assert res["total_monthly_income"] == 0.0
        assert res["total_monthly_expenses"] == 0.0
        assert res["resilience_score"] >= 0.0

    def test_extreme_wealth_caps_score_100(self):
        profile = {
            "monthly_take_home_income": 500000.0,
            "essential_monthly_expenses": 50000.0,
            "current_savings": 5000000.0,
            "outstanding_debt": 0.0,
            "monthly_debt_repayments": 0.0
        }
        res = calculate_financial_indicators(profile)
        assert res["resilience_score"] <= 100.0
        assert res["resilience_category"] == "High Resilience"

