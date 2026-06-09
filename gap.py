import numpy as np

def calculate_gap(aow_annual, pillar2_annual, pillar3_annual, target_annual, birth_year):
    """
    Calculate pension gap with Monte Carlo simulation.
    Models investment uncertainty post-WTP where Pillar 2 is DC.
    """
    
    CURRENT_YEAR = 2026
    RETIREMENT_AGE = 67.25
    
    current_age = CURRENT_YEAR - birth_year
    years_until_retirement = max(1, RETIREMENT_AGE - current_age)
    
    # ── Deterministic gap ──
    total_projected = aow_annual + pillar2_annual + pillar3_annual
    gap = target_annual - total_projected
    coverage_percentage = round((total_projected / target_annual) * 100) if target_annual > 0 else 0

    # ── Monte Carlo simulation ──
    NUM_SIMULATIONS = 10000
    MEAN_RETURN = 0.05
    STD_RETURN = 0.12
    
    np.random.seed(42)
    
    annual_returns = np.random.normal(
        MEAN_RETURN,
        STD_RETURN,
        (NUM_SIMULATIONS, int(years_until_retirement))
    )
    
    growth_factors = np.prod(1 + annual_returns, axis=1)
    expected_growth = (1 + MEAN_RETURN) ** years_until_retirement
    relative_factors = growth_factors / expected_growth
    
    simulated_pillar2 = pillar2_annual * relative_factors
    simulated_totals = aow_annual + simulated_pillar2 + pillar3_annual
    
    pessimistic = round(float(np.percentile(simulated_totals, 10)))
    expected = round(float(np.percentile(simulated_totals, 50)))
    optimistic = round(float(np.percentile(simulated_totals, 90)))
    
    gap_pessimistic = max(0, target_annual - pessimistic)
    gap_expected = max(0, target_annual - expected)
    gap_optimistic = max(0, target_annual - optimistic)
    
    prob_meeting_target = round(float(np.mean(simulated_totals >= target_annual)) * 100)
    
    # ── Growth timeline ──
    # Year by year expected pension pot growth for chart
    timeline_years = list(range(CURRENT_YEAR, CURRENT_YEAR + int(years_until_retirement) + 1))
    timeline_values = []
    for yr in range(len(timeline_years)):
        value = pillar2_annual * ((1 + MEAN_RETURN) ** yr)
        timeline_values.append(round(value))
    
    # ── Monthly contribution needed to close gap ──
    monthly_needed = calculate_monthly_contribution(
        gap_annual=max(0, gap),
        years_until_retirement=years_until_retirement,
        annual_return=MEAN_RETURN
    )
    
    # ── Risk classification ──
    risk_level = classify_risk(coverage_percentage, prob_meeting_target, gap)
    
    return {
        # Basic
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
        
        # Monte Carlo
        "mc_pessimistic": pessimistic,
        "mc_expected": expected,
        "mc_optimistic": optimistic,
        "mc_gap_pessimistic": gap_pessimistic,
        "mc_gap_expected": gap_expected,
        "mc_gap_optimistic": gap_optimistic,
        "prob_meeting_target": prob_meeting_target,
        "num_simulations": NUM_SIMULATIONS,
        
        # Timeline
        "timeline_years": timeline_years,
        "timeline_values": timeline_values,
        
        # Monthly contribution
        "monthly_contribution_needed": monthly_needed,
        
        # Risk
        "risk_level": risk_level,
        "risk_color": get_risk_color(risk_level)
    }


def calculate_monthly_contribution(gap_annual, years_until_retirement, annual_return):
    """
    Calculate monthly contribution needed to close the pension gap.
    Uses future value of annuity formula:
    FV = PMT * [((1+r)^n - 1) / r]
    Solving for PMT (monthly payment)
    """
    if gap_annual <= 0 or years_until_retirement <= 0:
        return 0
    
    # We need to accumulate enough capital to generate gap_annual for ~20 years in retirement
    # Assuming 20 year retirement period and 3% drawdown rate
    RETIREMENT_YEARS = 20
    capital_needed = gap_annual * RETIREMENT_YEARS
    
    # Monthly rate
    monthly_rate = annual_return / 12
    n_months = years_until_retirement * 12
    
    if monthly_rate == 0:
        monthly_payment = capital_needed / n_months
    else:
        monthly_payment = capital_needed * monthly_rate / ((1 + monthly_rate) ** n_months - 1)
    
    return round(monthly_payment)


def classify_risk(coverage_percentage, prob_meeting_target, gap):
    if prob_meeting_target >= 70 and coverage_percentage >= 80:
        return "On Track"
    elif prob_meeting_target >= 40 and coverage_percentage >= 60:
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
