def calculate_aow(birth_year, age_arrived_nl, years_abroad):
    """
    Calculate projected AOW entitlement at retirement.
    AOW counts from when you first lived/worked in NL.
    2% per year of insurance, max 50 years = 100%.
    """
    
    CURRENT_YEAR = 2026
    RETIREMENT_AGE = 67.25
    
    current_age = CURRENT_YEAR - birth_year
    years_until_retirement = max(0, RETIREMENT_AGE - current_age)
    
    # Total years insured = from arrival age to retirement - years abroad
    total_years_insured = (RETIREMENT_AGE - age_arrived_nl) - years_abroad
    total_years_insured = max(0, min(total_years_insured, 50))
    
    # AOW percentage
    aow_percentage = round(min(total_years_insured * 2, 100))
    
    # Full AOW 2025 gross per year
    FULL_AOW_SINGLE = 19674
    FULL_AOW_COUPLE = 13435
    
    aow_single = round(FULL_AOW_SINGLE * aow_percentage / 100)
    aow_couple = round(FULL_AOW_COUPLE * aow_percentage / 100)
    
    return {
        "current_age": round(current_age),
        "years_until_retirement": round(years_until_retirement),
        "total_years_insured": round(total_years_insured),
        "aow_percentage": aow_percentage,
        "aow_annual_single": aow_single,
        "aow_annual_couple": aow_couple,
        "aow_monthly_single": round(aow_single / 12),
        "aow_monthly_couple": round(aow_couple / 12),
        "retirement_age": RETIREMENT_AGE,
        "age_arrived_nl": age_arrived_nl
    }
