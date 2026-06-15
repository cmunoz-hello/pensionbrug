def get_response(user_input, pension_data=None):
    """
    Rule-based chatbot for pension questions.
    pension_data is optionally passed in to give personalised answers.
    """

    user_input = user_input.lower().strip()

    # Personalised responses if we have the user's data
    if pension_data:
        gap = pension_data.get("gap", 0)
        total = pension_data.get("total_projected", 0)
        coverage = pension_data.get("coverage_percentage", 0)

    # WTP questions
    if any(word in user_input for word in ["wtp", "wet toekomst", "pension reform", "reform"]):
        return """The WTP (Wet toekomst pensioenen) is the Dutch pension reform that came into effect in July 2023.

All pension funds must comply by January 2028. The key change is that your Pillar 2 pension moves from a **defined benefit** (a guaranteed fixed payout) to a **defined contribution** (a personal investment pot).

This means your pension now depends on investment returns. It can go up or down with the markets. The good news is that younger workers benefit more, as their pot is invested more aggressively over a longer horizon."""

    if any(word in user_input for word in ["defined benefit", "defined contribution", "db", "dc"]):
        return """**Defined Benefit (old system):** Your pension fund promised you a fixed monthly payout at retirement. The fund carried all investment risk.

**Defined Contribution (new system):** Your contributions are invested in a personal pot. The final amount depends on how those investments perform. You carry the investment risk, but you also benefit if markets do well."""

    # AOW questions
    if any(word in user_input for word in ["aow", "state pension", "pillar 1", "first pillar"]):
        return """The AOW is the Dutch state pension, also known as Pillar 1. It is automatically accrued by anyone living or working in the Netherlands.

You build up 2% per year of Dutch insurance, meaning 50 years gives a full benefit. The full AOW is approximately €19,674 per year for a single person (2025 figures).

Important: every year spent abroad without voluntary AOW insurance reduces your entitlement by 2%. This is especially relevant for expats and mobile workers."""

    # Gap questions
    if any(word in user_input for word in ["gap", "shortfall", "enough", "sufficient", "on track"]):
        if pension_data and gap > 0:
            return f"""Based on your inputs, you have a pension gap of €{gap:,} per year (€{gap//12:,} per month).

This means your projected pension covers {coverage}% of your target retirement income.

The most effective way to close this gap is through Pillar 3, voluntary individual pension products with tax benefits. See the recommendations below."""
        else:
            return """A pension gap is the difference between your projected retirement income and your target income.

If your projected pension is lower than what you need, you have a gap. This is common for people who:

* Worked abroad for several years
* Changed jobs frequently
* Worked part time for extended periods
* Are self employed

Pillar 3 products can help fill this gap with tax advantaged contributions."""

    # Pillar questions
    if any(word in user_input for word in ["pillar 2", "second pillar", "employer pension", "upo"]):
        return """Pillar 2 is your employer pension, the most significant part of most Dutch workers' retirement income.

Your employer selects a pension fund, and both you and your employer contribute monthly. The money is pooled and invested collectively.

The UPO (Uniform Pensioenoverzicht) is the standardised annual statement every fund must issue. It shows your accrued pension to date and your projected pension at retirement."""

    if any(word in user_input for word in ["pillar 3", "third pillar", "individual pension", "annuity"]):
        return """Pillar 3 is voluntary individual pension savings, typically used to supplement Pillar 1 and 2.

Products include investment pensions, annuities, and pension savings accounts. Contributions are often tax deductible, making them an efficient way to save.

Pillar 3 is especially relevant for:

* Freelancers and self employed workers who have no Pillar 2
* Workers with gaps in their Pillar 2 accrual
* Anyone who wants to retire earlier than the AOW age"""

    # Expat questions
    if any(word in user_input for word in ["expat", "abroad", "foreign", "international", "mobile worker"]):
        return """If you have lived or worked outside the Netherlands, your pension situation may be more complex.

For AOW (Pillar 1): every year abroad without voluntary insurance reduces your entitlement by 2%. You can check your insurance history at mijnsvb.nl.

For Pillar 2: pension rights accrued with Dutch employers stay in Dutch funds. A transfer (waardeoverdracht) to a new fund is possible but must be requested manually within a time limit.

For cross border workers: the European Tracking Service (ETS) at findyourpension.eu helps track pension rights across EU countries."""

    # Retirement age
    if any(word in user_input for word in ["retirement age", "when can i retire", "67", "pension age"]):
        return """The current Dutch retirement age is 67 years and 3 months (2025). It is linked to life expectancy and may rise further in coming years.

You can retire earlier, but you will need to fund the gap yourself until your AOW starts. Early retirement is possible through Pillar 2 or 3 arrangements, but at a reduced amount."""

    # Hello / greeting
    if any(word in user_input for word in ["hello", "hi", "hey", "hallo", "hoi"]):
        return """Hi! I'm the PensionBrug assistant. I can help you understand:

* Your pension gap and what it means
* The WTP pension reform and how it affects you
* The three pension pillars
* Pillar 3 options to supplement your pension

What would you like to know?"""

    # Default response
    return """I'm not sure I understand that question. You can ask me about:

* The WTP pension reform
* Your pension gap
* AOW (Pillar 1)
* Employer pension (Pillar 2)
* Individual pension products (Pillar 3)
* Retiring as an expat or mobile worker"""
