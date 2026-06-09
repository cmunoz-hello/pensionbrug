def get_recommendations(gap_annual):
    """
    Return Pillar 3 provider recommendations based on gap size.
    """
    
    providers = [
        {
            "name": "Brand New Day",
            "type": "Investment pension",
            "description": "Low-cost pension investing with flexible monthly contributions. Good for younger workers with a longer investment horizon.",
            "url": "https://www.brandnewday.nl",
            "min_monthly": 25,
            "best_for": "Young professionals, career changers"
        },
        {
            "name": "BrightPensioen",
            "type": "Sustainable investment pension",
            "description": "Sustainable pension investing with transparent costs. Fully digital and easy to manage.",
            "url": "https://www.brightpensioen.nl",
            "min_monthly": 10,
            "best_for": "Freelancers, expats, mobile workers"
        },
        {
            "name": "Centraal Beheer",
            "type": "Annuity / pension savings",
            "description": "Traditional pension savings with guaranteed returns option. Good for those closer to retirement who want more certainty.",
            "url": "https://www.centraalbeheer.nl",
            "min_monthly": 50,
            "best_for": "Workers aged 45+, risk-averse savers"
        }
    ]
    
    # Monthly contribution needed to close gap
    # Assuming 30 year investment horizon and 5% average return
    if gap_annual > 0:
        monthly_needed = round(gap_annual / 12 * 0.6)
    else:
        monthly_needed = 0
    
    # Filter recommendations based on gap size
    if gap_annual <= 0:
        message = "Your pension looks on track! You may still want to consider Pillar 3 for extra security."
        recommended = providers  # show all anyway
    elif gap_annual < 3000:
        message = f"You have a small gap of €{gap_annual:,} per year. A small monthly Pillar 3 contribution could close this."
        recommended = [p for p in providers if p["min_monthly"] <= 25]
    elif gap_annual < 8000:
        message = f"You have a moderate gap of €{gap_annual:,} per year. We recommend starting a Pillar 3 pension soon."
        recommended = providers
    else:
        message = f"You have a significant gap of €{gap_annual:,} per year. Starting a Pillar 3 pension is strongly recommended."
        recommended = providers
    
    return {
        "message": message,
        "monthly_needed": monthly_needed,
        "providers": recommended,
        "gap_annual": gap_annual
    }
