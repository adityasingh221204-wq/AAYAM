"""Regression tests for truthful verification reporting and live model playgrounds."""
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_SCRIPT = ROOT / "scripts" / "publish_verification_report.py"


def test_junit_report_counts_results_and_captures_failures(tmp_path):
    junit = tmp_path / "pytest.xml"
    output = tmp_path / "verification.json"
    junit.write_text(
        """<testsuites><testsuite name="pytest" tests="4" failures="1" errors="1" skipped="1">
        <testcase classname="tests.test_cyber_engine.TestRisk" name="test_pass"/>
        <testcase classname="tests.test_cyber_engine.TestRisk" name="test_fail">
          <failure message="expected 1 got 2">assert 1 == 2</failure>
        </testcase>
        <testcase classname="tests.test_economy_engine.TestRisk" name="test_error">
          <error message="unexpected error">ValueError</error>
        </testcase>
        <testcase classname="tests.test_economy_engine.TestRisk" name="test_skip">
          <skipped message="optional dependency"/>
        </testcase>
        </testsuite></testsuites>""",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env.update({
        "GITHUB_SHA": "abc123",
        "GITHUB_REPOSITORY": "owner/repo",
        "GITHUB_RUN_ID": "42",
        "GITHUB_SERVER_URL": "https://github.com",
    })
    subprocess.run(
        [sys.executable, str(REPORT_SCRIPT), str(junit), str(output)],
        check=True,
        cwd=ROOT,
        env=env,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["status"] == "FAIL"
    assert report["commit_sha"] == "abc123"
    assert report["counts"] == {
        "total": 4, "passed": 1, "failed": 1, "errors": 1, "skipped": 1
    }
    assert len(report["failures"]) == 2
    assert {item["path"] for item in report["files"]} == {
        "tests/test_cyber_engine.py", "tests/test_economy_engine.py"
    }


def test_missing_junit_report_is_not_run_not_passed(tmp_path):
    output = tmp_path / "verification.json"
    subprocess.run(
        [sys.executable, str(REPORT_SCRIPT), str(tmp_path / "missing.xml"), str(output)],
        check=True,
        cwd=ROOT,
    )
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["status"] == "NOT RUN"
    assert report["counts"]["total"] == 0
    assert report["error"]


def test_verification_dashboard_does_not_hardcode_pass_counts():
    html = (ROOT / "web" / "templates" / "defense.html").read_text(encoding="utf-8")
    assert 'id="verificationSuiteStatus"' in html
    assert "verification-results/verification.json" in html
    assert "35 / 35 Passed" not in html
    assert "130/130 Pytests Passed" not in html
    assert "NOT RUN / NO PUBLISHED REPORT" in html


def test_eri_formula_documents_actual_engine_components():
    html = (ROOT / "web" / "templates" / "defense.html").read_text(encoding="utf-8")
    assert "ERI = S<sub>runway</sub> + S<sub>surplus</sub> + S<sub>debt</sub> + S<sub>stability</sub>" in html
    assert "maximum 30 for positive surplus" in html
    assert "S<sub>stability</sub> = 10" in html
    assert "25 − ((DTI − 20) ÷ 20) × 15" in html


def test_model_playground_uses_engine_apis_and_no_fixed_pathway_wage():
    html = (ROOT / "web" / "templates" / "models.html").read_text(encoding="utf-8")
    assert "fetch('/api/cyber/assess'" in html
    assert "fetch('/api/recommendations/rank'" in html
    assert "let cyberPlaygroundRequestId = 0" in html
    assert "let opportunityPlaygroundRequestId = 0" in html
    assert "Projected Wage Delta: +₹12,000 to ₹18,000" not in html
    assert "Empty input is not treated as a safe result" in html


def test_smoke_test_endpoint_distinguishes_engine_checks_from_pytest():
    from web.server import app

    response = app.test_client().get("/api/system/smoke-test")
    payload = response.get_json()
    assert payload["status"] in {"success", "failure"}
    assert payload["engine_checks_run"] == 5
    assert payload["engine_checks_passed"] + payload["engine_checks_failed"] == 5
    assert payload["pytest_suite_status"].startswith("NOT RUN")
    assert "130/130 Passed" not in json.dumps(payload)
