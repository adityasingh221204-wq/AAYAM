"""
AAYAM - Shared Pytest Fixtures
Standardized test fixtures across economy, cyber, recommendations, simulator, and platform modules.
"""
import pytest
import sys
import os
from pathlib import Path

# Ensure project root is in python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def demo_profile():
    """Default baseline session profile matching app.py."""
    return {
        "monthly_take_home_income": 35000.0,
        "other_monthly_income": 5000.0,
        "essential_monthly_expenses": 20000.0,
        "discretionary_expenses": 6000.0,
        "current_savings": 50000.0,
        "outstanding_debt": 75000.0,
        "monthly_debt_repayments": 4500.0,
        "emergency_expenses_obligations": 0.0,
        "education": "Higher Secondary (12th)",
        "occupation": "Salaried / Support Role",
        "region": "Maharashtra",
        "skills": ["Customer Service", "Computer Literacy", "Digital Payments"],
        "economic_goals": "Build emergency buffer and transition to higher-wage career pathway"
    }


@pytest.fixture
def healthy_profile():
    """High-surplus, zero-debt resilient profile."""
    return {
        "monthly_take_home_income": 80000.0,
        "other_monthly_income": 10000.0,
        "essential_monthly_expenses": 25000.0,
        "discretionary_expenses": 8000.0,
        "current_savings": 500000.0,
        "outstanding_debt": 0.0,
        "monthly_debt_repayments": 0.0,
        "emergency_expenses_obligations": 0.0,
        "education": "Graduate / B.Com / B.Sc / B.A",
        "skills": ["Financial Accounting", "Data Entry", "Advanced Excel"]
    }


@pytest.fixture
def stressed_profile():
    """Deficit, high-debt vulnerable profile."""
    return {
        "monthly_take_home_income": 25000.0,
        "other_monthly_income": 0.0,
        "essential_monthly_expenses": 22000.0,
        "discretionary_expenses": 5000.0,
        "current_savings": 5000.0,
        "outstanding_debt": 120000.0,
        "monthly_debt_repayments": 6000.0,
        "emergency_expenses_obligations": 2000.0,
        "education": "Secondary (10th)",
        "skills": ["Manual Labor"]
    }


@pytest.fixture
def zero_income_profile():
    """Profile with zero income but non-zero living expenses."""
    return {
        "monthly_take_home_income": 0.0,
        "other_monthly_income": 0.0,
        "essential_monthly_expenses": 15000.0,
        "discretionary_expenses": 0.0,
        "current_savings": 30000.0,
        "outstanding_debt": 0.0,
        "monthly_debt_repayments": 0.0,
        "emergency_expenses_obligations": 0.0,
        "education": "Secondary (10th)",
        "skills": []
    }


@pytest.fixture
def base_scenario():
    """Standard 6-month job loss stress-test scenario."""
    return {
        "scenario_type": "job_loss",
        "duration_months": 6,
        "income_change_pct": -100.0,
        "lump_sum_loss_inr": 0.0,
        "expense_change_pct": 0.0
    }


@pytest.fixture
def sample_message_phishing():
    """Deceptive smishing text targeting electricity disconnection and fake APK."""
    return (
        "Dear consumer your electricity disconnected tonight from bijli vibhag. "
        "Install app from link http://bit.ly/update.apk to avoid power cut."
    )


@pytest.fixture
def sample_message_digital_arrest():
    """High-severity extortion lure impersonating CBI / customs."""
    return (
        "This is CBI Officer Sharma calling via Skype video call. A narcotics parcel addressed in your name "
        "was intercepted by Customs. You are placed under digital arrest until you transfer funds to court verification account."
    )


@pytest.fixture
def sample_message_clean():
    """Standard legitimate bank transactional SMS."""
    return "Your A/C ending in 4521 is credited with INR 35,000 on 28-Feb-2025 by salary transfer from employer. Ref: CMS3489201."


@pytest.fixture
def sample_opportunities():
    """Curated list of test opportunities for ranking assertions."""
    return [
        {
            "opportunity_id": "TEST-EMP-001",
            "title": "Data Analytics Specialist",
            "track": "Employment",
            "sector": "Technology",
            "required_skills": "Python, SQL, Data Visualization",
            "required_education": "graduate / b.com / b.sc / b.a",
            "estimated_monthly_income_min_inr": 35000,
            "estimated_monthly_income_max_inr": 65000,
            "capital_required_inr": 0,
            "training_cost_inr": 4000,
            "scheme_linkage": "PMKVY 4.0 | IT-ITeS SSC"
        },
        {
            "opportunity_id": "TEST-ENT-002",
            "title": "CSC Digital Seva Kendra",
            "track": "Enterprise",
            "sector": "Digital Services",
            "required_skills": "Computer Literacy, Digital Payments, Customer Service",
            "required_education": "higher secondary (12th)",
            "estimated_monthly_income_min_inr": 20000,
            "estimated_monthly_income_max_inr": 45000,
            "capital_required_inr": 30000,
            "training_cost_inr": 0,
            "scheme_linkage": "PM Mudra Yojana | Shishu"
        }
    ]


@pytest.fixture
def sample_network_nodes_edges():
    """Sample nodes and edges for testing graph generation."""
    nodes = [
        ("SMS_SMISHING", {"label": "SMS / Smishing", "type": "Channel", "color": "#6366F1"}),
        ("MALICIOUS_APK", {"label": "Malicious Android APK", "type": "Threat", "color": "#F43F5E"}),
        ("HELPLINE_1930", {"label": "1930 Cyber Fraud Helpline", "type": "Defense", "color": "#10B981"})
    ]
    edges = [
        ("SMS_SMISHING", "MALICIOUS_APK", {"relationship": "delivers payload"}),
        ("HELPLINE_1930", "MALICIOUS_APK", {"relationship": "mitigates"})
    ]
    return nodes, edges
