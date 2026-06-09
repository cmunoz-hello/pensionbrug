import numpy as np

def calculate_gap(aow_annual, pillar2_annual, pillar3_annual, target_annual):
    """
    Calculate pension gap with Monte Carlo simulation.
    Models investment uncertainty post-WTP where Pillar 2 is DC.
    """
    
    # ── Deterministic gap (simple) ──
    total_projected = aow_annual + pillar2_annual + pillar3_annual
    gap = target_annual - total_projected
    coverage_percentage = round((total_projected / target_annual) * 100) if target_annual > 0 else 0

    # ── Monte Carlo simulation ──
    # Models uncertainty in DC pension returns post-WTP
    # AOW and Pillar 3 are treated as fixed; Pillar 2 varies with market returns
    
    NUM_SIMULATIONS = 10000
    
    # Annual return assumptions for DC pension investments
    MEAN_RETURN = 0.05      # 5% expected annual return
    STD_RETURN = 0.12       # 12% standard deviation (market volatility)
    YEARS_TO_RETIREMENT = 30  # assumed investment horizon
    
    # Simulate Pillar 2 outcomes
    # Each simulation: compound a random annual return over the investment horizon
    np.random.seed(42)  # reproducible results
    
    annual_returns = np.random.normal(
        MEAN_RETURN, 
        STD_RETURN, 
        (NUM_SIMULATIONS, YEARS_TO_RETIREMENT)
    )
    
    # Compound returns over investment horizon
    # pillar2_annual is the current projected value — we simulate how it might vary
    growth_factors = np.prod(1 + annual_returns, axis=1)
    
    # Normalize: express as ratio relative to expected growth
    expected_growth = (1 + MEAN_RETURN) ** YEARS_TO_RETIREMENT
    relative_factors = growth_factors / expected_growth
    
    # Apply to pillar 2 projected pension
    simulated_pillar2 = pillar2_annual * relative_factors
    
    # Total pension in each simulation
    simulated_totals = aow_annual + simulated_pillar2 + pillar3_annual
    
    # Scenario outcomes
    pessimistic = round(float(np.percentile(simulated_totals, 10)))   # worst 10%
    expected = round(float(np.percentile(simulated_totals, 50)))       # median
    optimistic = round(float(np.percentile(simulated_totals, 90)))     # best 10%
    
    # Gap in each scenario
    gap_pessimistic = max(0, target_annual - pessimistic)
    gap_expected = max(0, target_annual - expected)
    gap_optimistic = max(0, target_annual - optimistic)
    
    # Probability of meeting target
    prob_meeting_target = round(float(np.mean(simulated_totals >= target_annual)) * 100)
    
    # Risk classification for the classifier
    risk_level = classify_risk(
        coverage_percentage=coverage_percentage,
        prob_meeting_target=prob_meeting_target,
        gap=gap
    )
    
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
        
        # Monte Carlo results
        "mc_pessimistic": pessimistic,
        "mc_expected": expected,
        "mc_optimistic": optimistic,
        "mc_gap_pessimistic": gap_pessimistic,
        "mc_gap_expected": gap_expected,
        "mc_gap_optimistic": gap_optimistic,
        "prob_meeting_target": prob_meeting_target,
        "num_simulations": NUM_SIMULATIONS,
        
        # Risk classification
        "risk_level": risk_level,
        "risk_color": get_risk_color(risk_level)
    }


def classify_risk(coverage_percentage, prob_meeting_target, gap):
    """
    Simple rule-based classifier that categorises pension risk.
    Maps multiple features to a risk category.
    """
    
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
