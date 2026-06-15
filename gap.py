import numpy as np


def calculate_gap(aow_annual, pillar2_annual, pillar3_annual, target_annual, birth_year):
    """
    Calculate pension gap and run a Monte Carlo simulation of the
    Pillar 2 (DC) payout under the WTP system.

    What varies and what doesn't:
    - AOW (Pillar 1)   -> FIXED. Government formula, pay-as-you-go, no investment risk.
    - Pillar 2         -> VARIES. Post-WTP this is a personal investment pot.
                          The UPO gives a projection assuming a standard (DNB-prescribed)
                          return; the real payout depends on actual market returns.
    - Pillar 3         -> FIXED for now (not yet a variable input in the MVP).

    Monte Carlo approach:
    We model the FINAL Pillar 2 payout directly as a distribution centred on
    the UPO projection, with spread that widens the further away retirement is.
    This mirrors how real Dutch pension planners present pessimistic /
    expected / optimistic scenarios.
    """

    CURRENT_YEAR = 2026
    RETIREMENT_AGE = 67.25

    current_age = CURRENT_YEAR - birth_year
    years_until_retirement = max(1, RETIREMENT_AGE - current_age)

    # ── Deterministic picture (what the UPO already tells you) ──
    total_projected = aow_annual + pillar2_annual + pillar3_annual
    gap = target_annual - total_projected
    coverage_percentage = (
        round((total_projected / target_annual) * 100) if target_annual > 0 else 0
    )

    # ── Monte Carlo: simulate the Pillar 2 payout only ──
    NUM_SIMULATIONS = 10_000

    # 8% per sqrt(year) reflects a lifecycle DC fund that de-risks as the
    # participant nears retirement (the WTP default), not a 100%-equity
    # portfolio (which would be closer to 12%).
    BASE_VOLATILITY = 0.08
    spread = min(BASE_VOLATILITY * np.sqrt(years_until_retirement) / np.sqrt(10), 0.6)

    np.random.seed(42)
    shocks = np.random.normal(loc=1.0, scale=spread, size=NUM_SIMULATIONS)
    shocks = np.clip(shocks, 0.3, 2.2)

    simulated_pillar2 = pillar2_annual * shocks
    simulated_totals = aow_annual + simulated_pillar2 + pillar3_annual

    pessimistic = round(float(np.percentile(simulated_totals, 10)))
    expected_mc = round(float(np.percentile(simulated_totals, 50)))
    optimistic = round(float(np.percentile(simulated_totals, 90)))

    prob_meeting_target = round(float(np.mean(simulated_totals >= target_annual)) * 100)

    # ── Growth timeline (illustrative, linear accrual to the UPO projection) ──
    timeline_years = list(range(CURRENT_YEAR, CURRENT_YEAR + int(years_until_retirement) + 1))
    timeline_values = [
        round(pillar2_annual * (yr / years_until_retirement))
        for yr in range(int(years_until_retirement) + 1)
    ]

    # ── Monthly Pillar 3 contribution needed to close the gap ──
    monthly_needed = calculate_monthly_contribution(
        gap_annual=max(0, gap),
        years_until_retirement=years_until_retirement,
        annual_return=0.05,
    )

    # ── Risk classification ──
    risk_level = classify_risk(coverage_percentage, prob_meeting_target)

    return {
        "aow_annual": aow_annual,
        "pillar2_annual": pillar2_annual,
        "pillar3_annual": pillar3_annual,
        "total_projected": total_projected,
        "target_annual": target_annual,
        "gap": gap,
        "has_gap": gap > 0,
        "coverage_percentage": min(coverage_percentage, 100),
        "monthly_gap": round(gap / 12),
        "monthly_projected": round(total_projected / 12),
        "monthly_target": round(target_annual / 12),
        "years_until_retirement": round(years_until_retirement),
        "current_age": round(current_age),
        "mc_pessimistic": pessimistic,
        "mc_expected": expected_mc,
        "mc_optimistic": optimistic,
        "prob_meeting_target": prob_meeting_target,
        "num_simulations": NUM_SIMULATIONS,
        "mc_spread_pct": round(spread * 100),
        "timeline_years": timeline_years,
        "timeline_values": timeline_values,
        "monthly_contribution_needed": monthly_needed,
        "risk_level": risk_level,
        "risk_color": get_risk_color(risk_level),
    }


def calculate_monthly_contribution(gap_annual, years_until_retirement, annual_return):
    if gap_annual <= 0 or years_until_retirement <= 0:
        return 0

    RETIREMENT_YEARS = 20
    capital_needed = gap_annual * RETIREMENT_YEARS

    monthly_rate = annual_return / 12
    n_months = years_until_retirement * 12

    if monthly_rate == 0:
        monthly_payment = capital_needed / n_months
    else:
        monthly_payment = capital_needed * monthly_rate / ((1 + monthly_rate) ** n_months - 1)

    return round(monthly_payment)


def classify_risk(coverage_percentage, prob_meeting_target):
    if coverage_percentage >= 90 and prob_meeting_target >= 60:
        return "On Track"
    elif coverage_percentage >= 70 and prob_meeting_target >= 35:
        return "At Risk"
    else:
        return "Critical Gap"


def get_risk_color(risk_level):
    if risk_level == "On Track":
        return "green"
    elif risk_level == "At Risk":
        return "orange"
    else:
        return "red"
