"""
AAYAM - Modern Web Application Server (Flask)
Exposes full REST API endpoints linked to AAYAM processing engines
and serves the website frontend.
"""
import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory

# Add project root to sys.path so engines and loaders import cleanly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.engines.economy import calculate_financial_indicators
from src.engines.cyber import assess_cyber_risk
from src.engines.recommendations import rank_opportunities
from src.engines.simulator import simulate_economic_scenario
from src.engines.recovery import get_recovery_steps
from src.data.loaders import load_public_dataset

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "web" / "templates"),
    static_folder=str(PROJECT_ROOT / "web" / "static")
)

# Default demo session profile
DEFAULT_PROFILE = {
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


@app.route("/")
def index():
    """Render main modern web application landing page."""
    return render_template("index.html")


@app.route("/command")
def page_command():
    """Render Module 1: Systemic Command Centre."""
    return render_template("command.html")


@app.route("/twin")
def page_twin():
    """Render Module 2: Economic Digital Twin."""
    return render_template("twin.html")


@app.route("/opportunities")
def page_opportunities():
    """Render Module 3: Opportunity Pathways & Mudra."""
    return render_template("opportunities.html")


@app.route("/cyberdrishti")
def page_cyberdrishti():
    """Render Module 4: CyberDrishti Threat Screener & Matrix."""
    return render_template("cyberdrishti.html")


@app.route("/arthsim")
def page_arthsim():
    """Render Module 5: ArthSim Scenario Simulator."""
    return render_template("arthsim.html")


@app.route("/intelligence")
def page_intelligence():
    """Render Module 6: India Macro & Cybercrime Intelligence."""
    return render_template("intelligence.html")


@app.route("/trustgraph")
def page_trustgraph():
    """Render Module 7: Trust Graph Threat Architecture."""
    return render_template("trustgraph.html")


@app.route("/recovery")
def page_recovery():
    """Render Module 8: Recovery Centre & 1930 Playbooks."""
    return render_template("recovery.html")


@app.route("/guide")
def page_guide():
    """Render System Guide & Persona Handbook."""
    return render_template("guide.html")


@app.route("/warning")
@app.route("/disclaimer")
def page_disclaimer():
    """Render Ethical Guardrails & Warning Page (What AAYAM Is Not For)."""
    return render_template("disclaimer.html")


# ── REST API ENDPOINTS ──

@app.route("/api/economy/calculate", methods=["POST"])
def api_calculate_economy():
    """Calculate financial indicators and composite resilience score."""
    data = request.get_json() or DEFAULT_PROFILE
    indicators = calculate_financial_indicators(data)
    return jsonify({"status": "success", "indicators": indicators, "profile": data})


@app.route("/api/cyber/assess", methods=["POST"])
def api_assess_cyber():
    """Screen message text for cyber threat signals."""
    data = request.get_json() or {}
    text = data.get("text", "")
    risk_result = assess_cyber_risk(text)
    return jsonify({"status": "success", "result": risk_result})


@app.route("/api/recommendations/rank", methods=["POST"])
def api_rank_opportunities():
    """Rank opportunities matching profile."""
    data = request.get_json() or {}
    profile = data.get("profile", DEFAULT_PROFILE)
    df_opps = load_public_dataset("opportunities")
    opps = df_opps.to_dict(orient="records") if not df_opps.empty else []
    ranked = rank_opportunities(profile, opps)
    return jsonify({"status": "success", "ranked": ranked, "total": len(ranked)})


@app.route("/api/simulator/simulate", methods=["POST"])
def api_simulate():
    """Simulate financial trajectory under shock scenario."""
    data = request.get_json() or {}
    profile = data.get("profile", DEFAULT_PROFILE)
    scenario_name = data.get("scenario", "job_loss")
    horizon = int(data.get("horizon_months", 12))

    scenario_cfg = {
        "scenario_type": scenario_name,
        "duration_months": horizon,
        "income_change_pct": -100.0 if scenario_name == "job_loss" else 0.0,
        "lump_sum_loss_inr": 50000.0 if scenario_name == "cyber_fraud_loss" else (75000.0 if scenario_name == "medical_emergency" else 0.0),
        "expense_change_pct": 20.0 if scenario_name == "inflation_spike" else 0.0
    }
    sim_result = simulate_economic_scenario(profile, scenario_cfg)
    
    # Map standardized trajectory points for UI chart
    trajectory = []
    for pt in sim_result.get("scenario_trajectory", []):
        trajectory.append({
            "month": pt["month"],
            "savings_end": pt["savings_balance"],
            "inflows": pt.get("inflows", 0),
            "outflows": pt.get("outflows", 0)
        })
        
    depleted = sim_result.get("months_to_depletion") is not None
    depletion_month = sim_result.get("months_to_depletion")
    initial_savings = profile.get("current_savings", 50000.0)
    
    actionable_guidance = (
        f"Critical: Liquid buffer depletes at Month {depletion_month}. Immediate discretionary cost reduction required."
        if depleted else
        f"Resilient: Household maintains emergency solvency across the full {horizon}-month stress horizon."
    )
    
    sim_result["trajectory"] = trajectory
    sim_result["depleted"] = depleted
    sim_result["depletion_month"] = depletion_month
    sim_result["initial_savings"] = initial_savings
    sim_result["actionable_guidance"] = actionable_guidance

    return jsonify({"status": "success", "result": sim_result})


@app.route("/api/recovery/playbook", methods=["POST"])
def api_recovery_playbook():
    """Fetch incident response playbook by category."""
    data = request.get_json() or {}
    category = data.get("incident_category", "suspicious_payment")
    steps = get_recovery_steps(category)
    return jsonify({"status": "success", "steps": steps, "category": category})


@app.route("/api/data/<dataset_name>", methods=["GET"])
def api_get_dataset(dataset_name):
    """Return JSON records for any registered dataset."""
    df = load_public_dataset(dataset_name)
    if df.empty:
        return jsonify({"status": "error", "message": f"Dataset '{dataset_name}' not found"}), 404
    return jsonify({"status": "success", "data": df.to_dict(orient="records"), "count": len(df)})


@app.route("/api/source-register", methods=["GET"])
def api_source_register():
    """Return all verified source provenance entries."""
    df = load_public_dataset("source_register")
    return jsonify({"status": "success", "sources": df.to_dict(orient="records") if not df.empty else []})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting AAYAM Modern Web Server on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
