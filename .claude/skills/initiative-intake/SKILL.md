---
name: initiative-intake
description: Turn raw, unstructured notes about a new initiative or project into a structured Initiative Brief, flag what is vague or missing, ask the user targeted questions to close the gaps, and only then plan. Use when the user starts a new initiative, project, feature or epic and pastes notes, statements, a Slack thread or a rough idea, or runs /initiative-intake.
---

# Initiative intake

The user's raw input about a new initiative is usually a stream of statements: some goals, some
solutions, some constraints, mixed together and often vague. Planning straight from that produces
plans built on guesses. Your job is to structure first, clarify second, and plan last.

The canonical structure is `templates/initiative-brief.md` in this repository. Read it before you start.

## Step 1: Map the raw input onto the brief

Take everything the user gave you (pasted text, files, links they referenced) and sort each statement
into the template sections:

Title · One-line summary · Problem and why now · Goals and success metrics · Users and stakeholders ·
In scope · Out of scope · Requirements · Constraints · Existing context · Timeline and milestones ·
Risks and dependencies · Assumptions and open questions · What I want from Claude

Rules while mapping:
- Keep the user's own wording. Do not invent facts, numbers, dates or names.
- A statement that describes a solution ("build a portal") goes under In scope or Requirements, and
  the problem behind it is a gap to ask about if it is not stated.
- Split compound statements into one bullet each.
- If you infer something, put it under Assumptions and open questions as `ASSUMPTION: ...`, not in
  the main sections.

## Step 2: Review the brief for clarity

Check every section against these rules and build a gap list. Each gap gets a severity.

**Blocking** (planning would rest on a guess):
- A required section is empty: Title, One-line summary, Problem and why now, Goals and success
  metrics, Users and stakeholders, In scope, Requirements.
- Something is listed as both in scope and out of scope, or two statements contradict each other.
- The deliverable the user wants from you is unknown.

**Unclear** (Claude would fill it with its own judgement):
- A goal has no number, baseline or target.
- Vague words with no measurable meaning: better, improve, enhance, optimize, fast/faster, quick,
  easy, simple, user-friendly, intuitive, seamless, scalable, robust, efficient, modern, flexible,
  streamline, significant, some, various, several, many, etc, ASAP, soon, good, high quality,
  world-class. Quote the exact phrase and say what number or example would replace it.
- Out of scope, Constraints or Timeline is empty.
- Timeline has no date, quarter or duration.
- A technical design is requested but no tech stack is named.

**Suggestion** (cleaner input, better output):
- Requirements lack MUST / SHOULD / COULD.
- A list is written as a paragraph.
- An abbreviation is never spelled out (for example "AR", "ERP" in a company-specific sense).
- TBD / TODO / ?? left in a section instead of under open questions.

## Step 3: Show the result and ask

Show the user:
1. The structured brief so far, in the template format.
2. A short clarity verdict: **Ready**, **Needs work** or **Not ready** (any blocking gap means Not ready),
   followed by the gap list grouped by severity. One line per gap, each naming the section and what is missing.
3. Your questions. Ask about blocking gaps first, then the unclear ones that would change the plan.
   At most 5 questions per round. Make each answerable in one line, and offer concrete options or an
   example of a good answer where you can (e.g. "Which target fits: resolve disputes in 3 days, or 5 days?").
   Use the AskUserQuestion tool when it is available and the question has a small set of answers.

Do not start planning while blocking gaps remain unless the user explicitly says to proceed. If they
do, list the gaps you are planning around as `[ASSUMPTION: ...]`.

## Step 4: Save the brief

When the user has answered (or chosen to proceed), update the brief and write it to
`initiatives/<kebab-case-title>/brief.md` using the template headings exactly, so it can be re-imported
into the Brief Builder (`tool/brief-builder.html`) or reused in later sessions. Remove the template's
HTML comments.

## Step 5: Produce the deliverable

Only now produce what the user asked for under "What I want from Claude" (project plan, PRD,
technical design, task breakdown, or readiness review). If they did not say, ask which one. While writing it:
- Stay inside In scope; treat Out of scope as excluded.
- Respect every constraint. If the goals cannot be met within them, say so up front.
- Mark anything you filled in yourself as `[ASSUMPTION: ...]`.
- End with the open decisions the user still needs to make.

Save the deliverable next to the brief, e.g. `initiatives/<slug>/plan.md`.
