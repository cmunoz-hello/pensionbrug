# PensionBrug

RSM Fintech Business Models & Applications, 2026
Amalia Nimeskern & Camila Munoz

## What is PensionBrug?

PensionBrug is a pension aggregation MVP that brings together all three pillars of the Dutch pension system into a single personalised dashboard. It detects retirement income gaps, runs a Monte Carlo simulation of the Pillar 2 pot under the WTP contribution system, and recommends Pillar 3 products to close any gap.

The product follows the same strategic logic as Tink before PSD2: building the aggregation layer and the user trust ahead of the regulatory mandate (FiDA) that will eventually require pension funds to open their data.

## Features

* **Pillar 1, AOW**: computed from user inputs (age arrived in the Netherlands, years spent abroad), based on the official 2% per insured year formula.
* **Pillar 2, Employer Pension**: UPO PDF upload with automatic parsing.
* **Gap Detection**: compares the total projected pension against your chosen retirement income target.
* **Monte Carlo Simulation**: 10,000 simulations of the Pillar 2 payout, reflecting the investment uncertainty introduced by the WTP shift from defined benefit to defined contribution.
* **Risk Classification**: On Track, At Risk, or Critical Gap, based on coverage percentage and probability of meeting target.
* **Pillar 3 Recommendations**: estimates the monthly contribution needed to close the gap and shows matching providers.
* **Pension Chatbot**: rule based question and answer assistant covering AOW, WTP, Pillar 2 and 3, gaps, and expat specific topics. No external AI API is used.

## Architecture

```
pensionbrug/
  app.py                Streamlit UI, main application and styling
  pillar1.py            AOW calculation logic
  pillar2.py            UPO PDF parsing (pdfplumber and regex)
  gap.py                Gap detection and Monte Carlo simulation (numpy)
  providers.py          Pillar 3 recommendation logic
  chatbot.py            Rule based pension question and answer assistant
  create_sample_upo.py  Generates a sample UPO PDF for testing
  assets/logo.png        PensionBrug logo, shown in the header and sidebar
  requirements.txt      Python dependencies
  CLAUDE.md              AI agent instructions
```

### Architecture

* Each pillar has its own module (`pillar1.py`, `pillar2.py`, and the Pillar 3 logic in `providers.py`) that normalises pension data from a different source into a common annual euro figure.
* `gap.py` is the intelligence layer. It takes the three normalised figures and the user's target, and produces a gap, a risk classification, and a Monte Carlo range. 
* `app.py` is the user facing layer, structured as a six step guided flow (About You, Employer Pension, Retirement Goal, Your Pension Picture, Close the Gap, Ask PensionBrug), so the UX mirrors the conceptual journey from raw pension data to a personalised plan.

---

## How to Run Locally

**Prerequisites:** Python 3.10 or later, pip

```bash
git clone https://github.com/cmunoz-hello/pensionbrug.git
cd pensionbrug
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## How to Generate a Sample UPO

```bash
python3 create_sample_upo.py
```

This creates `sample_upo.pdf`, a realistic Dutch pension statement in the standardised UPO format, which you can upload in Step 2 to test the parsing.

---

## Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| Styling | Custom CSS, Google Fonts (Poppins) |
| PDF parsing | pdfplumber and regex |
| Gap analysis and Monte Carlo | numpy |
| Charts | Plotly |
| Sample data generation | reportlab |
| AI coding agent | Claude (Anthropic) |

---
