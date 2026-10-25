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
from src.ui.charts import plot_opportunity_score_breakdown
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

# 2. Sidebar Filters (Member 3 Enhanced Specification: Track, Sector, Location Type)
all_tracks = sorted(list({o.get("track", "") for o in raw_opps if o.get("track")}))
all_sectors = sorted(list({o.get("sector", "") for o in raw_opps if o.get("sector")}))
all_locations = sorted(list({o.get("location_type", "") for o in raw_opps if o.get("location_type")}))

with st.sidebar:
    st.markdown("### 🔍 Multi-Factor Pathway Filters")
    track_filter = st.multiselect(
        "Opportunity Track",
        options=all_tracks,
        default=all_tracks
    )
    sector_filter = st.multiselect(
        "Target Sector",
        options=all_sectors,
        default=all_sectors
    )
    location_filter = st.multiselect(
        "Location / Work Mode",
        options=all_locations,
        default=all_locations
    )
    max_capital = st.slider(
        "Max Upfront Capital Required (₹)",
        min_value=0,
        max_value=100000,
        value=100000,
        step=5000
    )

# Filter opportunities
filtered_opps = [
    o for o in raw_opps
    if (o.get("track") in track_filter) and
       (o.get("sector") in sector_filter) and
       (o.get("location_type") in location_filter) and
       (float(o.get("capital_required_inr", 0.0) or 0.0) <= max_capital)
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
        subtext=f"Of {len(raw_opps)} total verified paths",
        delta_text="100% Transparent Scoring",
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
        delta_text=f"Edu: {profile.get('education', '12th')[:14]}",
        badge_color="indigo"
    )

st.markdown("---")
st.markdown("### 📋 Ranked Opportunities & Multi-Factor Alignment")

if not ranked_opps:
    st.warning("No opportunities match your filter selections. Try adjusting the filters in the sidebar.")

for idx, opp in enumerate(ranked_opps):
    score = opp["match_score_pct"]
    tier = opp["fit_tier"]
    
    tier_class = "aayam-badge-tier-high" if tier == "High Alignment" else ("aayam-badge-tier-mod" if tier == "Moderate Alignment" else "aayam-badge-tier-dev")
    
    with st.expander(f"#{idx+1} {opp['title']} — {opp['track']} &bull; Match: {score:.1f}% ({tier})", expanded=(idx < 2)):
        c1, c2 = st.columns([3, 2])
        
        with c1:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <h4 style="margin: 0; color: #F8FAFC;">{opp['title']}</h4>
                    <span class="aayam-badge-tier {tier_class}">{tier}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"**Sector:** `{opp.get('sector', '')}` &bull; **Track:** `{opp.get('track', '')}` &bull; **Location:** `{opp.get('location_type', '')}`")
            st.markdown(f"_{opp.get('description', '')}_")
            st.markdown(f"**Required Education:** `{opp.get('required_education', '')}`")
            
            # Skills breakdown with colored badges
            m_skills = opp.get("matched_skills", [])
            missing_skills = opp.get("missing_skills", [])
            
            st.markdown("**Skill Alignment:**")
            skills_html = []
            for s in m_skills:
                skills_html.append(f"<span style='background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-right: 4px;'>✓ {s}</span>")
            for s in missing_skills:
                skills_html.append(f"<span style='background: rgba(245, 158, 11, 0.2); color: #FBBF24; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; margin-right: 4px;'>+ {s}</span>")
            
            st.markdown(" ".join(skills_html), unsafe_allow_html=True)
            st.markdown(f"🏛️ **Government Scheme Linkage:** `{opp.get('scheme_linkage', 'Skill India')}`")
            
            # Transparent 4-item reason list (Member 3 Requirement)
            st.markdown("**Transparent Scoring Justification:**")
            for r_idx, r in enumerate(opp.get("transparent_reasons", []), start=1):
                st.markdown(f"<span style='font-size: 0.85rem; color: #CBD5E1;'>{r_idx}. {r}</span>", unsafe_allow_html=True)

        with c2:
            st.markdown(
                f"""
                <div class="aayam-card-secondary">
                    <div style="font-size: 0.82rem; color: #94A3B8;">ESTIMATED MONTHLY EARNINGS</div>
                    <div style="font-size: 1.35rem; font-weight: 700; color: #10B981; margin-bottom: 6px;">
                        {format_inr(opp.get('estimated_monthly_income_min_inr', 0))} – {format_inr(opp.get('estimated_monthly_income_max_inr', 0))}
                    </div>
                    <div style="font-size: 0.8rem; color: #F8FAFC; line-height: 1.6;">
                        <strong>Upfront Capital:</strong> {format_inr(opp.get('capital_required_inr', 0))}<br>
                        <strong>Training Duration:</strong> {opp.get('training_duration_weeks', 0)} Weeks<br>
                        <strong>Training Fee:</strong> {format_inr(opp.get('training_cost_inr', 0))}<br>
                        <strong>Projected Monthly Uplift:</strong> +{format_inr(opp.get('projected_monthly_uplift_inr', 0))}/mo
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # "Can I afford this?" Tooltip / Info Card (Member 3 Requirement)
            upfront_val = float(opp.get("total_upfront_cost_inr", 0.0))
            if upfront_val == 0.0:
                afford_text = "💡 **Can I afford this?** Zero upfront cost. 100% accessible immediately through government skill development or direct hiring."
                alert_type_choice = "success"
            elif profile.get("current_savings", 0) >= upfront_val:
                afford_text = f"💡 **Can I afford this?** Fully covered by your liquid savings ({format_inr(profile.get('current_savings', 0))} available vs. {format_inr(upfront_val)} required)."
                alert_type_choice = "success"
            elif profile.get("current_savings", 0) >= (upfront_val * 0.15):
                afford_text = f"💡 **Can I afford this?** Eligible for **PM Mudra Yojana (Shishu/Kishor)**. Your savings cover the mandatory 15% margin money; remaining {format_inr(upfront_val * 0.85)} can be financed via collateral-free institutional credit."
                alert_type_choice = "info"
            else:
                afford_text = f"💡 **Can I afford this?** Capital gap: Requires {format_inr(upfront_val)}. Recommend applying for state livelihood grants, NRLM SHG revolving funds, or building emergency savings first."
                alert_type_choice = "warning"
                
            render_alert_box("Financial Affordability Check", afford_text, alert_type=alert_type_choice)
            
            # Horizontal 4-bar sub-score breakdown chart (Member 3 Requirement)
            st.plotly_chart(
                plot_opportunity_score_breakdown(opp),
                use_container_width=True
            )

render_data_provenance(
    dataset_name="Opportunity Catalogue & NSQF Job Roles",
    publisher="NSDC, Ministry of Skill Development & MoMSME",
    reference_period="2024-25 Framework",
    source_url="https://www.skillindiadigital.gov.in/"
)

render_footer()
