"""
Tests for AAYAM ArthSim Simulator Engine (src/engines/simulator.py)
Covers: trajectory generation, depletion detection, resilience shift, assumptions.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engines.simulator import simulate_economic_scenario


@pytest.fixture
def base_profile():
    return {
        "monthly_take_home_income": 40000.0,
        "other_monthly_income": 0.0,
        "essential_monthly_expenses": 20000.0,
        "discretionary_expenses": 5000.0,
        "current_savings": 60000.0,
        "outstanding_debt": 50000.0,
        "monthly_debt_repayments": 3000.0,
        "emergency_expenses_obligations": 0.0,
    }


class TestReturnStructure:
    def test_returns_dict(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 6})
        assert isinstance(result, dict)

    def test_required_keys_present(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 6})
        required = [
            "scenario_type", "duration_months", "baseline_trajectory",
            "scenario_trajectory", "months_to_depletion", "net_financial_impact_inr",
            "baseline_resilience_score", "scenario_resilience_score",
            "resilience_shift", "assumptions", "disclaimer"
        ]
        for key in required:
            assert key in result, f"Missing key: {key}"

    def test_trajectory_length_matches_duration(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 12})
        assert len(result["baseline_trajectory"]) == 12
        assert len(result["scenario_trajectory"]) == 12

    def test_each_trajectory_entry_has_required_fields(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 6})
        for entry in result["baseline_trajectory"]:
            assert "month" in entry
            assert "income" in entry
            assert "expenses" in entry
            assert "net_cashflow" in entry
            assert "savings_balance" in entry


class TestDurationClamping:
    def test_duration_minimum_clamped_to_3(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 1})
        assert result["duration_months"] >= 3

    def test_duration_maximum_clamped_to_60(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 999})
        assert result["duration_months"] <= 60


class TestJobLossScenario:
    def test_job_loss_causes_savings_depletion(self, base_profile):
        result = simulate_economic_scenario(
            base_profile,
            {"scenario_type": "job_loss", "income_change_pct": -100.0, "duration_months": 12}
        )
        assert result["months_to_depletion"] is not None
        assert result["months_to_depletion"] <= 12

    def test_job_loss_lowers_resilience_score(self, base_profile):
        result = simulate_economic_scenario(
            base_profile,
            {"scenario_type": "job_loss", "income_change_pct": -100.0, "duration_months": 12}
        )
        assert result["resilience_shift"] < 0

    def test_scenario_income_zero_when_full_loss(self, base_profile):
        result = simulate_economic_scenario(
            base_profile,
            {"income_change_pct": -100.0, "duration_months": 6}
        )
        # First month scenario income should be 0
        assert result["scenario_trajectory"][0]["income"] == pytest.approx(0.0, abs=1.0)


class TestFraudLossScenario:
    def test_lump_sum_loss_reduces_initial_savings(self, base_profile):
        result = simulate_economic_scenario(
            base_profile,
            {"scenario_type": "fraud_loss", "lump_sum_loss_inr": 30000.0, "duration_months": 6}
        )
        # Baseline savings at month 1 should be higher than scenario
        assert result["baseline_trajectory"][0]["savings_balance"] > result["scenario_trajectory"][0]["savings_balance"]

    def test_lump_sum_loss_logged_in_result(self, base_profile):
        result = simulate_economic_scenario(
            base_profile,
            {"lump_sum_loss_inr": 45000.0, "duration_months": 6}
        )
        assert result["initial_savings_loss_inr"] == pytest.approx(45000.0, abs=1.0)


class TestInflationScenario:
    def test_expense_increase_reduces_net_cashflow(self, base_profile):
        result_baseline = simulate_economic_scenario(base_profile, {"duration_months": 6})
        result_inflation = simulate_economic_scenario(
            base_profile,
            {"expense_change_pct": 20.0, "duration_months": 6}
        )
        # Scenario net cashflow should be lower than baseline
        baseline_net = result_baseline["scenario_trajectory"][0]["net_cashflow"]
        inflation_net = result_inflation["scenario_trajectory"][0]["net_cashflow"]
        assert inflation_net < baseline_net


class TestBaselineStability:
    def test_baseline_savings_non_negative(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 12})
        for entry in result["baseline_trajectory"]:
            assert entry["savings_balance"] >= 0.0

    def test_scenario_savings_non_negative(self, base_profile):
        result = simulate_economic_scenario(
            base_profile,
            {"income_change_pct": -50.0, "duration_months": 12}
        )
        for entry in result["scenario_trajectory"]:
            assert entry["savings_balance"] >= 0.0


class TestAssumptions:
    def test_assumptions_is_list(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 6})
        assert isinstance(result["assumptions"], list)
        assert len(result["assumptions"]) > 0

    def test_disclaimer_present(self, base_profile):
        result = simulate_economic_scenario(base_profile, {"duration_months": 6})
        assert isinstance(result["disclaimer"], str)
        assert len(result["disclaimer"]) > 20

    def test_medical_emergency_scenario(self, base_profile):
        scenario = {
            "scenario_type": "medical_emergency",
            "lump_sum_loss_inr": 40000.0,
            "new_monthly_expense_inr": 5000.0,
            "duration_months": 12
        }
        res = simulate_economic_scenario(base_profile, scenario)
        assert res["net_financial_impact_inr"] < 0
        assert res["scenario_trajectory"][0]["savings_balance"] <= base_profile["current_savings"]

    def test_business_startup_scenario(self, base_profile):
        scenario = {
            "scenario_type": "business_startup",
            "lump_sum_loss_inr": 30000.0,
            "income_change_pct": 25.0,
            "duration_months": 24
        }
        res = simulate_economic_scenario(base_profile, scenario)
        assert len(res["scenario_trajectory"]) == 24
        assert res["scenario_trajectory"][-1]["income"] > base_profile["monthly_take_home_income"]

    def test_lump_sum_loss_depletes_savings_at_month_1(self, base_profile):
        scenario = {
            "lump_sum_loss_inr": base_profile["current_savings"] + 10000.0,
            "duration_months": 6
        }
        res = simulate_economic_scenario(base_profile, scenario)
        assert res["scenario_trajectory"][0]["savings_balance"] >= 0.0

