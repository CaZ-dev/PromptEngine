# Deliverable outlines

Use the outline for the deliverable the brief asks for. Sections may be merged or dropped when the
brief gives nothing for them; say so rather than filling them with guesses.

## Project plan

1. **Summary**: the initiative in three sentences: problem, outcome, shape of the plan.
2. **Goals and how we will measure them**: table of goal, metric, baseline, target, date, how measured.
3. **Phases**: for each phase: goal, deliverables, exit criteria, rough duration.
4. **Milestones**: table of milestone, date, owner (role), depends on.
5. **Workstreams and roles**: who does what, sized against the team in Constraints.
6. **Dependencies**: external teams, vendors, decisions; what happens if each is late.
7. **Risks**: table of risk, likelihood, impact, mitigation, owner.
8. **First two weeks**: concrete tasks, each small enough to start tomorrow.
9. **Open decisions**: what the user must decide, by when, and the default if they do not.

## Product requirements document (PRD)

1. **Problem**: who, the pain, evidence.
2. **Goals and non-goals**: measurable goals; non-goals from Out of scope.
3. **Users**: personas or roles, with the job each is trying to do.
4. **User stories**: "As a …, I want …, so that …", each with acceptance criteria (Given/When/Then).
   Group by MUST / SHOULD / COULD.
5. **Non-functional requirements**: performance, security, compliance, accessibility, with numbers.
6. **Success metrics and instrumentation**: what is tracked and where.
7. **Release plan**: pilot, rollout, rollback.
8. **Open questions**.

## Technical design

1. **Context and goals**: what the system must do, with the numbers that drive design (load, data
   volume, latency, availability).
2. **Current state**: existing systems from Existing context.
3. **Proposed architecture**: components and how they interact (a mermaid diagram helps).
4. **Data model**: entities, key fields, ownership, retention.
5. **Interfaces**: APIs, events, integrations, with the contract for each.
6. **Key decisions**: for each: options considered, trade-offs, choice, and why.
7. **Security and compliance**.
8. **Rollout, migration and rollback**.
9. **Testing and observability**.
10. **Risks and open questions**.

## Task breakdown

1. **Epics**: one per major deliverable, each traced to a goal.
2. **Tasks per epic**: title, description, acceptance criteria, size (S ≤ 1 day, M ≤ 3 days,
   L ≤ 1 week; split anything bigger), dependencies, suggested role.
3. **Execution order**: what can run in parallel, the critical path.
4. **Capacity check**: total size against the team and timeline in the brief; flag a mismatch.

Prefer a table per epic. If the user wants issues created in a tracker, offer to format them for it.

## Readiness review

Do not plan. Report:
1. **Verdict**: can planning start, and with what caveats.
2. **Gaps**: from the review skill, most important first.
3. **Risks already visible** from the brief.
4. **Unvalidated assumptions** and how to test each cheaply.
5. **Questions to answer before starting**, each with who should answer it.
