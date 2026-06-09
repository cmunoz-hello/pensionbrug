def calculate_aow(birth_year, years_in_nl, years_abroad):
    """
    Calculate projected AOW entitlement at retirement.
    AOW insurance runs from age 15 to retirement age (67.25).
    Maximum insurable period = 52.25 years, capped at 50 for full benefit.
    2% per year of insurance = 100% after 50 years.
    """
    
    CURRENT_YEAR = 2026
    RETIREMENT_AGE = 67.25
    AOW_START_AGE = 15
    
    current_age = CURRENT_YEAR - birth_year
    years_until_retirement = max(0, RETIREMENT_AGE - current_age)
    
    # Total possible insurable years from age 15 to retirement
    total_possible_years = RETIREMENT_AGE - AOW_START_AGE  # 52.25 years
    
    # Years already NOT insured = years abroad (uninsured gaps)
    uninsured_years = years_abroad
    
    # Total insured years by retirement
    # = total possible years - uninsured years
    total_years_insured = min(total_possible_years - uninsured_years, 50)
    total_years_insured = max(0, total_years_insured)
    
    # AOW percentage (2% per year, max 100%)
    aow_percentage = round(min(total_years_insured * 2, 100))
    
    # Full AOW amounts 2025 gross per year
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
        "retirement_age": RETIREMENT_AGE
    }
