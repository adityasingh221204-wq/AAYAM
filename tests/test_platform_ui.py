"""
Tests for AAYAM Platform, UI/UX & Chart Library (Member 4)
Covers: conftest shared fixtures, threat network visualization,
chart components, theme tokens, and formatting helpers.
"""
import pytest
import plotly.graph_objects as go
import pandas as pd

from src.ui.charts import (
    plot_threat_network, plot_resilience_gauge,
    plot_resilience_components, plot_opportunity_score_breakdown,
    plot_rbi_system_trend
)
from src.utils.formatting import format_inr, format_pct
from src.engines.economy import calculate_financial_indicators
from src.engines.cyber import assess_cyber_risk
from src.engines.recommendations import rank_opportunities
from src.engines.simulator import simulate_economic_scenario


# ════════════════════════════════════════════════════════════════════════════
# 1. CONFTEST FIXTURE INTEGRATION TESTS
# ════════════════════════════════════════════════════════════════════════════

class TestConftestFixtures:
    """Validate that shared fixtures from conftest.py integrate across all engines."""
    
    def test_demo_profile_structure(self, demo_profile):
        assert isinstance(demo_profile, dict)
        assert demo_profile["monthly_take_home_income"] == 35000.0
        assert demo_profile["current_savings"] == 50000.0
        res = calculate_financial_indicators(demo_profile)
        assert "resilience_score" in res
        assert 0 <= res["resilience_score"] <= 100

    def test_healthy_profile_high_resilience(self, healthy_profile):
        res = calculate_financial_indicators(healthy_profile)
        assert res["resilience_score"] >= 70
        assert res["monthly_surplus_deficit"] > 0

    def test_stressed_profile_low_resilience(self, stressed_profile):
        res = calculate_financial_indicators(stressed_profile)
        assert res["resilience_score"] <= 50
        assert len(res["risk_factors"]) > 0

    def test_base_scenario_runs_cleanly(self, demo_profile, base_scenario):
        res = simulate_economic_scenario(demo_profile, base_scenario)
        assert len(res["scenario_trajectory"]) == 6
        assert "months_to_depletion" in res

    def test_sample_message_phishing_triggers_detection(self, sample_message_phishing):
        res = assess_cyber_risk(sample_message_phishing)
        assert res["is_suspicious"] is True
        assert res["risk_score"] >= 35

    def test_sample_message_clean_passes(self, sample_message_clean):
        res = assess_cyber_risk(sample_message_clean)
        assert res["is_suspicious"] is False
        assert res["risk_score"] < 25

    def test_sample_opportunities_ranking(self, demo_profile, sample_opportunities):
        ranked = rank_opportunities(demo_profile, sample_opportunities)
        assert len(ranked) == 2
        assert "match_score_pct" in ranked[0]
        assert ranked[0]["match_score_pct"] >= ranked[1]["match_score_pct"]


# ════════════════════════════════════════════════════════════════════════════
# 2. THREAT NETWORK CHART TESTS (Member 4 Feature)
# ════════════════════════════════════════════════════════════════════════════

class TestThreatNetworkChart:
    """Validate plot_threat_network generation and filtering."""
    
    def test_plot_threat_network_empty_returns_figure(self):
        fig = plot_threat_network([], [])
        assert isinstance(fig, go.Figure)

    def test_plot_threat_network_none_returns_figure(self):
        fig = plot_threat_network(None, None)
        assert isinstance(fig, go.Figure)

    def test_plot_threat_network_renders_traces(self, sample_network_nodes_edges):
        nodes, edges = sample_network_nodes_edges
        fig = plot_threat_network(nodes, edges)
        assert isinstance(fig, go.Figure)
        # Should have 2 traces: edge lines and node markers
        assert len(fig.data) == 2
        assert fig.data[0].mode == "lines"
        assert "markers" in fig.data[1].mode

    def test_plot_threat_network_filter_types(self, sample_network_nodes_edges):
        nodes, edges = sample_network_nodes_edges
        # Filter to only Channel nodes
        fig = plot_threat_network(nodes, edges, filter_types=["Channel"])
        assert isinstance(fig, go.Figure)
        node_trace = fig.data[1]
        assert len(node_trace.x) == 1  # only 1 Channel node in fixture


# ════════════════════════════════════════════════════════════════════════════
# 3. CHART BUILDERS VERIFICATION
# ════════════════════════════════════════════════════════════════════════════

class TestPlatformCharts:
    """Validate chart builder outputs and error tolerance."""
    
    def test_plot_resilience_gauge(self):
        fig = plot_resilience_gauge(75.5)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == "indicator"

    def test_plot_resilience_components(self):
        component_scores = {
            "stability_points": 8.0,
            "debt_health_points": 20.0,
            "cashflow_surplus_points": 25.0,
            "emergency_runway_points": 30.0
        }
        fig = plot_resilience_components(component_scores)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == "bar"

    def test_plot_opportunity_score_breakdown(self, sample_opportunities):
        opp = sample_opportunities[0]
        opp["score_breakdown"] = {
            "skills_points": 30.0,
            "affordability_points": 20.0,
            "education_points": 15.0,
            "uplift_points": 18.0
        }
        fig = plot_opportunity_score_breakdown(opp)
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == "bar"

    def test_plot_rbi_system_trend(self):
        df_mock = pd.DataFrame([
            {"period": "Feb 2024", "system_name": "UPI", "volume_crore": 1210.0},
            {"period": "Feb 2025", "system_name": "UPI", "volume_crore": 1610.0}
        ])
        fig = plot_rbi_system_trend(df_mock, "UPI")
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].mode == "lines+markers"


# ════════════════════════════════════════════════════════════════════════════
# 4. FORMATTING UTILITIES VERIFICATION
# ════════════════════════════════════════════════════════════════════════════

class TestFormattingUtils:
    """Validate INR and percentage formatters."""
    
    def test_format_inr_positive(self):
        formatted = format_inr(35000)
        assert "35,000" in formatted or "35000" in formatted

    def test_format_inr_negative(self):
        formatted = format_inr(-5000)
        assert "-" in formatted

    def test_format_pct(self):
        formatted = format_pct(23.456)
        assert "%" in formatted
