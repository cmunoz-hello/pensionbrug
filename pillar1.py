def calculate_aow(birth_year, years_in_nl, years_abroad):
    """
    Calculate projected AOW entitlement at retirement.
    Projects forward assuming the user stays in NL until retirement.
    """
    
    # Current year
    CURRENT_YEAR = 2026
    RETIREMENT_AGE = 67.25
    
    # Years until retirement
    current_age = CURRENT_YEAR - birth_year
    years_until_retirement = max(0, RETIREMENT_AGE - current_age)
    
    # Total years insured by retirement = current years in NL + future years until retirement - years abroad
    total_years_insured = years_in_nl + years_until_retirement - years_abroad
    total_years_insured = max(0, min(total_years_insured, 50))  # cap at 50
    
    # AOW percentage (max 100%)
    aow_percentage = min(total_years_insured * 2, 100)
    
    # Full AOW amounts (2025 figures, gross per year)
    FULL_AOW_SINGLE = 19674
    FULL_AOW_COUPLE = 13435
    
    # Calculate entitlement
    aow_single = round(FULL_AOW_SINGLE * aow_percentage / 100)
    aow_couple = round(FULL_AOW_COUPLE * aow_percentage / 100)
    
    return {
        "current_age": round(current_age),
        "years_until_retirement": round(years_until_retirement),
        "total_years_insured": round(total_years_insured),
        "aow_percentage": round(aow_percentage),
        "aow_annual_single": aow_single,
        "aow_annual_couple": aow_couple,
        "aow_monthly_single": round(aow_single / 12),
        "aow_monthly_couple": round(aow_couple / 12),
        "retirement_age": RETIREMENT_AGE
    }
