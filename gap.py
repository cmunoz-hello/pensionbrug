def calculate_gap(aow_annual, pillar2_annual, pillar3_annual, target_annual):
    """
    Calculate the pension gap between projected income and target income.
    All amounts are annual gross figures.
    """
    
    # Total projected pension
    total_projected = aow_annual + pillar2_annual + pillar3_annual
    
    # Gap (negative means shortfall)
    gap = target_annual - total_projected
    
    # Replacement rate (what % of target will be covered)
    if target_annual > 0:
        coverage_percentage = round((total_projected / target_annual) * 100)
    else:
        coverage_percentage = 0
    
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
        "monthly_target": round(target_annual / 12)
    }
