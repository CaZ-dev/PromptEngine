# Clarity rules

Use these when reviewing an Initiative Brief. `scripts/lint_brief.py` checks the mechanical ones;
the rules marked *(judgement)* need you to read the brief.

## Severities

| Severity | Meaning | Effect |
| --- | --- | --- |
| Blocking | Planning would rest on a guess | Do not plan until fixed, unless the user says to proceed |
| Unclear | Claude would fill it with its own judgement | Ask about it if it would change the plan |
| Suggestion | Cleaner input, better output | Mention it; do not hold up planning |

Verdict: any blocking issue means **Not ready**. Otherwise score 80+ is **Ready**, below is **Needs work**.
Score starts at 100 and loses 12 per blocking, 5 per unclear and 2 per suggestion issue.

## Blocking

- A required section is empty: Title, One-line summary, Problem and why now, Goals and success metrics,
  Users and stakeholders, In scope, Requirements, What I want from Claude.
- The deliverable is not named (project plan, PRD, technical design, task breakdown, readiness review).
- The same item is both in scope and out of scope.
- *(judgement)* Two statements contradict each other, e.g. a 4-week deadline and a requirement to
  replace the billing system, or a goal that an out-of-scope item would be needed to reach.
- *(judgement)* The problem and the in-scope work do not connect: delivering the scope would not
  plausibly move the stated goals.

## Unclear

- A goal has no number. Each goal needs a metric, a baseline and a target.
- Vague words with no measurable meaning: better, improve, enhance, optimize, fast/faster, quick,
  easy, simple, user-friendly, intuitive, seamless, scalable, robust, efficient, modern, flexible,
  streamline, leverage, significant, some, various, several, many, etc, stuff, things, ASAP, soon,
  good, nice, high quality, best-in-class, world-class.
- Out of scope, Constraints or Timeline is empty.
- The timeline has no date, quarter or duration.
- A required section is too thin to act on.
- A technical design is requested and no tech stack is named.
- *(judgement)* Users are described generically ("users", "customers", "the team") where the plan
  depends on which users.
- *(judgement)* A requirement cannot be tested: nobody could say whether it passed.
- *(judgement)* An owner or approver is missing for a decision the plan depends on.

## Suggestion

- Requirements lack MUST / SHOULD / COULD.
- A list is written as a paragraph.
- An abbreviation is never spelled out.
- TBD / TODO / ?? left outside Assumptions and open questions.
- The problem section starts with a solution ("Build a portal…") instead of the pain.
- *(judgement)* An assumption is stated as fact in the main sections; move it to Assumptions.

## How to word a finding

One line each: the section, what is wrong, and what a good answer looks like. Quote the user's words.

- Weak: "Goals could be more specific."
- Strong: "Goals: 'Make the process faster for customers' has no number. Something like 'customers
  get a decision within 3 business days (today: 9)' would let the plan size the work."
