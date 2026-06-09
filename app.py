import streamlit as st
import tempfile
import os
import plotly.graph_objects as go

from pillar1 import calculate_aow
from pillar2 import extract_upo_data, manual_pillar2_input
from gap import calculate_gap
from providers import get_recommendations
from chatbot import get_response

# ── Page config ──
st.set_page_config(
    page_title="PensionBrug",
    page_icon="🌉",
    layout="wide"
)

# ── Header ──
st.title("🌉 PensionBrug")
st.subheader("Your pension in one place")
st.divider()

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pension_data" not in st.session_state:
    st.session_state.pension_data = None

# ── STEP 1: Pillar 1 ──
st.header("Step 1 — Pillar 1: AOW")

col1, col2, col3 = st.columns(3)
with col1:
    birth_year = st.number_input("Birth year", min_value=1950, max_value=2005, value=1990)
with col2:
    years_in_nl = st.number_input("Years lived/worked in NL", min_value=0, max_value=50, value=10)
with col3:
    years_abroad = st.number_input("Years spent abroad (without voluntary AOW insurance)", min_value=0, max_value=50, value=0)

aow = calculate_aow(birth_year, years_in_nl, years_abroad)

st.success(f"✅ AOW entitlement: **€{aow['aow_annual_single']:,}** per year (€{aow['aow_monthly_single']:,}/month) — {aow['aow_percentage']}% of full benefit")

st.divider()

# ── STEP 2: Pillar 2 ──
st.header("Step 2 — Pillar 2: Employer Pension")

upload_method = st.radio(
    "How would you like to add your Pillar 2 data?",
    ["Upload UPO PDF", "Enter manually"]
)

pillar2_annual = 0
fund_name = None

if upload_method == "Upload UPO PDF":
    uploaded_file = st.file_uploader("Upload your UPO PDF", type="pdf")
    
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        
        with st.spinner("Reading your UPO..."):
            upo_data = extract_upo_data(tmp_path)
        
        os.unlink(tmp_path)
        
        if upo_data["projected_pension_annual"]:
            fund_name = upo_data["fund_name"] or "Unknown fund"
            pillar2_annual = upo_data["projected_pension_annual"]
            st.success(f"✅ Found: **{fund_name}** — projected pension €{pillar2_annual:,}/year")
            
            if upo_data["accrued_pension_annual"]:
                st.info(f"Accrued to date: €{upo_data['accrued_pension_annual']:,}/year")
        else:
            st.warning("Could not automatically read your UPO. Please enter manually below.")
            pillar2_annual = st.number_input("Projected annual pension from UPO (€)", min_value=0, value=0)
            fund_name = st.text_input("Pension fund name")

else:
    pillar2_annual = st.number_input("Projected annual pension (€)", min_value=0, value=0)
    fund_name = st.text_input("Pension fund name")
    if pillar2_annual > 0:
        st.success(f"✅ Pillar 2: €{pillar2_annual:,}/year")

st.divider()

# ── STEP 3: Target & Gap ──
st.header("Step 3 — Retirement Target & Gap Analysis")

target_monthly = st.slider(
    "What monthly income do you want at retirement? (€)",
    min_value=500,
    max_value=5000,
    value=2000,
    step=100
)

target_annual = target_monthly * 12

gap_data = calculate_gap(
    aow_annual=aow["aow_annual_single"],
    pillar2_annual=pillar2_annual,
    pillar3_annual=0,
    target_annual=target_annual
)

st.session_state.pension_data = gap_data

# Gap chart
fig = go.Figure(go.Bar(
    x=["AOW (Pillar 1)", "Employer Pension (Pillar 2)", "Target"],
    y=[aow["aow_annual_single"], pillar2_annual, target_annual],
    marker_color=["#E07530", "#C8471F", "#3D4A5C"]
))
fig.update_layout(
    title="Your pension overview (annual, €)",
    yaxis_title="€ per year",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

if gap_data["has_gap"]:
    st.error(f"⚠️ You have a pension gap of **€{gap_data['gap']:,}/year** (€{gap_data['monthly_gap']:,}/month). Your projected pension covers {gap_data['coverage_percentage']}% of your target.")
else:
    st.success(f"✅ Your projected pension covers your target retirement income!")

st.divider()

# ── STEP 4: Pillar 3 Recommendations ──
st.header("Step 4 — Pillar 3 Recommendations")

recommendations = get_recommendations(gap_data["gap"])
st.write(recommendations["message"])

if gap_data["has_gap"]:
    st.info(f"💡 Estimated monthly contribution needed: **€{recommendations['monthly_needed']}**")

cols = st.columns(3)
for idx, provider in enumerate(recommendations["providers"]):
    with cols[idx]:
        st.markdown(f"### {provider['name']}")
        st.markdown(f"*{provider['type']}*")
        st.write(provider["description"])
        st.markdown(f"**Best for:** {provider['best_for']}")
        st.markdown(f"**From:** €{provider['min_monthly']}/month")
        st.link_button(f"Visit {provider['name']}", provider["url"])

st.divider()

# ── STEP 5: Chat assistant ──
st.header("Step 5 — Ask PensionBrug")
st.write("Ask me anything about your pension, the WTP reform, or your gap.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt, st.session_state.pension_data)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
