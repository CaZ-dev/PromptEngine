---
name: profile
description: Build or refresh a compact "Project profile" section in the repository's CLAUDE.md (stack, commands, folder layout, API and UI conventions, design tokens, testing) so later requests need less exploration and fewer questions. Use when the user sets up PromptEngine in a repo, asks Claude to "learn" or "remember" the project, or when the refine skill finds no profile in a repo the user works in often.
---

# Project profile

Claude Code loads `CLAUDE.md` into every session. A short, accurate profile there answers most of the
questions the refine skill would otherwise spend searches or user questions on. Build it once, then
refresh it when the stack changes.

## What to find

Look, don't guess. Each item comes from a file you actually read: manifests, config, a representative
example. Skip items that do not apply.

- **Stack:** languages, frameworks, versions that matter (from `package.json`, `pyproject.toml`, `go.mod`, etc.).
- **Commands:** install, dev server, test, lint, type check, build, migrations (from scripts, Makefile, CI config).
- **Layout:** where API routes, data models, UI pages, components, styles and tests live (folders only).
- **API conventions:** routing style, validation library, error format, auth middleware. Name one
  representative file to copy from.
- **UI conventions:** component library, styling approach (CSS modules, Tailwind, styled-components),
  where design tokens or the theme are defined, data-fetching pattern. Name one representative component.
- **Testing:** frameworks, where tests live, how to run one file.
- **Gotchas:** anything a newcomer would trip on (generated files not to edit, required env vars by name only).

Never copy secrets or the values of environment variables into the profile.

## Write it

Add or replace a section in the root `CLAUDE.md` (create the file if it does not exist), keeping
everything else in that file unchanged:

```markdown
## Project profile
<!-- Maintained by the promptengine profile skill. Refresh with /promptengine:profile. -->

**Stack:** …
**Commands:** install `…` · dev `…` · test `…` · lint `…` · typecheck `…` · build `…`
**Layout:** API `…` · models `…` · pages `…` · components `…` · styles `…` · tests `…`
**API pattern:** … (copy `path/to/example`)
**UI pattern:** … tokens in `…` (copy `path/to/example`)
**Testing:** …
**Gotchas:** …
```

Keep it under about 25 lines. It is loaded into every session, so every line costs tokens. Prefer
paths and names over prose.

Show the user the section you wrote and point out anything you were unsure about. Do not commit
unless asked.
