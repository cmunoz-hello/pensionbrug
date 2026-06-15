
## How Claude Was Used on This Project

Claude was used **conversationally**, through the standard chat interface (claude.ai), not through Claude Code or any terminal-based agent. The workflow was: describe a feature or bug in plain language, receive complete file contents or precise edits back, paste those into the GitHub web editor, commit, pull locally, and test with `streamlit run app.py`.

We described what we saw, including pasting screenshots of the running app and error tracebacks, and Claude returned updated code. Several modules (`gap.py` in particular) went through multiple rounds of this feedback loop before the logic was correct.


## Non-Negotiable Constraints Mentioned Conversationally to Claude

1. No external AI or LLM API calls anywhere in the application. All logic is rule based or mathematical. This is an explicit project requirement, do not add OpenAI, Anthropic, or any other API client to the runtime code.
2. No database. All state is held in Streamlit `session_state` for the duration of a session.
3. UPO parsing uses Dutch field labels mandated by the Pensioenfederatie (for example "Pensioenuitvoerder", "zolang u leeft", "Pensioenleeftijd"). Do not translate or rewrite these in `pillar2.py`, the parser depends on matching the real document text.
4. AOW counts from `age_arrived_nl`, not from birth year or a fixed starting age. This is intentional and reflects how Dutch AOW insurance actually works for people who move to the Netherlands as adults.
5. Monte Carlo: only Pillar 2 varies. `mc_expected` must always equal the deterministic `aow_annual + pillar2_annual + pillar3_annual` total (see "Monte Carlo Logic" below).
6. No dash characters (hyphens used as punctuation, en dashes, or em dashes) in any user facing text: chatbot responses, UI labels, captions, warnings, or markdown. Use commas, periods, or colons instead. This applies to `app.py`, `chatbot.py`, and any other file producing text shown to the user. Code comments and section dividers (for example `# ──`) are not user facing and are fine.


