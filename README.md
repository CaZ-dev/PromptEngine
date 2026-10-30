# PromptEngine

A plugin for **Claude Code** and **Codex** that turns the way you actually ask for work ("create an API
for this and implement it in the UI", "improve the CSS of my UI", "based on this doc please build X")
into a precise, codebase-grounded task before the agent starts building.

One plugin folder serves both tools: they share the same skills, hook and scripts, and each has its
own manifest.

## Why

Short prompts leave the agent to guess the scope, the files, the data shape and what "done" means. The
guesses cause rework, hallucinated endpoints and fields, and long back-and-forth that burns tokens.
Most of those gaps don't need you at all: the codebase and your docs already answer them. PromptEngine
makes the agent look those answers up first. It then asks you only what nobody else can answer, in one
round with recommended defaults, and builds against acceptance criteria it can check.

## How it works

```
your usual prompt
  │
  ├─ hook: looks vague? ──► adds a note pointing the agent at the refine skill
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
| refine | `/promptengine:refine <request>` | Everyday build requests. Usually triggered for you by the hook or by the agent recognising a vague request. |
| profile | `/promptengine:profile` | Run once per repo. Writes a short "Project profile" (stack, commands, layout, API and UI patterns, tokens) into `CLAUDE.md` or `AGENTS.md`, so later tasks need fewer searches and questions. |
| intake | `/promptengine:intake` | A new initiative or greenfield app: raw notes → structured brief → gap questions. |
| review | `/promptengine:review` | Clarity check of a brief: score, verdict, vague wording, goals without numbers, contradictions. |
| plan | `/promptengine:plan` | From a brief: project plan, PRD, technical design, task breakdown or readiness review. |

### The hook

On every prompt, a small local script (`hooks/scripts/nudge_vague_prompt.py`, Python 3 standard
library) checks for an underspecified build request. It looks for an action word together with signals
such as a very short prompt, vague words ("improve", "better", "modern"), "this/that" with nothing
named, or "based on this doc". When it finds one, it adds a one-line note to the agent's context. It never
blocks the prompt. Slash commands, questions, short replies like "yes go ahead", and specific requests
with file paths are left alone.

- Skip it for one prompt by adding `--raw` to the prompt.
- Turn it off with the environment variable `PROMPTENGINE_NUDGE=off`.

## Install

### Claude Code

Inside Claude Code:

```
/plugin marketplace add CaZ-dev/PromptEngine
/plugin install promptengine@promptengine
```

Restart Claude Code afterwards. The repository must be readable by whoever installs it. To try a local
checkout without installing:

```bash
claude --plugin-dir ./plugins/promptengine
```

### Codex

In a terminal:

```bash
codex plugin marketplace add CaZ-dev/PromptEngine
codex plugin add promptengine@promptengine
```

Then start Codex, run `/hooks`, and approve the PromptEngine hook. Codex doesn't run a plugin's hooks
until you have reviewed them. The skills work without the hook; you just have to call `refine` yourself.
To get updates later, run `codex plugin marketplace upgrade promptengine`.

## Usage

### 1. Once per project: let it learn your codebase

```
/promptengine:profile
```

Claude reads your project and writes a short "Project profile" section into `CLAUDE.md`: your stack,
commands, where things live, your API and UI patterns, and your design tokens. Check it and fix anything
wrong. Commit it so your team shares it. Run it again when the stack changes.

### 2. Day to day: type requests the way you do now

```
create an api for invoice disputes and show it in the ui
```

1. **It notices the request is vague.** It doesn't block anything; it tells Claude to work out the
   details before building.
2. **Claude looks things up instead of guessing.** It reads the project profile, any doc you mentioned,
   and the closest similar endpoint or page in your code.
3. **It asks once, only what it can't find out**, with a recommended answer for each:
   ```
   1. Require a reason? Recommended: yes, 10–500 chars.
   2. Who can dispute? Recommended: the invoice's customer.
   ```
   Reply `defaults are fine`, or change only what you want.
4. **It shows a short spec**: which files change, a "done when" checklist, and what's out of scope.
   For big changes it waits for your OK before building.
5. **It builds, then checks each "done when" item** with your tests, type check or screenshots, and
   tells you what it couldn't check.

Small, clear requests (like "rename getUser to fetchUser in api/users.ts") skip all of this and just
get done.

**Tips**

- **Working from a doc:** include the file path or paste the doc, e.g.
  `based on docs/disputes-prd.md, build the dispute flow`.
- **UI polish:** `improve the css of the settings page`. Claude looks at the page and suggests 3 to 5
  specific fixes for you to pick from.
- **Running refine directly:** `/promptengine:refine <your request>`.
- **Skipping it for one prompt:** add `--raw` to the prompt.
- **Turning off the automatic check:** set `PROMPTENGINE_NUDGE=off` before starting Claude Code or Codex.

### 3. Big work: a greenfield app or a new initiative

| Step | Command | What happens |
| --- | --- | --- |
| Structure it | `/promptengine:intake`, then paste your notes | Claude sorts them into a brief at `initiatives/<name>/brief.md` and asks about the gaps |
| Check it | `/promptengine:review` | A score, a verdict, and what's vague or missing, with suggested fixes |
| Plan it | `/promptengine:plan` | A project plan, requirements doc, technical design, task breakdown or readiness review, saved next to the brief |

You'll usually only need `intake`, because it runs the review for you and offers the plan at the end.

### Using it in Codex

Everything above works the same in Codex, with these differences:

- **Calling a skill:** type `$` and pick it (for example `$promptengine:refine`), or run `/skills`.
  Codex also picks the right skill on its own when your request matches it.
- **Project profile:** written to `AGENTS.md`, the file Codex loads every session. If your team uses
  both Claude Code and Codex, the profile goes in `AGENTS.md`, and `CLAUDE.md` gets a line `@AGENTS.md`
  so both tools read one copy.
- **The vague-prompt hook:** only runs after you approve it in `/hooks`.

### If the commands don't show up

- **Claude Code:** restart after installing, then type `/promptengine` and the five commands should
  appear. If they still don't, run `/plugin`: check that `promptengine` is listed and enabled, and run
  the update there to get the latest version.
- **Codex:** run `codex plugin list` and check that `promptengine@promptengine` shows as
  "installed, enabled". Then start a new session and type `$promptengine` to see the skills.

## Layout

```
.claude-plugin/marketplace.json            # marketplace "promptengine" for Claude Code
.agents/plugins/marketplace.json           # the same marketplace for Codex
plugins/promptengine/
  .claude-plugin/plugin.json               # Claude Code manifest
  .codex-plugin/plugin.json                # Codex manifest
  assets/icon.png
  hooks/hooks.json, hooks/scripts/nudge_vague_prompt.py
  skills/
    refine/   SKILL.md, references/task-types.md, references/spec-template.md
    profile/  SKILL.md
    intake/   SKILL.md, references/brief-template.md
    review/   SKILL.md, references/clarity-rules.md, scripts/lint_brief.py
    plan/     SKILL.md, references/deliverables.md
```

## License

MIT. See [LICENSE](LICENSE).
