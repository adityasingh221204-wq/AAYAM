"""
AAYAM - Plotly Visualization Components
Modern, dark-theme interactive financial and macroeconomic charts.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from src.utils.config import (
    COLOR_BG, COLOR_PRIMARY_SURFACE, COLOR_SECONDARY_SURFACE,
    COLOR_BORDER, COLOR_ACCENT_PRIMARY, COLOR_ACCENT_SECONDARY,
    COLOR_WARNING, COLOR_DANGER, COLOR_TEXT_LIGHT, COLOR_TEXT_MUTED
)

# Standard Dark Theme Layout Dict for Plotly
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLOR_TEXT_LIGHT, family="sans-serif", size=12),
    margin=dict(l=40, r=30, t=50, b=40),
    xaxis=dict(
        gridcolor=COLOR_BORDER,
        zerolinecolor=COLOR_BORDER,
        tickfont=dict(color=COLOR_TEXT_MUTED)
    ),
    yaxis=dict(
        gridcolor=COLOR_BORDER,
        zerolinecolor=COLOR_BORDER,
        tickfont=dict(color=COLOR_TEXT_MUTED)
    ),
    legend=dict(
        bgcolor="rgba(15, 23, 42, 0.8)",
        bordercolor=COLOR_BORDER,
        borderwidth=1,
        font=dict(color=COLOR_TEXT_LIGHT)
    )
)


def plot_cashflow_breakdown(income: float, essential: float, discretionary: float, emi: float, surplus: float) -> go.Figure:
    """Waterfall or bar chart visualizing monthly cashflow allocation."""
    categories = ["Income", "Essential Living", "Discretionary", "Debt / EMI", "Net Surplus"]
    amounts = [income, -essential, -discretionary, -emi, surplus]
    measures = ["absolute", "relative", "relative", "relative", "total"]
    
    fig = go.Figure(go.Waterfall(
        name="Cash Flow",
        orientation="v",
        measure=measures,
        x=categories,
        textposition="outside",
        text=[f"₹{abs(a):,.0f}" for a in amounts],
        y=amounts,
        connector={"line": {"color": COLOR_BORDER}},
        decreasing={"marker": {"color": COLOR_DANGER}},
        increasing={"marker": {"color": COLOR_ACCENT_PRIMARY}},
        totals={"marker": {"color": COLOR_ACCENT_SECONDARY}}
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title="Monthly Cash Flow Allocation Breakdown",
        showlegend=False,
        height=380
    )
    return fig


def plot_scenario_trajectories(baseline_traj: list[dict], scenario_traj: list[dict], duration: int) -> go.Figure:
    """Side-by-side comparative line chart for ArthSim savings trajectories."""
    df_b = pd.DataFrame(baseline_traj)
    df_s = pd.DataFrame(scenario_traj)
    
    fig = go.Figure()
    
    # Baseline line
    fig.add_trace(go.Scatter(
        x=df_b["month"],
        y=df_b["savings_balance"],
        mode="lines+markers",
        name="Baseline Savings",
        line=dict(color=COLOR_ACCENT_PRIMARY, width=3, dash="solid"),
        marker=dict(size=6)
    ))
    
    # Scenario line
    fig.add_trace(go.Scatter(
        x=df_s["month"],
        y=df_s["savings_balance"],
        mode="lines+markers",
        name="Shock Scenario Savings",
        line=dict(color=COLOR_DANGER, width=3, dash="dot"),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=f"Savings Balance Trajectory: Baseline vs Scenario ({duration} Months)",
        xaxis_title="Month",
        yaxis_title="Savings Balance (₹ INR)",
        height=420
    )
    return fig


def plot_rbi_payment_growth(df_payments: pd.DataFrame) -> go.Figure:
    """Bar chart comparing major payment systems in February 2025 vs February 2024."""
    if df_payments is None or df_payments.empty:
        return go.Figure()
        
    # Filter key retail systems for comparison
    key_systems = ["UPI", "NEFT", "IMPS", "Credit Cards", "Debit Cards", "Wallets"]
    df_sub = df_payments[
        df_payments["system_name"].isin(key_systems) & 
        df_payments["period"].isin(["February 2024", "February 2025"])
    ]
    
    fig = px.bar(
        df_sub,
        x="system_name",
        y="volume_crore",
        color="period",
        barmode="group",
        color_discrete_map={
            "February 2024": "#6366F1",
            "February 2025": "#10B981"
        },
        labels={"volume_crore": "Volume (Crore Transactions)", "system_name": "Payment Channel"}
    )
    
    fig.update_layout(
        **DARK_LAYOUT,
        title="RBI Payment Volumes: YoY Growth (Feb 2024 vs Feb 2025)",
        height=380
    )
    return fig


def plot_rbi_fraud_trends(df_frauds: pd.DataFrame) -> go.Figure:
    """Dual-axis line chart for domestic payment frauds (Volume vs Basis Points)."""
    if df_frauds is None or df_frauds.empty:
        return go.Figure()
        
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_frauds["month_year"],
        y=df_frauds["fraud_value_inr_crore"],
        name="Fraud Value (₹ Crore)",
        marker_color="rgba(244, 63, 94, 0.65)",
        yaxis="y"
    ))
    
    fig.add_trace(go.Scatter(
        x=df_frauds["month_year"],
        y=df_frauds["fts_basis_points"],
        name="Fraud to Sales (bps)",
        mode="lines+markers",
        line=dict(color="#FBBF24", width=3),
        yaxis="y2"
    ))
    
    layout = dict(DARK_LAYOUT)
    layout.update(
        title="Domestic Payment Frauds Reported to RBI Central Registry (CPFIR)",
        height=400,
        xaxis=dict(tickangle=-45, gridcolor=COLOR_BORDER),
        yaxis=dict(title="Fraud Value (₹ Cr)", gridcolor=COLOR_BORDER),
        yaxis2=dict(
            title="Fraud to Sales (Basis Points)",
            overlaying="y",
            side="right",
            gridcolor="rgba(0,0,0,0)",
            tickfont=dict(color="#FBBF24")
        )
    )
    fig.update_layout(**layout)
    return fig


def plot_plfs_wpr_by_state(df_plfs: pd.DataFrame) -> go.Figure:
    """State-wise Worker Population Ratio and Unemployment Rate chart."""
    if df_plfs is None or df_plfs.empty:
        return go.Figure()
        
    df_states = df_plfs[(df_plfs["sector"] == "Combined") & (df_plfs["state"] != "All India")]
    
    fig = px.bar(
        df_states.sort_values("wpr_pct", ascending=True),
        x="wpr_pct",
        y="state",
        orientation="h",
        color="ur_pct",
        color_continuous_scale="Viridis",
        labels={"wpr_pct": "Worker Population Ratio (%)", "ur_pct": "Unemployment Rate (%)", "state": "State"}
    )
    
    fig.update_layout(
        **DARK_LAYOUT,
        title="PLFS 2023-24: Worker Population Ratio & Unemployment Rate Across States",
        height=480
    )
    return fig


def plot_hces_fractiles(df_hces: pd.DataFrame, sector: str = "Urban") -> go.Figure:
    """Monthly Per Capita Consumption Expenditure by fractile classes."""
    if df_hces is None or df_hces.empty:
        return go.Figure()
        
    df_sub = df_hces[df_hces["sector"] == sector]
    
    fig = px.bar(
        df_sub,
        x="fractile_class",
        y="mpce_inr",
        color="food_expenditure_share_pct",
        color_continuous_scale="Tealgrn_r",
        labels={"mpce_inr": "Monthly Per Capita Exp (₹)", "food_expenditure_share_pct": "Food Share (%)", "fractile_class": "Fractile Class"}
    )
    
    fig.update_layout(
        **DARK_LAYOUT,
        title=f"HCES 2023-24: Consumption Distribution & Food Share ({sector} India)",
        height=380
    )
    return fig
