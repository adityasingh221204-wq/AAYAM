"""
AAYAM - Page 0: Interactive System Guide & User Manual
Comprehensive visual walkthrough explaining how to use AAYAM,
its architectural modules, decision engines, and dataset linkages.
"""
import streamlit as st
from src.ui.theme import apply_theme
from src.ui.components import render_header, render_alert_box, render_kpi_card, render_footer
from src.utils.config import APP_NAME, APP_TAGLINE, SDG_ALIGNMENT
from src.data.loaders import load_public_dataset

st.set_page_config(page_title="System Guide — AAYAM", page_icon="📖", layout="wide")
apply_theme()

render_header(
    title="AAYAM User Manual & System Guide",
    subtitle="Learn how to navigate, model personal economics, screen cyber threats, and interpret macroeconomic data.",
    badge_text="User Guide",
    badge_type="indigo",
    show_guide_btn=False
)

render_alert_box(
    title="How to Get the Most Out of AAYAM",
    message="AAYAM is organized into 8 interconnected modules. Data entered in one module (such as your Economic Digital Twin) seamlessly informs other modules (like Opportunity Pathways and ArthSim Simulator) across your active session.",
    alert_type="info"
)

# 1. Quick Start Stepper
st.markdown("### 🚀 3-Step Guided Onboarding")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        """
        <div class="aayam-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">1️⃣</div>
            <h4 style="color: #34D399; margin-top: 0;">Configure Your Twin</h4>
            <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.45;">
                Start in <strong>Economic Digital Twin</strong> (Module 2). Input your monthly income, living expenses, existing debt, and emergency reserves.
            </p>
            <span class="badge badge-emerald">Step 1: Baseline</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Go to Digital Twin →", key="guide_nav_dt"):
        st.switch_page("pages/2_Economic_Digital_Twin.py")

with c2:
    st.markdown(
        """
        <div class="aayam-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">2️⃣</div>
            <h4 style="color: #818CF8; margin-top: 0;">Match & Stress-Test</h4>
            <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.45;">
                Explore AI-matched career pathways in <strong>Opportunity Pathways</strong> (Module 3) or simulate income shocks in <strong>ArthSim</strong> (Module 5).
            </p>
            <span class="badge badge-indigo">Step 2: Mobility</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Explore Opportunities →", key="guide_nav_opp"):
        st.switch_page("pages/3_Opportunity_Pathways.py")

with c3:
    st.markdown(
        """
        <div class="aayam-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">3️⃣</div>
            <h4 style="color: #FB7185; margin-top: 0;">Screen Cyber Threats</h4>
            <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.45;">
                Check suspicious SMS, APKs, or calls in <strong>CyberDrishti</strong> (Module 4) and review recovery playbooks in <strong>Recovery Centre</strong> (Module 8).
            </p>
            <span class="badge badge-rose">Step 3: Defense</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Open CyberDrishti →", key="guide_nav_cd"):
        st.switch_page("pages/4_CyberDrishti.py")

st.markdown("---")

# 2. Detailed Module Manual (Interactive Tabs)
st.markdown("### 📚 Comprehensive Module Directory")

tab_mod, tab_workflow, tab_data, tab_faq = st.tabs([
    "🧭 Module Breakdown",
    "🔄 User Journeys & Scenarios",
    "📊 Dataset Transparency & Sources",
    "❓ Frequently Asked Questions"
])

with tab_mod:
    st.markdown(
        """
        #### Detailed Walkthrough of All 8 Modules
        
        ##### 🧭 1. Command Centre
        * **Purpose:** Executive dashboard offering unified cross-domain situational awareness.
        * **What to Look For:** Personal resilience status, live UPI payment volume counters, national employment health, and latest CERT-In threat alerts.
        * **Recommended For:** Daily check-ins and executive briefings.
        
        ##### 🧬 2. Economic Digital Twin
        * **Purpose:** Builds an interactive in-memory model of your personal financial situation.
        * **Outputs:** 
          - *Composite Resilience Index (0–100)*: Multi-dimensional score weighing savings rate, runway, DTI, and discretionary flexibility.
          - *Emergency Runway*: How many months your liquid savings can sustain essential living expenses + debt.
          - *Net Cash Flow*: Monthly surplus or deficit.
        * **Interactive Controls:** Adjust take-home pay, EMIs, expenses, education, and skills in real-time via the sidebar form.
        
        ##### 🚀 3. Opportunity Pathways
        * **Purpose:** AI/ML-driven decision-support matching your profile to viable wage-employment and micro-enterprise options.
        * **Scoring Factors:**
          1. *Skill Overlap (40% weight)*: Match between your listed skills and required role competencies.
          2. *Education Fit (25% weight)*: Qualification alignment with NSQF levels.
          3. *Affordability & Capital (20% weight)*: Required capital vs. your liquid savings + Mudra loan margin money.
          4. *Income Growth Potential (15% weight)*: Projected income uplift compared to current earnings.
        * **Government Linkages:** PMKVY 4.0, Skill India Digital, and Pradhan Mantri Mudra Yojana (Shishu, Kishore, Tarun).
        
        ##### 🔍 4. CyberDrishti
        * **Purpose:** Explainable heuristic threat detector screening digital communications for fraud signals.
        * **Detection Vectors:** Digital arrest scams, fake TRAI disconnection robocalls, deceptive UPI collect requests, reverse QR codes, malicious APK droppers, Telegram VIP task traps, and fastag KYC smishing.
        * **How to Use:** Paste any SMS or WhatsApp message into the text area and click *Screen Message*. Review the risk level, triggered red flags, and actionable guidance.
        
        ##### ⚡ 5. ArthSim: Scenario Simulator
        * **Purpose:** Deterministic financial simulator modeling the multi-month trajectory of personal finances under stress.
        * **Simulated Shocks:** 
          - Unanticipated job loss (0% or reduced income)
          - Cyber-financial fraud lump-sum loss
          - Medical emergency / healthcare expenditure
          - Inflationary cost-of-living increase
        * **Outputs:** Interactive savings depletion curve and estimated months until total liquidity exhaustion.
        
        ##### 📊 6. India Intelligence
        * **Purpose:** Macroeconomic and sector-level intelligence dashboard powered by 7+ verified institutional datasets.
        * **Tabs:**
          - *RBI Payments:* UPI, NEFT, IMPS, RTGS monthly volumes and values.
          - *Fraud Registry:* Domestic payment fraud counts and basis-point loss ratios (CPFIR).
          - *Labour Force:* PLFS 2023-24 LFPR, WPR, Unemployment Rate by state and sector.
          - *Consumption:* HCES 2023-24 MPCE fractile classes and food/non-food shares.
          - *Enterprises:* ASUSE 2023-24 GVA and worker compensation in unincorporated sector.
        
        ##### 🕸️ 7. Trust Graph
        * **Purpose:** Graph-theoretic knowledge network mapping the cyber-threat ecosystem.
        * **Nodes & Edges:** Visualizes connections between Threat Vectors, Attack Channels, Vulnerability Factors, and Official Defense Mechanisms.
        
        ##### 🆘 8. Recovery Centre
        * **Purpose:** Time-critical incident response playbook for victims of digital financial crime.
        * **Key Playbooks:**
          - *Golden 2-Hour Window:* Urgent steps to freeze fraudulent funds via 1930 / cybercrime.gov.in.
          - *RBI 72-Hour Zero-Liability Protocol:* How to report unauthorized transactions to your bank to preserve statutory protection.
          - *Direct Helpline Directory:* One-click emergency contacts for major Indian banks and law enforcement agencies.
        """
    )

with tab_workflow:
    st.markdown(
        """
        #### Common Real-World Scenarios
        
        ##### 👤 Persona 1: Gig Worker or Blue-Collar Professional (Seeking Economic Uplift)
        1. Open **Economic Digital Twin**, set monthly take-home to ₹22,000, essential expenses to ₹16,000, savings to ₹15,000.
        2. View your **Resilience Score** (~42/100, "Vulnerable").
        3. Switch to **Opportunity Pathways** to find *Quick Commerce Dark Store Inventory Executive* or *Drone Fleet Operator*.
        4. Check Mudra loan eligibility (Shishu category: up to ₹50,000) for micro-enterprise pathways.
        5. In **India Intelligence**, check the *Labour Force* tab to see regional wage averages in your state.
        
        ##### 🛡️ Persona 2: Citizen Receiving an Urgent SMS or Call
        1. An SMS arrives: *"Dear customer, your SBI rewards worth Rs 8,500 expire today. Redeem now at bit.ly/sbi-points-in"*.
        2. Open **CyberDrishti**, paste the text into the screening tool, and click **Screen Message**.
        3. CyberDrishti flags: **Critical Severity (Score: 85/100)** due to shortened link, urgent deadline, and fake bank domain.
        4. The citizen does NOT click the link and avoids losing credentials.
        
        ##### 🚨 Persona 3: Citizen Whose Account Had an Unauthorized Debit
        1. Open **Recovery Centre** immediately.
        2. Follow Step 1: Call **1930** (Citizen Financial Cyber Fraud Reporting System) within the **Golden 2-Hour Window** so the cyber cell can issue a lien/freeze order to the beneficiary bank.
        3. Follow Step 2: Call the bank's 24x7 fraud helpline (numbers provided on the page) to block the debit card, netbanking, and UPI handle.
        4. Follow Step 3: Lodge a written dispute with the bank under RBI's 72-hour Zero Liability Framework.
        """
    )

with tab_data:
    st.markdown("#### Official Data Provenance Register")
    df_reg = load_public_dataset("source_register")
    if not df_reg.empty:
        st.dataframe(
            df_reg[["dataset_name", "publisher", "reference_period", "official_source_url", "access_status"]].rename(
                columns={
                    "dataset_name": "Dataset",
                    "publisher": "Institutional Publisher",
                    "reference_period": "Reference Period",
                    "official_source_url": "Source URL",
                    "access_status": "Status"
                }
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Registry loading...")

with tab_faq:
    st.markdown(
        """
        #### Frequently Asked Questions (FAQ)
        
        **Q1: Does AAYAM store my bank account details or salary data?**  
        *No.* AAYAM operates entirely in-memory within your active browser session. None of your entered numbers, profile details, or messages are ever uploaded to a remote server, external database, or third-party AI API.
        
        **Q2: Is AAYAM affiliated with RBI, CERT-In, or MoSPI?**  
        *No.* AAYAM is an independent student academic decision-support prototype. It uses public government datasets published under open data policies for educational, research, and non-commercial decision support.
        
        **Q3: Can CyberDrishti scan my entire phone?**  
        *No.* AAYAM does not require or request device permissions. You paste suspicious text or app names directly into the screening tool for heuristic rule-based evaluation.
        
        **Q4: How are Opportunity Pathway match scores calculated?**  
        Matches are calculated using a weighted multi-attribute utility model combining Skill Overlap (40%), Educational Qualifications (25%), Capital Affordability with Mudra loans (20%), and Expected Income Uplift (15%). Every recommendation is accompanied by an explainable factor breakdown.
        """
    )

st.markdown("---")
render_footer()
