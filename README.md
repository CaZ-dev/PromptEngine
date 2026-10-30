# PromptEngine

A Claude Code plugin marketplace for giving Claude structured, unambiguous input.

## initiative-planner

When you start a new initiative, the input you give Claude is usually a stream of statements: goals
mixed with solutions, "make it faster", no scope edges, no dates. Claude fills the gaps with its own
guesses and the plan drifts from what you meant. This plugin puts a structured brief between your
notes and the plan, and tells you what is unclear before planning starts.

| Skill | Command | What it does |
| --- | --- | --- |
| intake | `/initiative-planner:intake` | Paste raw notes. Claude sorts them into the brief format, saves `initiatives/<name>/brief.md`, shows what is missing or vague, and asks you up to 5 questions per round. |
| review | `/initiative-planner:review` | Checks any brief: clarity score, verdict, and findings such as goals without numbers, vague words ("faster", "user-friendly", "ASAP"), empty scope edges, contradictions, undefined abbreviations, each with a suggested rewrite. |
| plan | `/initiative-planner:plan` | Produces a project plan, PRD, technical design, task breakdown or readiness review from the brief. It stays inside scope and constraints, labels assumptions, and ends with the decisions you need to make. |

Claude also picks these skills up on its own when you describe a new initiative, ask whether a brief is
clear enough, or ask for a plan from one.

### The brief format

Fourteen sections in four parts (full template with guidance:
[`brief-template.md`](plugins/initiative-planner/skills/intake/references/brief-template.md)):

1. **Why**: title, one-line summary, problem and why now, goals with a baseline and target.
2. **Who and what**: users and stakeholders, in scope, out of scope, requirements (MUST / SHOULD / COULD).
3. **Reality**: constraints, existing context, timeline, risks and dependencies, assumptions and open questions.
4. **The ask**: which deliverable you want, for whom, in what format.

The review skill runs [`lint_brief.py`](plugins/initiative-planner/skills/review/scripts/lint_brief.py)
(Python 3, standard library only) for the mechanical checks and applies
[judgement rules](plugins/initiative-planner/skills/review/references/clarity-rules.md) on top. You can
also run the script yourself:

```bash
python3 plugins/initiative-planner/skills/review/scripts/lint_brief.py initiatives/my-initiative/brief.md
```

## Install

From GitHub, inside Claude Code:

```
/plugin marketplace add CaZ-dev/PromptEngine
/plugin install initiative-planner@promptengine
```

The repository must be readable by whoever installs it; make it public to publish more widely.

To try a local checkout without installing:

```bash
claude --plugin-dir ./plugins/initiative-planner
```

## Layout

```
.claude-plugin/marketplace.json          # marketplace "promptengine"
plugins/initiative-planner/
  .claude-plugin/plugin.json
  skills/
    intake/   SKILL.md, references/brief-template.md
    review/   SKILL.md, references/clarity-rules.md, scripts/lint_brief.py
    plan/     SKILL.md, references/deliverables.md
```

Add more plugins under `plugins/` and list them in `marketplace.json`.
