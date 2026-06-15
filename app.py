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

# Page config
st.set_page_config(
    page_title="PensionBrug",
    layout="wide"
)

# Brand colors
CORAL  = "#C8471F"
ORANGE = "#E07530"
PEACH  = "#F0A96E"
SLATE  = "#3D4A5C"
CREAM  = "#F5EDE4"

# Custom CSS
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

# Header
st.markdown(f"<h1 style='color:{CORAL}'>PensionBrug</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#3D4A5C; font-size:18px;'>Your pension in one place: gap detection, projections, and personalised guidance</p>", unsafe_allow_html=True)
st.divider()

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pension_data" not in st.session_state:
    st.session_state.pension_data = None

# ══════════════════════════════════════════════
# STEP 1: Personal details + Pillar 1
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 1: About You and AOW (Pillar 1)</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    birth_year = st.number_input(
        "Birth year",
        min_value=1950, max_value=2005, value=2000
    )
with col2:
    age_arrived_nl = st.number_input(
        "Age when you first started living or working in NL",
        min_value=0, max_value=50, value=18,
        help="This is when your AOW insurance started. Nationality does not matter, it counts from when you first lived or worked here."
    )
with col3:
    years_abroad = st.number_input(
        "Years spent abroad since arriving (without voluntary AOW insurance)",
        min_value=0, max_value=50, value=0,
        help="Any years outside NL where you did not pay voluntary AOW contributions reduce your entitlement by 2% per year."
    )

aow = calculate_aow(birth_year, age_arrived_nl, years_abroad)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Current age", f"{aow['current_age']} years old")
with col_b:
    st.metric("Years until retirement", f"{aow['years_until_retirement']} years")
with col_c:
    st.metric("Projected AOW", f"€{aow['aow_monthly_single']:,}/month")

if aow['aow_percentage'] < 100:
    missing_years = 50 - aow['total_years_insured']
    st.warning(f"⚠️ Your AOW is {aow['aow_percentage']}% of the full benefit (€{aow['aow_annual_single']:,}/year). You arrived at age {age_arrived_nl} and have {round(aow['total_years_insured'])} insured years projected. You are missing approximately {round(missing_years)} years. You may be able to buy back some gaps via the SVB (svb.nl).")
else:
    st.success(f"✅ Full AOW entitlement projected: €{aow['aow_annual_single']:,}/year (€{aow['aow_monthly_single']:,}/month) based on {round(aow['total_years_insured'])} insured years.")

st.divider()

# ══════════════════════════════════════════════
# STEP 2: Pillar 2
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 2: Employer Pension (Pillar 2)</h2>", unsafe_allow_html=True)

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
        pillar2_annual = st.number_input("Projected annual pension (€)", min_value=0, value=0)
    with col2:
        fund_name = st.text_input("Pension fund name (optional)")
    if pillar2_annual > 0:
        st.success(f"✅ Pillar 2: €{pillar2_annual:,}/year (€{pillar2_annual//12:,}/month)")

st.divider()

# ══════════════════════════════════════════════
# STEP 3: Target income
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 3: Your Retirement Goal</h2>", unsafe_allow_html=True)

st.markdown("A common target is **70 to 80% of your current salary**. The average Dutch worker aims for around €2,000 to €2,500/month net.")

target_monthly = st.slider(
    "What monthly income do you want at retirement? (€ gross)",
    min_value=500,
    max_value=5000,
    value=2000,
    step=100
)
target_annual = target_monthly * 12
st.caption(f"That's €{target_annual:,} per year gross")

st.divider()

# ══════════════════════════════════════════════
# STEP 4: Full picture & gap analysis
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 4: Your Pension Picture</h2>", unsafe_allow_html=True)

gap_data = calculate_gap(
    aow_annual=aow["aow_annual_single"],
    pillar2_annual=pillar2_annual,
    pillar3_annual=0,
    target_annual=target_annual,
    birth_year=birth_year
)

st.session_state.pension_data = gap_data

# Summary metrics
sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
with sum_col1:
    st.metric("Pillar 1 (AOW)", f"€{aow['aow_monthly_single']:,}/mo")
with sum_col2:
    st.metric("Pillar 2 (Employer)", f"€{pillar2_annual//12:,}/mo")
with sum_col3:
    st.metric("Total projected", f"€{gap_data['monthly_projected']:,}/mo")
with sum_col4:
    delta = gap_data['monthly_projected'] - target_monthly
    delta_str = f"€{abs(delta):,}/mo {'surplus' if delta >= 0 else 'gap'}"
    st.metric("Your target", f"€{target_monthly:,}/mo", delta=delta_str)

# Bar chart
fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    name="AOW (Pillar 1)",
    x=["Your Projected Pension", "Your Target"],
    y=[aow["aow_annual_single"], 0],
    marker_color=PEACH
))
fig_bar.add_trace(go.Bar(
    name="Employer Pension (Pillar 2)",
    x=["Your Projected Pension", "Your Target"],
    y=[pillar2_annual, 0],
    marker_color=ORANGE
))
fig_bar.add_trace(go.Bar(
    name="Target Income",
    x=["Your Projected Pension", "Your Target"],
    y=[0, target_annual],
    marker_color=SLATE
))
fig_bar.update_layout(
    title="Annual pension overview (€)",
    yaxis_title="€ per year",
    barmode="stack",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)
st.plotly_chart(fig_bar, use_container_width=True)

# Growth timeline
st.subheader("Pillar 2 pot growth over time")
st.caption("How your DC pension pot is expected to grow until retirement, assuming a 5% annual return based on the historical equity market average.")

fig_timeline = go.Figure()
fig_timeline.add_trace(go.Scatter(
    x=gap_data["timeline_years"],
    y=gap_data["timeline_values"],
    mode="lines",
    fill="tozeroy",
    line=dict(color=CORAL, width=2),
    fillcolor="rgba(200,71,31,0.1)",
    name="Expected pension value"
))
fig_timeline.add_hline(
    y=target_annual,
    line_dash="dash",
    line_color=SLATE,
    annotation_text="Your target",
    annotation_position="top right"
)
fig_timeline.update_layout(
    xaxis_title="Year",
    yaxis_title="€ per year",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Monte Carlo
st.subheader("Monte Carlo Simulation: Your Pillar 2 Range")
st.caption(f"Based on {gap_data['num_simulations']:,} simulations of your Pillar 2 pot's possible growth. Your AOW stays fixed.")

with st.expander("Why does only Pillar 2 vary?"):
    st.markdown(f"""
    * **AOW (€{aow['aow_annual_single']:,}/yr)** is a fixed government formula. It is not an investment, so there is no risk attached to it.
    * **Pillar 2 (€{pillar2_annual:,}/yr)** is your UPO's projection. Under WTP this is now a personal investment pot, so the real payout depends on market returns between now and retirement.
    * **"Expected"** equals your UPO projection exactly. It sits in the middle of the range.
    * **"Pessimistic"** and **"Optimistic"** show weaker or stronger market returns over your remaining **{gap_data['years_until_retirement']} years**.
    """)

mc1, mc2, mc3, mc4 = st.columns(4)
with mc1:
    diff1 = gap_data['mc_pessimistic'] - target_annual
    st.metric(
        "Pessimistic total pension",
        f"€{gap_data['mc_pessimistic']:,}/yr",
        delta=f"€{diff1:,}/yr vs target",
        delta_color="normal" if diff1 >= 0 else "inverse",
        help="10th percentile. Weaker investment returns on your Pillar 2 pot."
    )
with mc2:
    diff2 = gap_data['mc_expected'] - target_annual
    st.metric(
        "Expected total pension",
        f"€{gap_data['mc_expected']:,}/yr",
        delta=f"€{diff2:,}/yr vs target",
        delta_color="normal" if diff2 >= 0 else "inverse",
        help="Median outcome. Matches your UPO's own projection."
    )
with mc3:
    diff3 = gap_data['mc_optimistic'] - target_annual
    st.metric(
        "Optimistic total pension",
        f"€{gap_data['mc_optimistic']:,}/yr",
        delta=f"€{diff3:,}/yr vs target",
        delta_color="normal" if diff3 >= 0 else "inverse",
        help="90th percentile. Stronger investment returns on your Pillar 2 pot."
    )
with mc4:
    st.metric(
        "Probability of meeting target",
        f"{gap_data['prob_meeting_target']}%",
        help=f"Share of simulations where AOW plus Pillar 2 reaches your €{target_monthly:,}/month target."
    )

st.caption(
    f"Your target: **€{target_annual:,}/year (€{target_monthly:,}/month)**. "
    f"AOW (fixed): €{aow['aow_annual_single']:,}/year. "
    f"Pillar 2 (UPO projection): €{pillar2_annual:,}/year."
)

# ══════════════════════════════════════════════
# STEP 5: Pillar 3 recommendations
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 5: Close the Gap with Pillar 3</h2>", unsafe_allow_html=True)

recommendations = get_recommendations(
    gap_annual=gap_data["gap"],
    monthly_contribution_needed=gap_data["monthly_contribution_needed"],
    years_until_retirement=gap_data["years_until_retirement"]
)

if gap_data["has_gap"]:
    gap_val = gap_data['gap']
    monthly_gap = gap_data['monthly_gap']
    years_ret = gap_data['years_until_retirement']
    monthly_contrib = gap_data['monthly_contribution_needed']

    st.markdown(f"""
    <div style='background-color:white; border-left: 4px solid {CORAL}; padding: 16px; border-radius: 8px; margin-bottom: 16px;'>
        <h4 style='color:{CORAL}; margin:0'>Your pension gap: €{gap_val:,}/year (€{monthly_gap:,}/month)</h4>
        <p style='margin:8px 0 0 0'>To close this gap by retirement in <b>{years_ret} years</b>,
        you would need to invest approximately <b>€{monthly_contrib:,}/month</b>
        into a Pillar 3 product starting today.</p>
        <p style='margin:4px 0 0 0; color:grey; font-size:13px'>
        This assumes a 5% average annual return and a 20 year retirement period.
        Contributions are often tax deductible (jaarruimte).</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.success("✅ Your pension looks on track! You may still want to consider Pillar 3 for extra security or early retirement.")

st.write(recommendations["message"])

cols = st.columns(3)
for idx, provider in enumerate(recommendations["providers"]):
    with cols[idx]:
        name = provider['name']
        ptype = provider['type']
        desc = provider['description']
        best_for = provider['best_for']
        min_monthly = provider['min_monthly']
        url = provider['url']

        st.markdown(f"""
        <div style='background-color:white; border: 1px solid #DDD0C4; border-radius: 8px; padding: 16px;'>
            <h4 style='color:{CORAL}; margin-top:0'>{name}</h4>
            <p style='color:{SLATE}; font-style:italic; margin:0'>{ptype}</p>
            <hr style='border-color:#DDD0C4'>
            <p>{desc}</p>
            <p><b>Best for:</b> {best_for}</p>
            <p><b>From:</b> €{min_monthly}/month</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(f"Visit {name}", url)

st.divider()

# ══════════════════════════════════════════════
# STEP 6: Chat assistant
# ══════════════════════════════════════════════
st.markdown(f"<h2 style='color:{SLATE}'>Step 6: Ask PensionBrug</h2>", unsafe_allow_html=True)
st.write("Ask me anything about your pension, the WTP reform, or your gap.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("e.g. What does WTP mean for me? What is a pension gap?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = get_response(prompt, st.session_state.pension_data)

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
