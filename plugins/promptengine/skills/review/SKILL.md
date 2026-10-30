---
name: review
description: Review an Initiative Brief (or any written project brief, PRD draft or requirements doc) for clarity before planning. Scores it, flags missing sections, vague wording, goals without numbers, contradictions and undefined terms, and suggests concrete rewrites. Use when the user asks to check, review, lint or sanity-check a brief or requirements, or asks "is this clear enough to plan from?".
---

# Brief review

Check a brief for anything that would make Claude guess while planning, and tell the user exactly
what to change.

## 1. Get the brief

Use the file the user names, or the text they pasted. If it is not in the Initiative Brief format
(the `##` headings in `../intake/references/brief-template.md`), say so and offer to restructure it
with the intake skill first; the mechanical checks depend on those headings.

## 2. Run the mechanical checks

```bash
python3 "<this skill's directory>/scripts/lint_brief.py" path/to/brief.md
```

For pasted text, write it to a temporary file first, or pipe it in with `-` as the path.
Use `--json` if you want to process the result. If Python is not available, apply the mechanical
rules from `references/clarity-rules.md` by hand.

## 3. Add judgement

Read the brief yourself and apply the *(judgement)* rules in `references/clarity-rules.md`:
contradictions, scope that would not move the goals, generic users, untestable requirements,
missing owners, assumptions stated as fact. The script cannot see these, and they are often the
issues that matter most. Drop any script finding that is clearly a false positive (for example an
abbreviation the user's whole company uses, or "some" used harmlessly), and say you dropped it.

## 4. Report

Lead with the verdict and score, then the findings grouped by severity, one line each, worded as in
"How to word a finding" in the rules file. Keep the list to what matters: if there are more than ~12
findings, show the blocking and unclear ones and summarise the suggestions as a count.

Then offer the next step:
- **Not ready / Needs work:** offer to ask up to 5 questions to close the gaps (most important first),
  and update the brief with the answers.
- **Ready:** offer to produce the deliverable with the plan skill.

Do not rewrite the brief unless the user asks; when you do, keep their wording wherever it was clear.
