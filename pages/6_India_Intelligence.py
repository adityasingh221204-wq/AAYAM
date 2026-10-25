"""
AAYAM - Page 6: India Intelligence
Macroeconomic and digital payments analytics dashboard using official public datasets:
RBI Payment System Indicators, PLFS 2023-24, HCES 2023-24, and ASUSE 2023-24.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.ui.charts import (
    plot_rbi_payment_growth, plot_rbi_fraud_trends,
    plot_plfs_wpr_by_state, plot_hces_fractiles,
    plot_rbi_system_trend, DARK_LAYOUT
)
from src.data.loaders import load_public_dataset

st.set_page_config(page_title="India Intelligence — AAYAM", page_icon="📊", layout="wide")
apply_theme()

render_header(
    title="AAYAM India Intelligence",
    subtitle="Macroeconomic, Labour, Household Consumption, and Payment Fraud Statistics from Official Indian Portals.",
    badge_text="Module 6",
    badge_type="indigo"
)

render_alert_box(
    title="Data Governance & Methodology Note",
    message="All data presented in this section is sourced directly from official government releases: Reserve Bank of India (RBI), Ministry of Statistics and Programme Implementation (MoSPI NSSO). Aggregates are presented for regional/sectoral context and should not be used to infer individual-level financial behavior.",
    alert_type="info"
)

# 5 Dedicated Tabs as per Member 3 Specification
tab_rbi, tab_frauds, tab_plfs, tab_hces, tab_asuse = st.tabs([
    "💳 RBI Payments",
    "🚨 Fraud Trends",
    "💼 Labour Force",
    "🛒 Household Expenditure",
    "🏭 Enterprises"
])

# 1. TAB: RBI Payments
with tab_rbi:
    df_payments = load_public_dataset("rbi_payment_systems")
    
    st.markdown("### Digital Payment Volumes & Channel Adoption (RBI)")
    
    k1, k2, k3 = st.columns(3)
    with k1:
        render_kpi_card(
            title="Total Digital Vol (Feb 2025)",
            value="19,095 Cr",
            subtext="All domestic retail channels",
            delta_text="+26.7% YoY Growth",
            badge_color="emerald"
        )
    with k2:
        render_kpi_card(
            title="UPI Share of Retail Vol",
            value="84.2%",
            subtext="16,106 Cr transactions",
            delta_text="Dominant Retail Rail",
            badge_color="emerald"
        )
    with k3:
        render_kpi_card(
            title="NEFT Monthly Vol",
            value="55.2 Cr",
            subtext="High-value batch settlement",
            delta_text="+14.8% YoY",
            badge_color="indigo"
        )
        
    st.markdown("---")
    
    if not df_payments.empty:
        # Channel Filter & Trend Line (Member 3 Requirement)
        col_ctrl, col_chart = st.columns([1, 2])
        
        with col_ctrl:
            st.markdown("#### Channel Telemetry Selector")
            available_channels = sorted(list(df_payments["system_name"].unique()))
            selected_sys = st.selectbox(
                "Filter by Payment System:",
                options=available_channels,
                index=available_channels.index("UPI") if "UPI" in available_channels else 0
            )
            st.caption(f"Inspecting transaction volume for **{selected_sys}** across reporting periods.")
            
            # Show summary stats for selected channel
            df_chan = df_payments[df_payments["system_name"] == selected_sys]
            if not df_chan.empty:
                st.dataframe(
                    df_chan[["period", "volume_crore", "value_inr_crore"]].rename(
                        columns={
                            "period": "Period",
                            "volume_crore": "Volume (Cr Txns)",
                            "value_inr_crore": "Value (₹ Crore)"
                        }
                    ),
                    hide_index=True,
                    use_container_width=True
                )
                
        with col_chart:
            st.plotly_chart(plot_rbi_system_trend(df_payments, selected_sys), use_container_width=True)
            
        st.markdown("#### Comprehensive YoY Growth Comparison (Feb 2024 vs Feb 2025)")
        st.plotly_chart(plot_rbi_payment_growth(df_payments), use_container_width=True)
        render_data_provenance("Payment System Indicators", "Reserve Bank of India", "February 2025 Bulletin", "https://www.rbi.org.in/Scripts/PSIUserView.aspx?Id=45")
    else:
        st.info("Payment indicators dataset unavailable.")

# 2. TAB: Fraud Trends
with tab_frauds:
    df_frauds = load_public_dataset("rbi_frauds")
    st.markdown("### Domestic Payment Frauds Registry (RBI CPFIR)")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        render_kpi_card(
            title="Reported Fraud Incidents",
            value="1,83,172",
            subtext="February 2025 CPFIR registry",
            delta_text="1 in every 1,07,458 txns",
            badge_color="amber"
        )
    with f2:
        render_kpi_card(
            title="Monthly Fraud Value",
            value="₹287.8 Cr",
            subtext="Reported to Central Registry",
            delta_text="-14.2% vs Nov 2024 peak",
            badge_color="emerald"
        )
    with f3:
        render_kpi_card(
            title="Fraud to Sales (FTS)",
            value="0.121 bps",
            subtext="Down from 0.240 bps in May 2024",
            delta_text="Systemic Hygiene Improving",
            badge_color="emerald"
        )
        
    if not df_frauds.empty:
        st.plotly_chart(plot_rbi_fraud_trends(df_frauds), use_container_width=True)
        render_data_provenance("Central Payments Fraud Information Registry (CPFIR)", "Reserve Bank of India", "Sept 2022 - Feb 2025", "https://www.rbi.org.in/")
    else:
        st.info("Fraud registry dataset unavailable.")

# 3. TAB: Labour Force (PLFS)
with tab_plfs:
    df_plfs = load_public_dataset("plfs")
    st.markdown("### Labour Force & Workforce Distribution (PLFS 2023-24)")
    
    if not df_plfs.empty:
        # Sector Comparison Bar Chart (Member 3 Requirement)
        st.markdown("#### National Workforce Ratios Across Sectors (Rural vs. Urban vs. Combined)")
        all_india_sectors = df_plfs[(df_plfs["state"] == "All India") & (df_plfs["gender"] == "Person")]
        
        fig_sec = px.bar(
            all_india_sectors,
            x="sector",
            y=["lfpr_pct", "wpr_pct", "ur_pct"],
            barmode="group",
            color_discrete_map={
                "lfpr_pct": "#818CF8",
                "wpr_pct": "#10B981",
                "ur_pct": "#FB7185"
            },
            labels={
                "sector": "Sector",
                "value": "Percentage (%)",
                "variable": "Indicator"
            }
        )
        fig_sec.update_layout(
            **DARK_LAYOUT,
            title="PLFS 2023-24: LFPR, WPR, and Unemployment Rate Across Sectors",
            height=340
        )
        st.plotly_chart(fig_sec, use_container_width=True)
        
        col_chart, col_table = st.columns([3, 2])
        with col_chart:
            st.plotly_chart(plot_plfs_wpr_by_state(df_plfs), use_container_width=True)
            render_data_provenance("Periodic Labour Force Survey (PLFS)", "MoSPI NSSO", "July 2023 - June 2024", "https://microdata.gov.in/nada/index.php/catalog")
            
        with col_table:
            st.markdown("#### State-Level Indicators Table")
            state_select = st.multiselect(
                "Filter States",
                options=sorted(list(df_plfs["state"].unique())),
                default=["All India", "Maharashtra", "Tamil Nadu", "Karnataka", "Uttar Pradesh", "Gujarat"]
            )
            df_filtered = df_plfs[df_plfs["state"].isin(state_select) & (df_plfs["sector"] == "Combined")]
            st.dataframe(
                df_filtered[["state", "lfpr_pct", "wpr_pct", "ur_pct", "avg_daily_earnings_regular_inr"]].rename(
                    columns={
                        "state": "State",
                        "lfpr_pct": "LFPR (%)",
                        "wpr_pct": "WPR (%)",
                        "ur_pct": "UR (%)",
                        "avg_daily_earnings_regular_inr": "Regular Wage (₹/day)"
                    }
                ),
                hide_index=True,
                use_container_width=True
            )

# 4. TAB: HCES Household Consumption
with tab_hces:
    df_hces = load_public_dataset("hces")
    st.markdown("### Household Consumption Expenditure Survey (HCES 2023-24)")
    
    if not df_hces.empty:
        sector_choice = st.radio("Select Consumption Sector", options=["Urban", "Rural"], horizontal=True)
        st.plotly_chart(plot_hces_fractiles(df_hces, sector=sector_choice), use_container_width=True)
        
        st.markdown(
            """
            **Key Economic Takeaway:** In bottom 5% households, food expenditures represent over 50% of monthly budgets, leaving minimal margin for discretionary buffers or cyber-fraud recovery. Higher fractiles exhibit expanding non-food and discretionary allocations.
            """
        )
        render_data_provenance("Household Consumption Expenditure Survey", "MoSPI NSSO", "August 2023 - July 2024", "https://microdata.gov.in/nada/index.php/catalog")

# 5. TAB: ASUSE Unincorporated Enterprises
with tab_asuse:
    df_asuse = load_public_dataset("asuse")
    st.markdown("### Unincorporated Enterprises & Informal Economy (ASUSE 2023-24)")
    
    if not df_asuse.empty:
        st.dataframe(
            df_asuse.rename(
                columns={
                    "broad_activity": "Sector Activity",
                    "enterprise_type": "Enterprise Type",
                    "annual_gva_per_enterprise_inr": "Annual GVA per Enterprise (₹)",
                    "avg_workers_per_ent": "Avg Workforce (Workers)",
                    "pct_share_enterprises": "National Enterprise Share (%)",
                    "avg_annual_emoluments_hired_worker_inr": "Avg Annual Emoluments / Hired Worker (₹)"
                }
            ),
            hide_index=True,
            use_container_width=True
        )
        st.markdown(
            """
            **Analytical Insight:** Own Account Enterprises (OAEs) represent over 85% of unincorporated units in India with average annual Gross Value Added between ₹1.48L and ₹1.92L. Establishments employing hired labour generate 3x to 4x higher productivity.
            """
        )
        render_data_provenance("Annual Survey of Unincorporated Sector Enterprises (ASUSE)", "MoSPI NSSO", "FY 2023-24", "https://microdata.gov.in/nada/index.php/catalog")

render_footer()
