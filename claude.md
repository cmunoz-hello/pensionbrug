## How Claude Was Used on This Project

Claude was used conversationally, through the standard chat interface (claude.ai), not through Claude Code or any terminal based agent. We would describe a feature or bug in plain language, received recommendations and edits. Then we would update the GitHub files, commit, pull locally, and test with `streamlit run app.py`. We would then flag any issues in the logic, or bugs and repeat the same process.

We described what we saw, including pasting screenshots of the running app and error tracebacks, and Claude returned updated code. Several modules (`gap.py` in particular) went through multiple rounds of this feedback loop before the logic was correct. The Monte Carlo simulation was rewritten three times: first to fix a compounding bias that caused the median to diverge from the UPO projection, then to switch from a normal-with-clip to a lognormal distribution, and finally to align the percentiles with the Dutch URM standard (5th, 50th, 95th).


## Non-Negotiable Constraints Mentioned Conversationally to Claude

1. No external AI or LLM API calls anywhere in the application. All logic is rule based or mathematical.
2. No database. All state is held in Streamlit `session_state` for the duration of a session.
3. UPO parsing uses Dutch field labels mandated by the Pensioenfederatie (for example "Pensioenuitvoerder", "zolang u leeft", "Pensioenleeftijd"). Do not translate or rewrite these in `pillar2.py`, the parser depends on matching the real document text.
4. AOW counts from `age_arrived_nl`, not from birth year or a fixed starting age. This reflects how Dutch AOW insurance actually works for people who move to the Netherlands as adults.
5. Monte Carlo: only Pillar 2 varies. The lognormal distribution is centred on the UPO projection so the 50th percentile always equals the deterministic total. Percentiles follow the Dutch URM standard (5th, 50th, 95th).

