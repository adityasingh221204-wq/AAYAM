"""
AAYAM - Page 3: Opportunity Pathways
Explainable career, upskilling, and micro-entrepreneurship recommendation engine.
"""
import streamlit as st
import json
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.engines.recommendations import rank_opportunities
from src.data.loaders import load_public_dataset
from src.utils.formatting import format_inr

st.set_page_config(page_title="Opportunity Pathways — AAYAM", page_icon="🚀", layout="wide")
apply_theme()

render_header(
    title="Opportunity Pathways",
    subtitle="Explainable, skill-aligned career progression and micro-enterprise opportunities.",
    badge_text="Module 3",
    badge_type="emerald"
)

render_alert_box(
    title="Transparent Recommendation Principle",
    message="Recommendations are evaluated against transparent criteria: skill overlap, capital affordability, education alignment, and potential monthly income uplift. AAYAM does not guarantee job placement, loan sanction, or commercial outcomes.",
    alert_type="info"
)

# 1. Load User Profile & Opportunity Catalogue
profile = st.session_state.get("user_profile", {})
df_opps = load_public_dataset("opportunities")

if df_opps.empty:
    st.error("Opportunity catalogue dataset could not be loaded.")
    st.stop()
    
# Convert DataFrame to list of dicts for the canonical engine
raw_opps = df_opps.to_dict(orient="records")

# 2. Sidebar Filters
with st.sidebar:
    st.markdown("### 🔍 Pathway Filters")
    track_filter = st.multiselect(
        "Opportunity Track",
        options=["Employment", "Micro-Enterprise", "Self-Employment"],
        default=["Employment", "Micro-Enterprise", "Self-Employment"]
    )
    max_capital = st.slider(
        "Maximum Starting Capital Required (₹)",
        min_value=0,
        max_value=100000,
        value=100000,
        step=5000
    )

# Filter opportunities
filtered_opps = [
    o for o in raw_opps
    if o.get("track") in track_filter and float(o.get("capital_required_inr", 0.0)) <= max_capital
]

# 3. Rank Opportunities via Canonical Engine
ranked_opps = rank_opportunities(profile, filtered_opps)

# Summary KPIs
st.markdown("### 🎯 Matched Pathways Overview")
s_col1, s_col2, s_col3 = st.columns(3)

with s_col1:
    render_kpi_card(
        title="Pathways Evaluated",
        value=str(len(ranked_opps)),
        subtext="From verified NSQF / MSME frameworks",
        delta_text="100% Transparent",
        badge_color="indigo"
    )
with s_col2:
    high_fits = sum(1 for o in ranked_opps if o["match_score_pct"] >= 70.0)
    render_kpi_card(
        title="High Alignment Fits",
        value=str(high_fits),
        subtext="Score ≥ 70%",
        delta_text="Immediate Viability",
        badge_color="emerald"
    )
with s_col3:
    user_skills_len = len(profile.get("skills", []))
    render_kpi_card(
        title="Profile Skills Applied",
        value=f"{user_skills_len} Skills",
        subtext=", ".join(profile.get("skills", [])[:3]),
        delta_text="In Twin Profile",
        badge_color="indigo"
    )

st.markdown("---")
st.markdown("### 📋 Ranked Opportunities")

for idx, opp in enumerate(ranked_opps):
    score = opp["match_score_pct"]
    tier = opp["fit_tier"]
    badge_type = "emerald" if score >= 75 else ("indigo" if score >= 50 else "amber")
    
    with st.expander(f"#{idx+1} {opp['title']} — {opp['track']} &bull; Match: {score}% ({tier})", expanded=(idx < 2)):
        c1, c2 = st.columns([3, 2])
        
        with c1:
            st.markdown(f"**Description:** {opp.get('description', '')}")
            st.markdown(f"**Sector:** `{opp.get('sector', '')}` &bull; **Location Type:** `{opp.get('location_type', '')}`")
            st.markdown(f"**Educational Requirement:** `{opp.get('required_education', '')}`")
            
            # Skills breakdown
            m_skills = opp.get("matched_skills", [])
            missing_skills = opp.get("missing_skills", [])
            
            st.markdown("**Skill Alignment:**")
            if m_skills:
                st.markdown("✅ *Verified Matching Skills:* " + ", ".join([f"`{s}`" for s in m_skills]))
            if missing_skills:
                st.markdown("🎯 *Skills to Acquire / Upskill:* " + ", ".join([f"`{s}`" for s in missing_skills]))
                
            st.markdown(f"**Linked Government Scheme:** 🏛️ **{opp.get('scheme_linkage', 'Skill India')}**")
            
        with c2:
            st.markdown(
                f"""
                <div class="aayam-card-secondary">
                    <div style="font-size: 0.82rem; color: #94A3B8;">ESTIMATED MONTHLY EARNINGS</div>
                    <div style="font-size: 1.35rem; font-weight: 700; color: #10B981; margin-bottom: 6px;">
                        {format_inr(opp.get('estimated_monthly_income_min_inr', 0))} – {format_inr(opp.get('estimated_monthly_income_max_inr', 0))}
                    </div>
                    <div style="font-size: 0.8rem; color: #F8FAFC;">
                        <strong>Upfront Capital:</strong> {format_inr(opp.get('capital_required_inr', 0))}<br>
                        <strong>Training Duration:</strong> {opp.get('training_duration_weeks', 0)} Weeks<br>
                        <strong>Training Fee:</strong> {format_inr(opp.get('training_cost_inr', 0))}<br>
                        <strong>Affordability:</strong> <span style="color: #FBBF24;">{opp.get('affordability_status', '')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("**Explainability Score Breakdown:**")
        b = opp.get("score_breakdown", {})
        st.markdown(
            f"- Skills: `{b.get('skills_points', 0)}/40 pts` &bull; "
            f"Affordability: `{b.get('affordability_points', 0)}/25 pts` &bull; "
            f"Education: `{b.get('education_points', 0)}/15 pts` &bull; "
            f"Income Uplift: `{b.get('uplift_points', 0)}/20 pts`"
        )
        for r in opp.get("transparent_reasons", []):
            st.caption(f"&bull; {r}")

render_data_provenance(
    dataset_name="Opportunity & Skill Matrix",
    publisher="NSDC, PMKVY 4.0 & Ministry of MSME",
    reference_period="2024-2025 Framework",
    source_url="https://www.skillindiadigital.gov.in/"
)

render_footer()
