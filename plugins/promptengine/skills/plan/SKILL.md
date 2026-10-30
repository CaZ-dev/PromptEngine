---
name: plan
description: Produce a project plan, PRD, technical design, task breakdown or readiness review from an Initiative Brief, staying inside its scope and constraints and labelling every assumption. Use when the user has a brief (for example initiatives/<name>/brief.md) and asks for a plan, roadmap, PRD, design, task list or estimate for that initiative.
---

# Plan from a brief

## 1. Load and check the brief

Find the brief: the path the user gives, or `initiatives/*/brief.md` (ask which one if there are
several). If there is no brief, offer the intake skill first. If the user declines, work from what
they gave you and say the output rests on unreviewed input.

Run the review skill's checks (`../review/scripts/lint_brief.py` plus its judgement rules). If the
verdict is **Not ready**, show the blocking issues and ask whether to resolve them first or proceed
with them as assumptions. Do not silently plan past a blocking gap.

## 2. Pick the deliverable

Use the deliverable named under "What I want from Claude". If none is named, ask: project plan, PRD,
technical design, task breakdown or readiness review. Follow its outline in
`references/deliverables.md`, plus any format, audience or length the brief asks for.

## 3. Write it

- **Stay in scope.** Only plan what is In scope. If something out of scope is needed to reach a goal,
  say so as a finding; do not add it.
- **Respect constraints.** Size the work against the team, budget, stack and dates in Constraints and
  Timeline. If the goals do not fit, say so at the top, with the options (cut scope, move the date,
  add people) rather than a plan that quietly assumes more.
- **Trace to goals.** Every phase, epic or major component should serve a stated goal; name which.
- **Label assumptions.** Anything not stated in the brief gets `[ASSUMPTION: ...]` inline.
- **Use the user's terms.** Reuse names of teams, systems and roles exactly as the brief has them.
- **End with open decisions.** What the user must decide, by when, and the default if they do not.

## 4. Save

Write the result next to the brief, e.g. `initiatives/<slug>/plan.md`, `prd.md`, `design.md`,
`tasks.md` or `readiness.md`, and give the user the path with a short summary: the shape of the plan,
the biggest risk, and the decisions waiting on them.
