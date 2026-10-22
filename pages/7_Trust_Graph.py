"""
AAYAM - Page 7: Trust Graph
NetworkX and Plotly knowledge graph mapping entities, threat vectors, delivery channels,
financial consequences, and statutory defense frameworks.
"""
import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from src.ui.theme import apply_theme
from src.ui.components import (
    render_header, render_kpi_card, render_alert_box,
    render_data_provenance, render_footer
)
from src.utils.config import COLOR_BORDER

st.set_page_config(page_title="Trust Graph — AAYAM", page_icon="🕸️", layout="wide")
apply_theme()

render_header(
    title="Trust Graph: Threat Vectors & Defense Frameworks",
    subtitle="Knowledge graph representing structural relationships among delivery channels, cyber threats, and statutory mitigations.",
    badge_text="Module 7",
    badge_type="emerald"
)

render_alert_box(
    title="Graph Provenance & Scope",
    message="Relationships in this graph are derived strictly from published cybersecurity taxonomies (MITRE ATT&CK, CERT-In, RBI CPFIR). It depicts systemic threat mechanisms and official defense mechanisms, never unverified allegations against individuals.",
    alert_type="info"
)

# 1. Build NetworkX Knowledge Graph
@st.cache_data
def build_knowledge_graph():
    G = nx.DiGraph()
    
    # Node types and styling
    # Types: Channel, Threat, Target, Consequence, Defense
    nodes = [
        # Channels
        ("SMS_SMISHING", {"label": "SMS / Smishing", "type": "Channel", "color": "#6366F1"}),
        ("WHATSAPP_CHAT", {"label": "WhatsApp / Telegram", "type": "Channel", "color": "#6366F1"}),
        ("VOICE_CALL", {"label": "Spoofed Voice Call", "type": "Channel", "color": "#6366F1"}),
        ("FAKE_WEB_PORTAL", {"label": "Lookalike Web Portal", "type": "Channel", "color": "#6366F1"}),
        
        # Threats / Techniques
        ("MALICIOUS_APK", {"label": "Malicious Android APK", "type": "Threat", "color": "#F43F5E"}),
        ("REMOTE_SCREEN_TOOL", {"label": "Remote Screen Sharing", "type": "Threat", "color": "#F43F5E"}),
        ("REVERSE_QR_UPI", {"label": "Reverse QR / Collect Prompt", "type": "Threat", "color": "#F43F5E"}),
        ("DIGITAL_ARREST_LURE", {"label": "Digital Arrest Extortion", "type": "Threat", "color": "#F43F5E"}),
        ("SIM_SWAP_ATTACK", {"label": "SIM Swap / eSIM Transfer", "type": "Threat", "color": "#F43F5E"}),
        ("TASK_PREPAID_FRAUD", {"label": "Prepaid Task Trap", "type": "Threat", "color": "#F43F5E"}),
        
        # Targets / Vulnerabilities
        ("SMS_OTP_ACCESS", {"label": "SMS 2FA OTP Interception", "type": "Vulnerability", "color": "#F59E0B"}),
        ("UPI_PIN_EXPOSURE", {"label": "UPI PIN Deception", "type": "Vulnerability", "color": "#F59E0B"}),
        ("BANK_CREDENTIALS", {"label": "Net Banking Login Theft", "type": "Vulnerability", "color": "#F59E0B"}),
        ("PAN_AADHAAR_ID", {"label": "Identity Documents Misuse", "type": "Vulnerability", "color": "#F59E0B"}),
        
        # Consequences
        ("UNAUTHORIZED_DEBIT", {"label": "Unauthorized Bank Debit", "type": "Consequence", "color": "#FB7185"}),
        ("LIFELONG_SAVINGS_LOSS", {"label": "Life Savings Depletion", "type": "Consequence", "color": "#FB7185"}),
        ("FRAUDULENT_LOANS", {"label": "Fraudulent Instant Loans", "type": "Consequence", "color": "#FB7185"}),
        
        # Statutory Defenses & Mitigations
        ("HELPLINE_1930", {"label": "1930 Cyber Fraud Helpline", "type": "Defense", "color": "#10B981"}),
        ("CYBERCRIME_PORTAL", {"label": "National Cyber Crime Portal", "type": "Defense", "color": "#10B981"}),
        ("RBI_ZERO_LIABILITY", {"label": "RBI 72-Hour Zero Liability", "type": "Defense", "color": "#10B981"}),
        ("MAADHAAR_LOCK", {"label": "Aadhaar Biometric Lock", "type": "Defense", "color": "#10B981"}),
        ("AUTHENTICATOR_2FA", {"label": "App-Based Authenticator 2FA", "type": "Defense", "color": "#10B981"})
    ]
    
    for n, attr in nodes:
        G.add_node(n, **attr)
        
    edges = [
        # Channels deliver Threats
        ("SMS_SMISHING", "MALICIOUS_APK", {"relationship": "delivers payload"}),
        ("SMS_SMISHING", "FAKE_WEB_PORTAL", {"relationship": "contains link"}),
        ("WHATSAPP_CHAT", "TASK_PREPAID_FRAUD", {"relationship": "initiates contact"}),
        ("WHATSAPP_CHAT", "MALICIOUS_APK", {"relationship": "sends untrusted file"}),
        ("VOICE_CALL", "REMOTE_SCREEN_TOOL", {"relationship": "instructs installation"}),
        ("VOICE_CALL", "DIGITAL_ARREST_LURE", {"relationship": "impersonates authority"}),
        ("VOICE_CALL", "SIM_SWAP_ATTACK", {"relationship": "tricks SMS forward"}),
        
        # Threats exploit Targets
        ("MALICIOUS_APK", "SMS_OTP_ACCESS", {"relationship": "reads incoming SMS"}),
        ("REMOTE_SCREEN_TOOL", "BANK_CREDENTIALS", {"relationship": "captures screen credentials"}),
        ("REVERSE_QR_UPI", "UPI_PIN_EXPOSURE", {"relationship": "tricks user to enter PIN"}),
        ("SIM_SWAP_ATTACK", "SMS_OTP_ACCESS", {"relationship": "redirects all carrier OTPs"}),
        ("DIGITAL_ARREST_LURE", "BANK_CREDENTIALS", {"relationship": "demands RTGS transfer"}),
        
        # Targets lead to Consequences
        ("SMS_OTP_ACCESS", "UNAUTHORIZED_DEBIT", {"relationship": "authorizes transfer"}),
        ("UPI_PIN_EXPOSURE", "UNAUTHORIZED_DEBIT", {"relationship": "triggers immediate debit"}),
        ("BANK_CREDENTIALS", "UNAUTHORIZED_DEBIT", {"relationship": "executes unauthorized payment"}),
        ("DIGITAL_ARREST_LURE", "LIFELONG_SAVINGS_LOSS", {"relationship": "extorts life savings"}),
        ("PAN_AADHAAR_ID", "FRAUDULENT_LOANS", {"relationship": "applies for instant loan"}),
        
        # Defenses mitigate Consequences & Threats
        ("HELPLINE_1930", "UNAUTHORIZED_DEBIT", {"relationship": "freezes transit funds"}),
        ("RBI_ZERO_LIABILITY", "UNAUTHORIZED_DEBIT", {"relationship": "mandates bank compensation"}),
        ("MAADHAAR_LOCK", "PAN_AADHAAR_ID", {"relationship": "prevents biometric misuse"}),
        ("AUTHENTICATOR_2FA", "SMS_OTP_ACCESS", {"relationship": "replaces vulnerable SMS OTP"}),
        ("CYBERCRIME_PORTAL", "LIFELONG_SAVINGS_LOSS", {"relationship": "coordinates inter-bank lien"})
    ]
    
    for u, v, attr in edges:
        G.add_edge(u, v, **attr)
        
    return G

G = build_knowledge_graph()

# 2. Controls & Search
c1, c2 = st.columns([2, 1])
with c1:
    search_node = st.selectbox(
        "Inspect Specific Node in Network:",
        options=["All Nodes"] + sorted([G.nodes[n]["label"] for n in G.nodes])
    )
with c2:
    filter_type = st.multiselect(
        "Filter Node Categories:",
        options=["Channel", "Threat", "Vulnerability", "Consequence", "Defense"],
        default=["Channel", "Threat", "Vulnerability", "Consequence", "Defense"]
    )

# 3. Generate Graph Visualization using Plotly & Spring Layout
pos = nx.spring_layout(G, seed=42, k=0.9, iterations=50)

edge_x = []
edge_y = []
for edge in G.edges():
    u, v = edge
    # Check if both nodes pass filter
    if G.nodes[u]["type"] in filter_type and G.nodes[v]["type"] in filter_type:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1.5, color="rgba(148, 163, 184, 0.4)"),
    hoverinfo="none",
    mode="lines"
)

node_x = []
node_y = []
node_text = []
node_colors = []

for node in G.nodes():
    if G.nodes[node]["type"] in filter_type:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        attr = G.nodes[node]
        node_text.append(f"{attr['label']} ({attr['type']})")
        node_colors.append(attr["color"])

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode="markers+text",
    text=[G.nodes[n]["label"] for n in G.nodes() if G.nodes[n]["type"] in filter_type],
    textposition="top center",
    hovertext=node_text,
    hoverinfo="text",
    marker=dict(
        showscale=False,
        color=node_colors,
        size=18,
        line=dict(width=2, color="#090D16")
    )
)

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=20, r=20, t=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=560
    )
)

st.plotly_chart(fig, use_container_width=True)

# 4. Legend & Relationship Matrix
st.markdown("### 🏷️ Graph Taxonomy Legend")
leg1, leg2, leg3, leg4, leg5 = st.columns(5)
with leg1:
    st.markdown("🔵 <span style='color: #6366F1;'>**Channel:** Delivery medium</span>", unsafe_allow_html=True)
with leg2:
    st.markdown("🔴 <span style='color: #F43F5E;'>**Threat:** Exploitation tactic</span>", unsafe_allow_html=True)
with leg3:
    st.markdown("🟠 <span style='color: #F59E0B;'>**Target:** Vulnerability</span>", unsafe_allow_html=True)
with leg4:
    st.markdown("🟣 <span style='color: #FB7185;'>**Impact:** Economic harm</span>", unsafe_allow_html=True)
with leg5:
    st.markdown("🟢 <span style='color: #10B981;'>**Defense:** Statutory mitigation</span>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📋 Sourced Relationship Ledger")

edge_data = []
for u, v, data in G.edges(data=True):
    edge_data.append({
        "Source Entity": G.nodes[u]["label"],
        "Source Type": G.nodes[u]["type"],
        "Relationship": data.get("relationship", "connects to"),
        "Target Entity": G.nodes[v]["label"],
        "Target Type": G.nodes[v]["type"],
        "Provenance": "CERT-In Advisories / RBI Guidelines"
    })

df_edges = pd.DataFrame(edge_data)
st.dataframe(df_edges, use_container_width=True, hide_index=True)

render_data_provenance(
    dataset_name="Cyber Threat Knowledge Graph",
    publisher="CERT-In, NPCI & RBI Frameworks",
    reference_period="2024 Taxonomy",
    source_url="https://www.cert-in.org.in/"
)

render_footer()
