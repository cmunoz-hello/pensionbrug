# Gap chart - Monte Carlo scenarios
fig = go.Figure()

# Bar chart for pillars
fig.add_trace(go.Bar(
    name="AOW (Pillar 1)",
    x=["Your Pension"],
    y=[aow["aow_annual_single"]],
    marker_color="#F0A96E"
))
fig.add_trace(go.Bar(
    name="Employer Pension (Pillar 2)",
    x=["Your Pension"],
    y=[pillar2_annual],
    marker_color="#E07530"
))
fig.add_trace(go.Bar(
    name="Target",
    x=["Target"],
    y=[target_annual],
    marker_color="#3D4A5C"
))

fig.update_layout(
    title="Your pension overview (annual, €)",
    yaxis_title="€ per year",
    barmode="stack",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

# Monte Carlo results
st.subheader("Monte Carlo Simulation")
st.caption(f"Based on {gap_data['num_simulations']:,} simulations of investment return scenarios")

mc_col1, mc_col2, mc_col3, mc_col4 = st.columns(4)
with mc_col1:
    st.metric("Pessimistic (10th %ile)", f"€{gap_data['mc_pessimistic']:,}/yr")
with mc_col2:
    st.metric("Expected (median)", f"€{gap_data['mc_expected']:,}/yr")
with mc_col3:
    st.metric("Optimistic (90th %ile)", f"€{gap_data['mc_optimistic']:,}/yr")
with mc_col4:
    st.metric("Probability of meeting target", f"{gap_data['prob_meeting_target']}%")

# Risk classification
risk = gap_data["risk_level"]
color = gap_data["risk_color"]

if color == "green":
    st.success(f"✅ Risk assessment: **{risk}** — your pension covers {gap_data['coverage_percentage']}% of your target")
elif color == "orange":
    st.warning(f"⚠️ Risk assessment: **{risk}** — your pension covers {gap_data['coverage_percentage']}% of your target")
else:
    st.error(f"🚨 Risk assessment: **{risk}** — your pension covers {gap_data['coverage_percentage']}% of your target")
