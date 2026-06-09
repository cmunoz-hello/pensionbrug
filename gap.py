import numpy as np

def calculate_gap(aow_annual, pillar2_annual, pillar3_annual, target_annual, birth_year):
    """
    Calculate pension gap with Monte Carlo simulation.
    Monte Carlo models uncertainty in the final Pillar 2 payout
    by simulating varying investment returns over the accumulation period.
    """
    
    CURRENT_YEAR = 2026
    RETIREMENT_AGE = 67.25
    MEAN_RETURN = 0.05
    STD_RETURN = 0.12
    NUM_SIMULATIONS = 10000
    
    current_age = CURRENT_YEAR - birth_year
    years_until_retirement = max(1, RETIREMENT_AGE - current_age)
    
    # ── Deterministic gap ──
    total_projected = aow_annual + pillar2_annual + pillar3_annual
    gap = target_annual - total_projected
    coverage_percentage = round((total_projected / target_annual) * 100) if target_annual > 0 else 0

    # ── Monte Carlo simulation ──
    # Models how the Pillar 2 PAYOUT might vary depending on investment returns
    # We apply a return variability factor directly to the projected payout
    # This reflects that the UPO projection assumes a fixed return;
    # actual returns will be higher or lower
    
    np.random.seed(42)
    
    # Simulate annual return deviation from expected over accumulation period
    annual_returns = np.random.normal(
        MEAN_RETURN,
        STD_RETURN,
        (NUM_SIMULATIONS, int(years_until_retirement))
    )
    
    # Compound the deviation relative to expected
    actual_growth = np.prod(1 + annual_returns, axis=1)
    expected_growth = (1 + MEAN_RETURN) ** years_until_retirement
    
    # Ratio of actual to expected — applied as a scaling factor to Pillar 2
    scaling_factors = actual_growth / expected_growth
    
    # Keep scaling factors reasonable — cap between 0.3 and 2.5
    scaling_factors = np.clip(scaling_factors, 0.3, 2.5)
    
    # Simulated Pillar 2 payouts
    simulated_pillar2 = pillar2_annual * scaling_factors
    
    # Total pension in each simulation
    simulated_totals = aow_annual + simulated_pillar2 + pillar3_annual
    
    # Percentile outcomes
    pessimistic = round(float(np.percentile(simulated_totals, 10)))
    expected_mc  = round(float(np.percentile(simulated_totals, 50)))
    optimistic   = round(float(np.percentile(simulated_totals, 90)))
    
    # Probability of meeting target
    prob_meeting_target = round(float(np.mean(simulated_totals >= target_annual)) * 100)
    
    # ── Growth timeline ──
    # Shows how the Pillar 2 projected payout grows year by year
    # as more contributions are made and invested
    timeline_years = list(range(CURRENT_YEAR, CURRENT_YEAR + int(years_until_retirement) + 1))
    
    # Assume linear accrual — at retirement they get full pillar2_annual
    # Scale from current accrued (small) to projected (full) linearly
    timeline_values = [
        round(pillar2_annual * (yr / years_until_retirement))
        for yr in range(int(years_until_retirement) + 1)
    ]
    
    # ── Monthly contribution needed ──
    monthly_needed = calculate_monthly_contribution(
        gap_annual=max(0, gap),
        years_until_retirement=years_until_retirement,
        annual_return=MEAN_RETURN
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
        "timeline_years": timeline_years,
        "timeline_values": timeline_values,
        "monthly_contribution_needed": monthly_needed,
        "risk_level": risk_level,
        "risk_color": get_risk_color(risk_level)
    }


def calculate_monthly_contribution(gap_annual, years_until_retirement, annual_return):
    """
    Monthly contribution needed to generate enough capital to fill the gap.
    Uses future value of annuity formula.
    Assumes 20 year retirement drawdown period.
    """
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
    """
    Classify pension risk based on coverage and probability of meeting target.
    """
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
