"""
AAYAM - Opportunity Pathways Recommendation Engine
Implements canonical contract:
    rank_opportunities(profile: dict, opportunities: list[dict]) -> list[dict]
Ranks employment, upskilling, and micro-entrepreneurship pathways based on transparent,
explainable criteria: skill alignment, financial affordability, educational prerequisites,
and potential economic uplift.
"""
from src.utils.logging_config import logger


# Educational hierarchy for alignment scoring
EDUCATION_LEVELS = {
    "none": 0,
    "primary": 1,
    "secondary (10th)": 2,
    "higher secondary (12th)": 3,
    "iti / vocational": 3,
    "diploma": 4,
    "graduate / b.com / b.sc / b.a": 5,
    "b.tech / be / stem graduate": 6,
    "post graduate": 7
}


def _normalize_edu_score(edu_str: str) -> int:
    """Normalize education string to rank integer."""
    if not edu_str:
        return 2
    low = edu_str.lower()
    for key, val in EDUCATION_LEVELS.items():
        if key in low:
            return val
    return 3


def rank_opportunities(profile: dict, opportunities: list[dict]) -> list[dict]:
    """
    Rank career and enterprise pathways using explainable multi-factor scoring.
    
    Args:
        profile: User profile dictionary containing:
            - education: str
            - skills: list[str] or comma-separated str
            - current_savings: float
            - monthly_take_home_income: float
            - location: str
        opportunities: List of opportunity dictionaries from the catalogue.
        
    Returns:
        list[dict]: Ranked opportunities sorted by fit score with transparent breakdown.
    """
    if not isinstance(opportunities, list) or not opportunities:
        logger.warning("Empty opportunities list passed to ranking engine.")
        return []
        
    # User Profile parsing
    user_skills_raw = profile.get("skills", [])
    if isinstance(user_skills_raw, str):
        user_skills = {s.strip().lower() for s in user_skills_raw.split(",") if s.strip()}
    elif isinstance(user_skills_raw, list):
        user_skills = {str(s).strip().lower() for s in user_skills_raw if s}
    else:
        user_skills = set()
        
    user_savings = max(0.0, float(profile.get("current_savings") or 0.0))
    user_income = max(0.0, float(profile.get("monthly_take_home_income") or 0.0))
    user_edu_score = _normalize_edu_score(str(profile.get("education", "")))
    
    ranked_results = []
    
    for opp in opportunities:
        req_skills_raw = opp.get("required_skills", [])
        if isinstance(req_skills_raw, str):
            req_skills = [s.strip() for s in req_skills_raw.split(",") if s.strip()]
        else:
            req_skills = [str(s).strip() for s in req_skills_raw if s]
            
        req_skills_lower = {s.lower() for s in req_skills}
        
        # 1. Skill Match Component (Max 40 points)
        if req_skills_lower:
            matched_skills = [s for s in req_skills if s.lower() in user_skills]
            missing_skills = [s for s in req_skills if s.lower() not in user_skills]
            skill_ratio = len(matched_skills) / len(req_skills_lower)
            pts_skills = skill_ratio * 40.0
        else:
            matched_skills = []
            missing_skills = []
            pts_skills = 30.0  # Entry-level with no strict skill gate
            
        # 2. Financial Affordability (Max 25 points)
        capital_req = float(opp.get("capital_required_inr", 0.0))
        training_cost = float(opp.get("training_cost_inr", 0.0))
        total_upfront = capital_req + training_cost
        
        if total_upfront == 0.0:
            pts_affordability = 25.0
            affordability_status = "Fully Affordable (Zero Upfront Capital)"
        elif user_savings >= total_upfront:
            pts_affordability = 25.0
            affordability_status = "Fully Affordable from Savings"
        elif user_savings >= (total_upfront * 0.25):
            # Eligible with Mudra / PMEGP margin money (user puts 10-25%)
            pts_affordability = 18.0
            affordability_status = "Affordable via Government Micro-Loan (Mudra / PMEGP)"
        else:
            pts_affordability = 8.0
            affordability_status = "Capital Gap (Requires Grant or Savings Accrual)"
            
        # 3. Education Prerequisite Alignment (Max 15 points)
        req_edu_str = opp.get("required_education", "")
        req_edu_score = _normalize_edu_score(req_edu_str)
        if user_edu_score >= req_edu_score:
            pts_education = 15.0
            edu_status = "Meets or exceeds educational requirements"
        else:
            pts_education = max(5.0, 15.0 - (req_edu_score - user_edu_score) * 5.0)
            edu_status = f"Requires prerequisite credential: {req_edu_str}"
            
        # 4. Income Uplift Potential (Max 20 points)
        min_income = float(opp.get("estimated_monthly_income_min_inr", 0.0))
        max_income = float(opp.get("estimated_monthly_income_max_inr", min_income))
        midpoint_income = (min_income + max_income) / 2.0
        
        if user_income == 0.0:
            pts_uplift = 20.0
            uplift_inr = midpoint_income
            uplift_desc = f"Provides new primary livelihood (₹{min_income:,.0f} - ₹{max_income:,.0f}/mo)"
        elif midpoint_income > user_income:
            uplift_inr = midpoint_income - user_income
            uplift_pct = (uplift_inr / user_income) * 100.0
            pts_uplift = min(20.0, 10.0 + (uplift_pct / 50.0) * 10.0)
            uplift_desc = f"Projected income uplift of +₹{uplift_inr:,.0f}/month (+{uplift_pct:.0f}%)"
        else:
            uplift_inr = 0.0
            pts_uplift = 8.0
            uplift_desc = "Comparable or secondary diversification income"
            
        total_score = round(pts_skills + pts_affordability + pts_education + pts_uplift, 1)
        
        # Categorize Fit
        if total_score >= 75.0:
            fit_tier = "High Alignment"
        elif total_score >= 50.0:
            fit_tier = "Moderate Alignment"
        else:
            fit_tier = "Development Opportunity"
            
        # Transparent reasons
        reasons = [
            f"Skill match: {len(matched_skills)} of {len(req_skills)} required competencies verified ({pts_skills:.1f}/40 pts).",
            f"Financial entry: {affordability_status} ({pts_affordability:.1f}/25 pts).",
            f"Education fit: {edu_status} ({pts_education:.1f}/15 pts).",
            f"Economic outcome: {uplift_desc} ({pts_uplift:.1f}/20 pts)."
        ]
        
        ranked_results.append({
            **opp,
            "match_score_pct": total_score,
            "fit_tier": fit_tier,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "affordability_status": affordability_status,
            "total_upfront_cost_inr": total_upfront,
            "projected_monthly_uplift_inr": round(uplift_inr, 2),
            "score_breakdown": {
                "skills_points": round(pts_skills, 1),
                "affordability_points": round(pts_affordability, 1),
                "education_points": round(pts_education, 1),
                "uplift_points": round(pts_uplift, 1)
            },
            "transparent_reasons": reasons
        })
        
    # Sort descending by match score
    ranked_results.sort(key=lambda x: x["match_score_pct"], reverse=True)
    return ranked_results
