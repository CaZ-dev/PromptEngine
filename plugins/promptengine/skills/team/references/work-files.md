# Work folder templates

Everything for one team run lives in `.promptengine/work/<feature-slug>/` in the main checkout.

```
.promptengine/work/<feature>/
  README.md        goal, done-when, contracts, piece list, run settings   (lead only)
  01-<piece>.md    one file per piece                                    (lead writes; its worker updates)
  02-<piece>.md
  board.md         shared, append-only log                               (everyone appends)
  test-report.md   written by the tester
```

## README.md

```markdown
# <Feature name>

**Goal:** <one sentence: who gets what outcome>
**Source:** <the user's request, brief path or doc path>
**Target branch:** <branch the pieces merge into>
**Max parallel workers:** 4

## Done when
- [ ] <overall, testable criterion>

## Contracts
The fixed interfaces between pieces. Workers build to these exactly. Only the lead changes them, and
any change is posted to the board.

### API
`POST /invites` body `{ email: string, role: "admin" | "member" }`
→ 201 `{ id: string, status: "pending" }` · 400 `{ error: "invalid_email" }` · 409 `{ error: "already_invited" }`

### Data
`Invite { id uuid pk, email text unique, role text, status text default 'pending', created_at timestamptz }`

### UI
`<InviteForm onInvited(invite: Invite) />` in `web/components/invites/`

## Pieces
| Id | Piece | Depends on | Status |
| --- | --- | --- | --- |
| 01-db | Invite model and migration | | todo |
| 02-api | POST /invites | 01-db | todo |
| 03-ui | Invite form and list | contract only | todo |
| 04-tests | End-to-end invite test | 02-api, 03-ui | todo |

## Out of scope
- <exclusion>
```

"Depends on: contract only" means the piece can start right away, because it builds against the
contract rather than the other piece's code. Prefer this wherever it is true; it is what makes the
work parallel.

## Piece file (`NN-<piece>.md`)

```markdown
# 02-api: POST /invites

**Status:** todo          <!-- todo | in progress | blocked | done -->
**Owner:**
**Branch:** pe/<feature>/02-api
**Depends on:** 01-db

## Scope
<what this piece builds, in two to five lines>

## May change
- `server/routes/invites.ts` (new)
- `server/routes/index.ts` (register route)
- `server/routes/invites.test.ts` (new)

## Must not change
- Anything outside "May change", in particular other pieces' files and the contracts.

## Follow this example
`server/routes/members.ts`: same validation, error format and auth guard.

## Done when
- [ ] Valid body returns 201 with `{ id, status: "pending" }`
- [ ] Invalid email returns 400 `invalid_email`; duplicate returns 409 `already_invited`
- [ ] `npm test -- invites` and `npm run typecheck` pass

## Notes
<worker: blockers, what could not be verified, follow-ups>
```

Write pieces so that two pieces never list the same file under "May change". If they must (a shared
route index, for example), give that file to one piece only and have the other request the change
through the board, or add it to the integrator's instructions.

## board.md

```markdown
# Board: <feature>

Append-only. One entry per message, written with a single shell append. Newest at the bottom.

### <yyyy-mm-dd hh:mm> · lead · decision
Breakdown approved by the user. Wave 1: 01-db, 03-ui. Wave 2: 02-api. Wave 3: 04-tests.
```

Entry types: `question`, `proposal`, `decision`, `blocked`, `done`, `integrated`, `tested`.
