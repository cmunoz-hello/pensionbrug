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
    
    # Apply to pillar 2 pr
