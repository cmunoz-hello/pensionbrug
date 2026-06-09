import streamlit as st
import tempfile
import os
import plotly.graph_objects as go
import numpy as np

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

# ── Brand colors ──
CORAL  = "#C8471F"
ORANGE = "#E07530"
PEACH  = "#F0A96E"
SLATE  = "#3D4A5C"
CREAM  = "#F5EDE4"

# ── Custom CSS ──
st.markdown("""
<style>
    .main { background-color: #F5EDE4; }
    .stApp { background-color: #F5EDE4; }
    h1, h2, h3 { color: #3D4A5C; }
    .stAlert { border-radius: 8px; }
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #DDD0C4;
        border-radius: 8px;
        padding: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown(f"<h1 style='color:{CORAL}'>🌉 PensionBrug</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#3D4A5C; font-size:18px;'>Your pension in one place — gap detection, projections, and personalised guidance</p>", unsafe_allow_html=True)
st.divider()

# ── Session state ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pension_data" not in st.session_state:
    st.session_state.pension_data = None

# ══════════════════════════════════════════════
# STEP 1: Personal details + Pillar 1
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 1 — About You & AOW (Pillar 1)</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    birth_year = st.number_input("Birth year", min_value=1950, max_value=2005, value=2000)
with col2:
    years_in_nl = st.number_input("Years lived/worked in NL", min_value=0, max_value=50, value=4)
with col3:
    years_abroad = st.number_input("Years abroad (without voluntary AOW insurance)", min_value=0, max_value=50, value=2)

aow = calculate_aow(birth_year, years_in_nl, years_abroad)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Current age", f"{aow['current_age']} years old")
with col_b:
    st.metric("Years until retirement", f"{aow['years_until_retirement']} years")
with col_c:
    st.metric("Projected AOW", f"€{aow['aow_monthly_single']:,}/month")

if aow['aow_percentage'] < 100:
    st.warning(f"⚠️ Due to {years_abroad} year(s) abroad, your AOW is reduced to {aow['aow_percentage']}% of the full benefit (€{aow['aow_annual_single']:,}/year). You may be able to buy back missing years via the SVB.")
else:
    st.success(f"✅ Full AOW entitlement: €{aow['aow_annual_single']:,}/year (€{aow['aow_monthly_single']:,}/month)")

st.divider()

# ══════════════════════════════════════════════
# STEP 2: Pillar 2
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 2 — Employer Pension (Pillar 2)</h2>", unsafe_allow_html=True)

upload_method = st.radio(
    "How would you like to add your Pillar 2 data?",
    ["Upload UPO PDF", "Enter manually"]
)

pillar2_annual = 0
fund_name = None

if upload_method == "Upload UPO PDF":
    st.info("📄 Your UPO is the annual pension statement from your employer's pension fund. Download it from your fund's portal (e.g. mijnpfzw.nl, mijnabp.nl) and upload it here.")
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

            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.metric("Pension fund", fund_name.split("(")[0].strip())
            with col_p2:
                accrued = upo_data['accrued_pension_annual']
                st.metric("Accrued to date", f"€{accrued:,}/year" if accrued else "N/A")
            with col_p3:
                st.metric("Projected at retirement", f"€{pillar2_annual:,}/year")
        else:
            st.warning("Could not automatically read your UPO. Please enter manually below.")
            pillar2_annual = st.number_input("Projected annual pension from UPO (€)", min_value=0, value=0)
            fund_name = st.text_input("Pension fund name")

else:
    col1, col2 = st.columns(2)
    with col1:
        pillar2_annual = st.number_input("Projected annual pension (€)", min_value=0, valu
