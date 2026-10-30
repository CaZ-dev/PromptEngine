# Task spec template

Keep it to one screen. Every line should help either the user approve it or you build it.

```markdown
## Task: <short name>

**Goal:** <one sentence: who gets what outcome>
**Type:** <API + UI feature | UI improvement | doc-driven | bug fix | refactor | other>

### Found
- <fact> (`path/to/file.ts`)
- <requirement> (doc §2.3: "quote")

### Changes
- **API:** <endpoint, method, request → response> in `path/`
- **Data:** <model or migration change, or "none">
- **UI:** <component or page, states handled> in `path/`
- **Tests:** <what is added, where>

### Done when
- [ ] <testable criterion>
- [ ] <testable criterion>

### Not in this task
- <explicit exclusion>

### Assumptions
- <default you chose, and why> (say "change it" if wrong)

### Questions (only if any)
1. <question>? Recommended: <answer>.
```

## Small task version

```markdown
**Task:** <one line> · **Files:** `a.ts`, `b.css`
**Done when:** <one or two criteria>
**Assuming:** <the one default that matters>
```

## Example

Raw request: "create an api for invoices disputes and show it in the ui"

```markdown
## Task: Invoice dispute API and UI

**Goal:** Customers can dispute an invoice line from the invoice page, and the dispute is stored.
**Type:** API + UI feature

### Found
- REST routes live in `server/routes/*.ts` using `zod` validation (`server/routes/invoices.ts`)
- Invoice lines in `prisma/schema.prisma` (`InvoiceLine`); no dispute model yet
- Invoice page: `web/app/invoices/[id]/page.tsx`; data via `useQuery` + `web/lib/api.ts`

### Changes
- **Data:** new `Dispute` model (lineId, reason, status, createdBy, createdAt) + migration
- **API:** `POST /invoices/:id/lines/:lineId/disputes` → 201 `{ id, status }`; 400 on empty reason; 409 if already open
- **UI:** "Dispute" button per line → dialog with reason field; line shows "Disputed" badge
- **Tests:** route tests next to `invoices.test.ts`; component test for the dialog

### Done when
- [ ] Posting a reason creates a dispute and returns 201
- [ ] A second open dispute on the same line returns 409
- [ ] The line shows "Disputed" after submitting, with no page reload
- [ ] `npm test` and `npm run typecheck` pass

### Not in this task
- Resolving disputes, notifications, credit notes

### Assumptions
- Only the invoice's customer can dispute (same auth guard as `GET /invoices/:id`)

### Questions
1. Should a reason be required? Recommended: yes, 10–500 characters.
```
