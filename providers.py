def get_recommendations(gap_annual, monthly_contribution_needed, years_until_retirement):
    """
    Return Pillar 3 recommendations based on gap size and required contribution.
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
    
    if gap_annual <= 0:
        message = "Your pension looks on track! You may still want to consider Pillar 3 for extra security."
        urgency = "low"
    elif gap_annual < 3000:
        message = "You have a small gap. A modest Pillar 3 contribution can close this comfortably."
        urgency = "low"
    elif gap_annual < 8000:
        message = "You have a moderate gap. Starting a Pillar 3 pension soon is recommended."
        urgency = "medium"
    else:
        message = "You have a significant gap. Starting a Pillar 3 pension is strongly recommended."
        urgency = "high"
    
    return {
        "message": message,
        "urgency": urgency,
        "monthly_contribution_needed": monthly_contribution_needed,
        "years_until_retirement": years_until_retirement,
        "providers": providers,
        "gap_annual": gap_annual
    }
