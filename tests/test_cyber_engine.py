"""
Tests for AAYAM CyberDrishti Engine (src/engines/cyber.py)
Covers: threat detection, risk scoring, guidance, edge cases.
"""
import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engines.cyber import assess_cyber_risk


# ─── Known Threat Messages ────────────────────────────────────────────────────

DIGITAL_ARREST_MSG = (
    "Sir this is CBI officer Sharma. A parcel with narcotics was seized in your name. "
    "You must appear for a Skype interrogation now or face digital arrest."
)

REVERSE_UPI_MSG = (
    "Congratulations! Your KBC prize is ready. Enter UPI PIN to receive payment of Rs 5,00,000. "
    "Scan the QR code and enter pin dalte hi paise milenge."
)

APK_MSG = (
    "Your electricity bill is overdue. To avoid disconnection tonight, "
    "install our bijli vibhag apk from this link to pay immediately."
)

CREDENTIAL_MSG = (
    "Your SBI account is on hold. Please share OTP received on your phone "
    "along with your card number and CVV to restore access."
)

RAT_MSG = (
    "Please install AnyDesk and share the 9 digit code with our bank customer support "
    "to resolve your account issue."
)

LEGITIMATE_MSG = (
    "Your transaction of Rs 150 at BigBazaar on account XXXX1234 was successful. "
    "Available balance: Rs 12,450. If unauthorized, call 1800-XXX-XXXX."
)

EMPTY_MSG = ""


# ─── Return Structure Tests ───────────────────────────────────────────────────

class TestReturnStructure:
    def test_returns_dict(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert isinstance(result, dict)

    def test_required_keys_present(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        required_keys = [
            "risk_score", "risk_level", "is_suspicious",
            "triggered_patterns", "reason_codes",
            "attack_chain_stage", "safety_guidance", "disclaimer"
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_empty_string_does_not_crash(self):
        result = assess_cyber_risk(EMPTY_MSG)
        assert isinstance(result, dict)
        assert result["risk_score"] == 0.0

    def test_none_does_not_crash(self):
        result = assess_cyber_risk(None)
        assert isinstance(result, dict)
        assert result["is_suspicious"] is False

    def test_non_string_does_not_crash(self):
        result = assess_cyber_risk(12345)
        assert isinstance(result, dict)


# ─── Threat Detection Tests ───────────────────────────────────────────────────

class TestThreatDetection:
    def test_digital_arrest_detected(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert result["is_suspicious"] is True
        assert "DIGITAL_ARREST_IMPERSONATION" in result["reason_codes"]

    def test_reverse_upi_detected(self):
        result = assess_cyber_risk(REVERSE_UPI_MSG)
        assert result["is_suspicious"] is True
        assert "REVERSE_UPI_QR_SCAM" in result["reason_codes"]

    def test_malicious_apk_detected(self):
        result = assess_cyber_risk(APK_MSG)
        assert result["is_suspicious"] is True
        assert "MALICIOUS_APK_DELIVERY" in result["reason_codes"]

    def test_credential_harvesting_detected(self):
        result = assess_cyber_risk(CREDENTIAL_MSG)
        assert result["is_suspicious"] is True
        assert "CREDENTIAL_OTP_HARVESTING" in result["reason_codes"]

    def test_remote_access_tool_detected(self):
        result = assess_cyber_risk(RAT_MSG)
        assert result["is_suspicious"] is True
        assert "REMOTE_ACCESS_TOOL_PROMPT" in result["reason_codes"]

    def test_legitimate_transaction_not_flagged(self):
        result = assess_cyber_risk(LEGITIMATE_MSG)
        assert result["risk_level"] in ("Low Risk", "Minimal Risk")
        assert result["is_suspicious"] is False


# ─── Risk Score Tests ─────────────────────────────────────────────────────────

class TestRiskScoring:
    def test_risk_score_bounded_0_to_100(self):
        for msg in [DIGITAL_ARREST_MSG, REVERSE_UPI_MSG, APK_MSG, CREDENTIAL_MSG, LEGITIMATE_MSG, EMPTY_MSG]:
            result = assess_cyber_risk(msg)
            assert 0.0 <= result["risk_score"] <= 100.0, f"Score out of bounds for: {msg[:40]}"

    def test_high_severity_threat_score_high(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert result["risk_score"] >= 35.0

    def test_critical_combined_threat_score_very_high(self):
        combined = DIGITAL_ARREST_MSG + " " + RAT_MSG
        result = assess_cyber_risk(combined)
        assert result["risk_score"] >= 60.0
        assert result["risk_level"] == "Critical Threat"

    def test_legitimate_msg_low_score(self):
        result = assess_cyber_risk(LEGITIMATE_MSG)
        assert result["risk_score"] < 15.0


# ─── Risk Level Categorization Tests ─────────────────────────────────────────

class TestRiskLevels:
    def test_digital_arrest_critical_or_high(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert result["risk_level"] in ("Critical Threat", "High Suspicion")

    def test_legitimate_low_risk(self):
        result = assess_cyber_risk(LEGITIMATE_MSG)
        assert result["risk_level"] in ("Low Risk", "Minimal Risk")

    def test_empty_msg_minimal_risk(self):
        result = assess_cyber_risk(EMPTY_MSG)
        assert result["risk_level"] in ("Low Risk", "Minimal Risk")


# ─── Safety Guidance Tests ────────────────────────────────────────────────────

class TestSafetyGuidance:
    def test_guidance_is_list(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert isinstance(result["safety_guidance"], list)
        assert len(result["safety_guidance"]) > 0

    def test_digital_arrest_guidance_mentions_1930(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        combined_guidance = " ".join(result["safety_guidance"]).lower()
        assert "1930" in combined_guidance or "cybercrime" in combined_guidance

    def test_upi_guidance_explains_pin_debit(self):
        result = assess_cyber_risk(REVERSE_UPI_MSG)
        combined_guidance = " ".join(result["safety_guidance"]).lower()
        assert "pin" in combined_guidance or "debit" in combined_guidance or "deducting" in combined_guidance

    def test_rat_guidance_mentions_anydesk(self):
        result = assess_cyber_risk(RAT_MSG)
        combined_guidance = " ".join(result["safety_guidance"]).lower()
        assert "anydesk" in combined_guidance or "9-digit" in combined_guidance or "9 digit" in combined_guidance

    def test_disclaimer_present(self):
        result = assess_cyber_risk(LEGITIMATE_MSG)
        assert isinstance(result["disclaimer"], str)
        assert len(result["disclaimer"]) > 20


# ─── Triggered Patterns Structure Tests ──────────────────────────────────────

class TestTriggeredPatterns:
    def test_triggered_patterns_is_list(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert isinstance(result["triggered_patterns"], list)

    def test_each_pattern_has_required_fields(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        for pattern in result["triggered_patterns"]:
            assert "code" in pattern
            assert "category" in pattern
            assert "severity_points" in pattern
            assert "explanation" in pattern

    def test_matched_terms_populated(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        for pattern in result["triggered_patterns"]:
            assert "matched_terms" in pattern
            assert isinstance(pattern["matched_terms"], list)

    def test_no_patterns_for_clean_message(self):
        result = assess_cyber_risk(LEGITIMATE_MSG)
        assert len(result["triggered_patterns"]) == 0


# ─── Attack Chain Stage Tests ─────────────────────────────────────────────────

class TestAttackChainStage:
    def test_chain_stage_is_string(self):
        result = assess_cyber_risk(DIGITAL_ARREST_MSG)
        assert isinstance(result["attack_chain_stage"], str)

    def test_clean_message_no_chain(self):
        result = assess_cyber_risk(LEGITIMATE_MSG)
        combined = result["attack_chain_stage"].lower()
        assert "none" in combined or "no malicious" in combined
