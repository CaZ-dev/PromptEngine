---
name: refine
description: Turn a rough coding request into a grounded task spec before building it. Use when the user asks for a change in a short or vague way, such as "create an API for this and implement it in the UI", "improve the CSS and design of my UI", "based on this doc please build X", "add login", "fix the dashboard", or when a request leaves the scope, the target files, the data shape or what "done" means unclear. Works out what it can from the codebase and the docs, asks only what they cannot answer (once, with recommended defaults), confirms a short spec, then implements and verifies it.
---

# Refine a request, then build it

The user's request is their intent, not a specification. They may not know the codebase well, or may
know it and still write a short prompt. Your job is to turn the intent into a precise task with as few
round trips and as little wasted reading as possible, then do it.

The two failure modes to avoid:
- **Guessing**: building on assumptions the user never confirmed, then redoing the work.
- **Interrogating**: asking the user things the code, the docs or common sense already answer.

## 0. Decide whether refining is worth it

Skip straight to the work (step 6) when the request already names the target, the change and the
expected result, or is a small change you can fully verify (a typo, a rename, one style tweak on a
named element). Say "Clear enough to do directly" and proceed. Refining a clear task wastes tokens.

Hand off to the intake skill instead when the request is a new product or greenfield app, or spans
several teams or weeks. Those need a brief and a plan, not a task spec.

## 1. Classify the request

Pick the closest type from `references/task-types.md` (API + UI feature, UI or design improvement,
doc-driven feature, bug fix, refactor, other). A request can combine types; use each one's checklist.
The checklist lists what must be known before building. That list drives everything below.

## 2. Ground it: answer the checklist from sources, not from the user

Work through the checklist and answer each item from, in order:

1. **Project profile.** If `CLAUDE.md` or `AGENTS.md` has a "Project profile" section (written by the profile skill), read it
   first. It holds the stack, commands and conventions, so you do not need to rediscover them.
2. **Docs the user referenced.** Read them in full. Pull out every concrete requirement, with a short
   quote or section reference, so the spec traces back to the doc.
3. **The codebase, targeted.** Search for the specific things the checklist needs: the nearest similar
   feature (an existing endpoint, page or component to copy the pattern from), the data model, the
   API client, the design tokens or theme file, the test setup. Use Grep and Glob with specific
   patterns. Read the few files that matter, not whole directories. The closest existing example
   is the best answer to most "how should this look" questions.
4. **Sensible defaults.** For anything still open, decide what a careful engineer on this codebase would
   choose, and treat it as a proposed default rather than a question.

Record each item as **Known** (with the file or doc it came from), **Default** (your proposal) or
**Unknown** (only the user can say, and the answer would change what you build).

## 3. Ask once, only what matters

Ask only about **Unknown** items, plus any **Default** that is risky to get wrong (data deletion, auth,
public API contracts, money, anything hard to undo). Rules:

- One round, at most 4 questions, most important first. Put every question in that one message.
- Each question names the recommended answer, so the user can reply "defaults are fine".
- Offer concrete options from what you found ("Use the existing `ApiClient` in `src/lib/api.ts`, or a
  new fetch wrapper?"), not open-ended prompts.
- Use your environment's structured question tool when it has one (AskUserQuestion in Claude Code).
- Never ask what you could look up.

If nothing is Unknown and no Default is risky, do not ask. Go to step 4.

## 4. Confirm a short spec

Write the spec using `references/spec-template.md`. Keep it to one screen: goal, what you found,
the changes per layer with file paths, acceptance criteria, out of scope, assumptions. For a small task,
compress it to a few bullets.

If you asked questions, fold in the answers and show the spec with them. If you did not need to ask,
show the spec and say you are proceeding. Then proceed, unless the task is large (many files, a schema
change, a public contract) or the user has asked to approve plans first. In those cases, wait for an OK.

For tasks larger than a few files, save the spec to `.claude/specs/<yyyy-mm-dd>-<slug>.md` so it
survives the session and can be reused or handed to someone else.

## 5. Write UI and API changes in the codebase's own idiom

- Copy the patterns of the nearest similar feature: file layout, naming, error handling, state
  management, styling approach, test style.
- Use the existing design tokens, components and spacing scale. Add new ones only when none fits,
  and say so.
- Never invent endpoints, fields, environment variables or library APIs. If you have not seen them in the
  code, the docs or the user's answers, they are assumptions: label them as such in the spec.

## 6. Build and verify against the acceptance criteria

Implement in small steps. Then check each acceptance criterion with the project's own commands
(tests, type check, lint, build), and for UI work look at the result where you can (run the app, take a
screenshot) rather than assuming the CSS does what you meant.

Finish with a short report: what changed (files), how each acceptance criterion was verified, what you
could not verify, and any assumption the user should confirm. Do not claim a criterion passed if you did not check it.

## Keeping tokens down

- Read the project profile before searching; suggest the profile skill if there is none and the user
  works in this repo often.
- Prefer one targeted search over reading a directory. Read the closest example, not every example.
- One question round. A spec the user can approve in one reply.
- Do not restate the user's request back to them at length; the spec is the restatement.
