"""
Tests for AAYAM Recommendations Engine (src/engines/recommendations.py)
Tests for AAYAM Recovery Engine (src/engines/recovery.py)
Tests for AAYAM Data Loaders (src/data/loaders.py)
"""
import pytest
import sys
import os
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engines.recommendations import rank_opportunities
from src.engines.recovery import get_recovery_steps
from src.data.loaders import load_public_dataset


# ════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS ENGINE TESTS
# ════════════════════════════════════════════════════════════════════════════

SAMPLE_OPPORTUNITIES = [
    {
        "opportunity_id": "OPP001",
        "title": "Full Stack Web Developer",
        "category": "Employment",
        "required_skills": "Python, JavaScript, HTML/CSS",
        "required_education": "graduate / b.com / b.sc / b.a",
        "estimated_monthly_income_min_inr": 40000,
        "estimated_monthly_income_max_inr": 80000,
        "capital_required_inr": 0,
        "training_cost_inr": 5000,
        "description": "Develop web applications."
    },
    {
        "opportunity_id": "OPP002",
        "title": "Mobile Food Cart Operator",
        "category": "Micro-Enterprise",
        "required_skills": "Basic Cooking",
        "required_education": "primary",
        "estimated_monthly_income_min_inr": 15000,
        "estimated_monthly_income_max_inr": 30000,
        "capital_required_inr": 20000,
        "training_cost_inr": 0,
        "description": "Street food micro-enterprise."
    },
    {
        "opportunity_id": "OPP003",
        "title": "Digital Payments Agent (BC Agent)",
        "category": "Banking Correspondent",
        "required_skills": "Customer Service, Digital Payments",
        "required_education": "secondary (10th)",
        "estimated_monthly_income_min_inr": 10000,
        "estimated_monthly_income_max_inr": 20000,
        "capital_required_inr": 5000,
        "training_cost_inr": 0,
        "description": "Assist customers with digital banking."
    }
]

SKILLED_PROFILE = {
    "education": "Graduate / B.Com / B.Sc / B.A",
    "skills": ["Python", "JavaScript", "HTML/CSS", "Customer Service"],
    "current_savings": 30000.0,
    "monthly_take_home_income": 25000.0,
}

BASIC_PROFILE = {
    "education": "Secondary (10th)",
    "skills": ["Customer Service", "Digital Payments"],
    "current_savings": 8000.0,
    "monthly_take_home_income": 12000.0,
}


class TestRankOpportunitiesStructure:
    def test_returns_list(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        assert isinstance(result, list)

    def test_empty_opportunities_returns_empty_list(self):
        result = rank_opportunities(SKILLED_PROFILE, [])
        assert result == []

    def test_none_opportunities_returns_empty_list(self):
        result = rank_opportunities(SKILLED_PROFILE, None)
        assert result == []

    def test_each_result_has_match_score(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        for r in result:
            assert "match_score_pct" in r
            assert "fit_tier" in r
            assert "matched_skills" in r
            assert "missing_skills" in r
            assert "score_breakdown" in r
            assert "transparent_reasons" in r


class TestRankOpportunitiesScoring:
    def test_results_sorted_descending(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        scores = [r["match_score_pct"] for r in result]
        assert scores == sorted(scores, reverse=True)

    def test_high_skill_match_gets_higher_score(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        # Find OPP001 score (skilled profile matches Python, JS, HTML)
        opp001 = next(r for r in result if r["opportunity_id"] == "OPP001")
        opp003 = next(r for r in result if r["opportunity_id"] == "OPP003")
        assert opp001["match_score_pct"] >= opp003["match_score_pct"]

    def test_score_in_range_0_to_100(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        for r in result:
            assert 0.0 <= r["match_score_pct"] <= 100.0

    def test_basic_profile_matches_bc_agent_well(self):
        result = rank_opportunities(BASIC_PROFILE, SAMPLE_OPPORTUNITIES)
        opp003 = next(r for r in result if r["opportunity_id"] == "OPP003")
        # BC agent requires exactly the basic profile skills
        assert opp003["match_score_pct"] >= 50.0

    def test_fit_tiers_valid(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        valid_tiers = {"High Alignment", "Moderate Alignment", "Development Opportunity"}
        for r in result:
            assert r["fit_tier"] in valid_tiers

    def test_transparent_reasons_is_list_of_strings(self):
        result = rank_opportunities(SKILLED_PROFILE, SAMPLE_OPPORTUNITIES)
        for r in result:
            assert isinstance(r["transparent_reasons"], list)
            for reason in r["transparent_reasons"]:
                assert isinstance(reason, str)


# ════════════════════════════════════════════════════════════════════════════
# RECOVERY ENGINE TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestRecoverySteps:
    def test_returns_list(self):
        steps = get_recovery_steps("suspicious_payment")
        assert isinstance(steps, list)
        assert len(steps) > 0

    def test_step_structure(self):
        steps = get_recovery_steps("suspicious_payment")
        for step in steps:
            assert "step_number" in step
            assert "priority" in step
            assert "action_title" in step
            assert "instructions" in step

    def test_all_incident_types_resolve(self):
        incident_types = [
            "suspicious_payment", "suspected_account_compromise",
            "suspected_phishing", "malicious_application_installation",
            "identity_misuse"
        ]
        for inc_type in incident_types:
            steps = get_recovery_steps(inc_type)
            assert len(steps) > 0, f"No steps returned for: {inc_type}"

    def test_alias_payment_fraud_resolves(self):
        steps = get_recovery_steps("payment_fraud")
        assert len(steps) > 0

    def test_alias_phishing_resolves(self):
        steps = get_recovery_steps("phishing")
        assert len(steps) > 0

    def test_alias_malicious_apk_resolves(self):
        steps = get_recovery_steps("malicious_apk")
        assert len(steps) > 0

    def test_alias_sim_swap_resolves(self):
        steps = get_recovery_steps("sim_swap")
        assert len(steps) > 0

    def test_unknown_type_returns_default(self):
        # Should fall back to default (suspicious_payment) steps
        steps = get_recovery_steps("totally_unknown_incident_xyz")
        assert len(steps) > 0

    def test_steps_ordered_by_step_number(self):
        steps = get_recovery_steps("suspicious_payment")
        nums = [s["step_number"] for s in steps]
        assert nums == sorted(nums)

    def test_payment_steps_mention_1930(self):
        steps = get_recovery_steps("suspicious_payment")
        combined = " ".join(str(s) for s in steps).lower()
        assert "1930" in combined

    def test_phishing_steps_mention_cert_in(self):
        steps = get_recovery_steps("suspected_phishing")
        combined = " ".join(str(s) for s in steps).lower()
        assert "cert-in" in combined or "cert_in" in combined or "cert" in combined


# ════════════════════════════════════════════════════════════════════════════
# DATA LOADER TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestDataLoaders:
    def test_rbi_payment_systems_loads(self):
        df = load_public_dataset("rbi_payment_systems")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_rbi_frauds_loads(self):
        df = load_public_dataset("domestic_payment_frauds")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_plfs_loads(self):
        df = load_public_dataset("plfs_indicators")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_hces_loads(self):
        df = load_public_dataset("hces_indicators")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_asuse_loads(self):
        df = load_public_dataset("asuse_indicators")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_cert_in_loads(self):
        df = load_public_dataset("cert_in_advisories")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_opportunities_loads(self):
        df = load_public_dataset("opportunities")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_source_register_loads(self):
        df = load_public_dataset("source_register")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_alias_rbi_resolves(self):
        df = load_public_dataset("rbi")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_alias_frauds_resolves(self):
        df = load_public_dataset("frauds")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_alias_plfs_resolves(self):
        df = load_public_dataset("plfs")
        assert isinstance(df, pd.DataFrame)
        assert not df.empty

    def test_unknown_dataset_returns_empty_df(self):
        df = load_public_dataset("nonexistent_dataset_xyz")
        assert isinstance(df, pd.DataFrame)
        assert df.empty

    def test_rbi_has_expected_columns(self):
        df = load_public_dataset("rbi_payment_systems")
        expected_cols = {"system_name", "period", "value_inr_crore"}
        assert expected_cols.issubset(set(df.columns))

    def test_cert_in_has_expected_columns(self):
        df = load_public_dataset("cert_in_advisories")
        expected_cols = {"title", "severity", "attack_vector"}
        assert expected_cols.issubset(set(df.columns))

    def test_opportunities_has_expected_columns(self):
        df = load_public_dataset("opportunities")
        expected_cols = {"opportunity_id", "title", "track", "sector"}
        assert expected_cols.issubset(set(df.columns))
