# Task types and what must be known

For each type: what must be known before building, and where the answer usually comes from.
**Code** means answerable from the repository, **Doc** from a document the user referenced, and **User**
only from the user. Default to looking it up; ask only for items that stay Unknown.

## API + UI feature
"Create an API for this and implement it in the UI."

| Must know | Usually from |
| --- | --- |
| The resource or action: what entity, what operation | Doc, User |
| Endpoint shape: method, path, request and response fields | Code (existing routes), Doc |
| Validation rules and error responses | Doc, Code (existing validators), Default |
| Persistence: which table or store, schema change needed? | Code |
| Auth: who may call it | Code (existing middleware), User if new |
| Where it appears in the UI: page, component, entry point | User, Doc |
| UI states: loading, empty, error, success | Default (copy existing pattern) |
| How the UI calls the API: existing client, data-fetching library | Code |
| Tests expected: API, UI, both | Code (existing test setup) |

Acceptance criteria to propose: the endpoint returns the documented shape; invalid input returns the
documented error; the UI shows each state; tests pass.

## UI or design improvement
"Improve the CSS and design of my UI."

| Must know | Usually from |
| --- | --- |
| Which screens or components | User (ask if "my UI" is the whole app) |
| What is wrong today: spacing, hierarchy, consistency, responsiveness, accessibility, looks dated | User; or look at it and propose |
| The design system: tokens, theme file, component library, CSS approach | Code |
| A reference for the target look: brand guide, Figma, site they like | User, Doc |
| Constraints: what must not change (layout, copy, behaviour) | User, Default (behaviour and copy unchanged) |
| Breakpoints and dark mode support | Code |
| How "done" is judged | Default: before and after screenshots at desktop and mobile widths |

When the user cannot say what is wrong, look at the UI first (run it and take screenshots, or read the
components) and propose 3–5 specific problems with fixes ("buttons use 4 different paddings; standardise
on the `--space-3` token"). Ask them to pick, rather than asking them to describe the problem.

## Doc-driven feature
"Based on this doc, please do X."

| Must know | Usually from |
| --- | --- |
| Every requirement in the doc, as a numbered list with section references | Doc |
| Which requirements are in this task and which are later | User (propose a split if the doc is large) |
| Conflicts between the doc and the current code | Code + Doc |
| Ambiguities and gaps in the doc | Doc (flag them; ask only the ones that change the build) |
| Terms the doc uses that map to code names | Code |

Quote the doc in the spec so every change traces back to a requirement. Never fill a gap in the doc
silently. Either ask, or mark it as an assumption.

## Bug fix
"The dashboard is broken."

| Must know | Usually from |
| --- | --- |
| Steps to reproduce | User, or reproduce it yourself |
| Expected and actual behaviour | User |
| Error messages, logs, environment | User, Code (run it) |
| When it started; recent changes | git log |

Reproduce before fixing. Add a test that fails without the fix where the codebase has tests.

## Refactor
"Clean up this module."

| Must know | Usually from |
| --- | --- |
| The goal: readability, performance, testability, removing duplication | User |
| Boundaries: which files, which public interfaces stay fixed | User, Default (public interfaces fixed) |
| Safety net: tests that cover the behaviour | Code |

Behaviour must not change. Run the tests before and after.

## Other
Ask yourself: what is the target, what is the change, how will we know it worked, and what must not
change? Answer from sources first.

## Greenfield app or multi-week initiative
Hand off to the intake skill. It needs a brief and a plan before any task can be specified.
