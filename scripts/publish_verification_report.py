#!/usr/bin/env python3
"""Convert pytest JUnit XML into a small, honest dashboard report."""
import json
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def main():
    junit_path = Path(sys.argv[1] if len(sys.argv) > 1 else "reports/pytest.xml")
    output_path = Path(sys.argv[2] if len(sys.argv) > 2 else "reports/publish/verification.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit_sha": os.environ.get("GITHUB_SHA", ""),
        "workflow_url": os.environ.get("GITHUB_SERVER_URL", "https://github.com")
        + "/" + os.environ.get("GITHUB_REPOSITORY", "")
        + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", ""),
        "status": "NOT RUN",
        "counts": {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0},
        "files": [],
        "failures": [],
        "error": None,
    }
    if not junit_path.is_file():
        report["error"] = "Pytest did not produce a JUnit XML report."
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return 0

    try:
        root = ET.parse(junit_path).getroot()
    except (ET.ParseError, OSError) as exc:
        report["error"] = "Could not parse pytest JUnit XML: " + str(exc)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return 0

    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    per_file = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0, "errors": 0, "skipped": 0})
    for suite in suites:
        for case in suite.findall("testcase"):
            name = case.get("name", "unknown")
            classname = case.get("classname", "")
            module = classname.rsplit(".", 1)[0] if classname else ""
            if module.startswith("tests."):
                file_path = module.replace(".", "/") + ".py"
            elif module.startswith("test_"):
                file_path = "tests/" + module + ".py"
            else:
                file_path = suite.get("name", module or "unknown")
                if not file_path.endswith(".py"):
                    file_path += ".py"
            status = "passed"
            failure = case.find("failure")
            error = case.find("error")
            skipped = case.find("skipped")
            if failure is not None:
                status = "failed"
                report["failures"].append({
                    "nodeid": file_path + "::" + name,
                    "message": (failure.get("message") or failure.text or "Assertion failed")[:4000],
                })
            elif error is not None:
                status = "errors"
                report["failures"].append({
                    "nodeid": file_path + "::" + name,
                    "message": (error.get("message") or error.text or "Test error")[:4000],
                })
            elif skipped is not None:
                status = "skipped"
            per_file[file_path]["total"] += 1
            per_file[file_path][status] += 1
            report["counts"]["total"] += 1
            report["counts"][status] += 1

    report["files"] = [{"path": path, "counts": counts} for path, counts in sorted(per_file.items())]
    report["status"] = "PASS" if report["counts"]["failed"] == 0 and report["counts"]["errors"] == 0 and report["counts"]["total"] > 0 else "FAIL"
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
