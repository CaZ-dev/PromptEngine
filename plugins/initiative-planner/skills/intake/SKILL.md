---
name: intake
description: Turn raw, unstructured notes about a new initiative, project, feature or epic into a structured Initiative Brief, then interview the user to close the gaps before any planning. Use when the user starts a new initiative and shares rough notes, a list of statements, a Slack or email thread, meeting notes or just an idea, or says they want help structuring what they want to build.
---

# Initiative intake

Raw input about a new initiative is usually a stream of statements: goals, solutions, constraints
and opinions mixed together, often vague. Planning straight from that produces a plan built on
guesses. Structure first, clarify second, plan last.

## 1. Map the raw input onto the brief

Read `references/brief-template.md`. Sort every statement the user gave you (pasted text, files they
point to) into its sections:

Title · One-line summary · Problem and why now · Goals and success metrics · Users and stakeholders ·
In scope · Out of scope · Requirements · Constraints · Existing context · Timeline and milestones ·
Risks and dependencies · Assumptions and open questions · What I want from Claude

While mapping:
- Keep the user's wording. Never invent numbers, dates, names or decisions.
- A statement describing a solution ("build a portal") goes under In scope or Requirements. If the
  problem behind it is not stated, that is a gap.
- Split compound statements into one bullet each.
- Anything you infer goes under Assumptions and open questions as `ASSUMPTION: ...`, not into the
  main sections.
- Leave a section empty rather than padding it.

## 2. Review it

Save the draft to `initiatives/<kebab-case-title>/brief.md` (create the folder; ask for a title if
there is none), then apply the review skill to it: run its `scripts/lint_brief.py` and its
judgement rules from `../review/references/clarity-rules.md`.

## 3. Show the draft and ask

Show the user, briefly:
1. The structured draft (or the path, plus the sections that were filled).
2. The verdict and the findings, grouped by severity, one line each.
3. Up to 5 questions, blocking gaps first, then the unclear points that would change the plan.
   Make each answerable in a line. Offer concrete options or an example of a good answer
   ("Which target fits: decision within 3 business days, or 5?"). Use the AskUserQuestion tool
   when it is available and a question has a small set of answers.

Always ask which deliverable they want if "What I want from Claude" is empty.

## 4. Iterate

Fold the answers into the brief, re-run the review, and ask the next round only if blocking or
plan-changing gaps remain. Two or three rounds is normally enough; do not interrogate the user about
suggestions. If they say to proceed with gaps open, record each one under Assumptions and open
questions.

## 5. Hand over

When the verdict is Ready, or the user says to proceed, tell them the brief is saved and offer to
produce the deliverable with the plan skill. Do not start planning inside this skill unless they ask.
