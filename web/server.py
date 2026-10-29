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


@app.route("/defense")
@app.route("/rubrics")
@app.route("/architecture")
@app.route("/report")
def page_defense():
    """Render Report & Architecture Portal (AUCML Case Study)."""
    return render_template("defense.html")


@app.route("/models")
@app.route("/code")
@app.route("/playground")
def page_models():
    """Render Real-Time Interactive Model Code & Playground."""
    return render_template("models.html")



# ── REST API ENDPOINTS ──

@app.route("/api/system/smoke-test", methods=["GET", "POST"])
def api_system_smoke_test():
    """Run five live engine smoke checks; this endpoint does not execute pytest."""
    import time
    start_t = time.perf_counter()
    checks = []
    diagnostics = {}

    def run_check(name, operation, validate):
        """Run one engine check and record its real result without hiding failures."""
        try:
            value = operation()
            validate(value)
            checks.append({"name": name, "status": "PASS", "detail": "Output contract validated."})
            diagnostics[name] = value
        except Exception as exc:
            checks.append({"name": name, "status": "FAIL", "detail": f"{type(exc).__name__}: {exc}"})
            diagnostics[name] = {"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}

    def check_economy():
        result = calculate_financial_indicators(DEFAULT_PROFILE)
        assert isinstance(result, dict) and 0 <= float(result["resilience_score"]) <= 100
        return {"status": "OPERATIONAL", "resilience_score": result.get("resilience_score"),
                "net_surplus_inr": result.get("monthly_surplus_deficit"),
                "runway_months": result.get("emergency_fund_months"),
                "category": result.get("resilience_category")}

    def check_cyber():
        threat = assess_cyber_risk("CBI Officer: Digital arrest warrant issued. Transfer funds to avoid detention.")
        safe = assess_cyber_risk("Your SBI salary credit of INR 35,000 is processed. Ref #42981.")
        assert isinstance(threat, dict) and "risk_score" in threat
        assert isinstance(safe, dict) and "risk_score" in safe
        assert float(threat["risk_score"]) > float(safe["risk_score"])
        return {"status": "OPERATIONAL", "threat_score": threat.get("risk_score"),
                "threat_level": threat.get("risk_level"), "safe_score": safe.get("risk_score")}

    def check_opportunities():
        df = load_public_dataset("opportunities")
        opportunities = df.to_dict(orient="records") if not df.empty else []
        ranked = rank_opportunities(DEFAULT_PROFILE, opportunities)
        assert isinstance(ranked, list)
        if opportunities:
            assert ranked, "Opportunity catalogue exists but ranking returned no results."
            assert "match_score_pct" in ranked[0]
        return {"status": "OPERATIONAL", "matched_count": len(ranked),
                "top_recommendation": ranked[0].get("title") if ranked else None}

    def check_simulator():
        result = simulate_economic_scenario(DEFAULT_PROFILE, {
            "scenario_type": "job_loss", "duration_months": 12,
            "income_change_pct": -100.0, "lump_sum_loss_inr": 0.0, "expense_change_pct": 0.0
        })
        trajectory = result.get("scenario_trajectory")
        assert isinstance(trajectory, list) and len(trajectory) == 12
        return {"status": "OPERATIONAL", "depletion_month": result.get("months_to_depletion"),
                "trajectory_steps": len(trajectory)}

    def check_recovery():
        steps = get_recovery_steps("unauthorized_upi")
        assert isinstance(steps, list) and len(steps) > 0
        return {"status": "OPERATIONAL", "playbook_steps": len(steps)}

    run_check("economy_engine", check_economy, lambda value: value.update({"_validated": True}))
    run_check("cyber_engine", check_cyber, lambda value: value.update({"_validated": True}))
    run_check("opportunity_engine", check_opportunities, lambda value: value.update({"_validated": True}))
    run_check("simulator_engine", check_simulator, lambda value: value.update({"_validated": True}))
    run_check("recovery_engine", check_recovery, lambda value: value.update({"_validated": True}))

    # Internal validation marker is not part of the public diagnostics contract.
    for value in diagnostics.values():
        if isinstance(value, dict):
            value.pop("_validated", None)

    passed = sum(check["status"] == "PASS" for check in checks)
    failed = len(checks) - passed
    return jsonify({
        "status": "success" if failed == 0 else "failure",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "latency_ms": round((time.perf_counter() - start_t) * 1000, 2),
        "engine_checks_run": len(checks),
        "engine_checks_passed": passed,
        "engine_checks_failed": failed,
        "pytest_suite_status": "NOT RUN by this smoke-test endpoint; see the CI-generated verification report.",
        "checks": checks,
        "diagnostics": diagnostics
    }), (200 if failed == 0 else 500)


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
