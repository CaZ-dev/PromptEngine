# PromptEngine

A Claude Code plugin that turns the way you actually ask for work ("create an API for this and
implement it in the UI", "improve the CSS of my UI", "based on this doc please build X") into a precise,
codebase-grounded task before Claude starts building.

## Why

Short prompts leave Claude to guess the scope, the files, the data shape and what "done" means. The
guesses cause rework, hallucinated endpoints and fields, and long back-and-forth that burns tokens.
Most of those gaps don't need you at all: the codebase and your docs already answer them. PromptEngine
makes Claude look those answers up first. It then asks you only what nobody else can answer, in one
round with recommended defaults, and builds against acceptance criteria it can check.

## How it works

```
your usual prompt
  │
  ├─ hook: looks vague? ──► adds a note pointing Claude at the refine skill
  │
  ▼
refine
  1. classify     API + UI · UI/design · doc-driven · bug · refactor
  2. ground       project profile → referenced docs → closest similar code
  3. ask once     ≤ 4 questions, each with a recommended answer (skipped if none needed)
  4. spec         goal · files per layer · "done when" · out of scope · assumptions
  5. build        in the codebase's own patterns and design tokens
  6. verify       tests / typecheck / screenshots against each "done when"
```

Clear, small requests skip straight to building. Greenfield apps and multi-week work go to the
initiative skills instead.

## Skills

| Skill | Command | Use it for |
| --- | --- | --- |
| refine | `/promptengine:refine <request>` | Everyday build requests. Usually triggered for you by the hook or by Claude recognising a vague request. |
| profile | `/promptengine:profile` | Run once per repo. Writes a short "Project profile" (stack, commands, layout, API and UI patterns, tokens) into `CLAUDE.md`, so later tasks need fewer searches and questions. |
| intake | `/promptengine:intake` | A new initiative or greenfield app: raw notes → structured brief → gap questions. |
| review | `/promptengine:review` | Clarity check of a brief: score, verdict, vague wording, goals without numbers, contradictions. |
| plan | `/promptengine:plan` | From a brief: project plan, PRD, technical design, task breakdown or readiness review. |

### The hook

On every prompt, a small local script (`hooks/scripts/nudge_vague_prompt.py`, Python 3 standard
library) checks for an underspecified build request. It looks for an action word together with signals
such as a very short prompt, vague words ("improve", "better", "modern"), "this/that" with nothing
named, or "based on this doc". When it finds one, it adds a one-line note to Claude's context. It never
blocks the prompt. Slash commands, questions, short replies like "yes go ahead", and specific requests
with file paths are left alone.

- Skip it for one prompt by adding `--raw` to the prompt.
- Turn it off with the environment variable `PROMPTENGINE_NUDGE=off`.

## Typical use

```
> /promptengine:profile                        # once per repo
> create an api for invoice disputes and show it in the ui
  … Claude reads the profile, finds the closest route and page, then asks:
  1. Require a reason? Recommended: yes, 10–500 chars.
  2. Who may dispute? Recommended: the invoice's customer (same guard as GET /invoices/:id).
> defaults are fine
  … spec with files and "done when", then build, then test results per criterion
```

## Install

Inside Claude Code:

```
/plugin marketplace add CaZ-dev/PromptEngine
/plugin install promptengine@promptengine
```

The repository must be readable by whoever installs it. To try a local checkout without installing:

```bash
claude --plugin-dir ./plugins/promptengine
```

## Layout

```
.claude-plugin/marketplace.json            # marketplace "promptengine"
plugins/promptengine/
  .claude-plugin/plugin.json
  hooks/hooks.json, hooks/scripts/nudge_vague_prompt.py
  skills/
    refine/   SKILL.md, references/task-types.md, references/spec-template.md
    profile/  SKILL.md
    intake/   SKILL.md, references/brief-template.md
    review/   SKILL.md, references/clarity-rules.md, scripts/lint_brief.py
    plan/     SKILL.md, references/deliverables.md
```
