# PromptEngine

Tools for handing a new initiative to Claude as a structured brief instead of a stream of statements.

When the input is unstructured (goals mixed with solutions, "make it faster", no scope edges, no
dates), Claude fills the gaps with its own guesses and the plan drifts from what you meant. PromptEngine
gives you one input format and two ways to check it before Claude starts planning.

## What's here

| Path | What it is | Use it when |
| --- | --- | --- |
| `templates/initiative-brief.md` | The input format: 14 sections, with guidance in each | You want to write the brief in a doc or editor |
| `tool/brief-builder.html` | A form that scores the brief as you type, flags vague or missing input, and generates a Claude-ready prompt | You want feedback while you write, then paste into claude.ai |
| `.claude/skills/initiative-intake/` | A Claude Code skill: paste raw notes, Claude maps them to the template, lists the gaps, asks you up to 5 questions, then plans | You'd rather dump notes and be interviewed |

## The format

The brief answers four questions, in this order:

1. **Why**: title, one-line summary, problem and why now, goals with measurable targets.
2. **Who and what**: users and stakeholders, in scope, out of scope, requirements (MUST / SHOULD / COULD).
3. **Reality**: constraints, existing context, timeline, risks and dependencies, assumptions and open questions.
4. **The ask**: which deliverable you want (project plan, PRD, technical design, task breakdown, readiness review), its format and audience, and whether Claude should ask questions first.

## What the review flags

- **Blocking**: a required section is empty, or something is both in and out of scope.
- **Unclear**: goals without numbers; vague words such as *better, faster, easy, user-friendly, scalable, ASAP, etc* (each comes with a suggestion for what to write instead); empty out-of-scope, constraints or timeline; a timeline with no date.
- **Suggestions**: requirements without priorities, lists written as paragraphs, undefined abbreviations, TBD / TODO left in the body.

The generated prompt wraps each section in XML tags, lists any gaps you chose not to fix under
`<known_gaps>`, and tells Claude to stay in scope, label its assumptions, and ask clarifying
questions before it writes the deliverable.

## Workflows

**Browser**: open `tool/brief-builder.html` (double-click it, no install needed). It opens with an
example brief that has deliberate gaps so you can see the review at work. Click *Clear all* to start
your own. Your draft is saved in that browser. *Import Markdown* accepts a brief written with the
template, and the *Markdown brief* tab exports it back.

**Claude Code**: in this repository, run `/initiative-intake` and paste your notes. The brief is saved
to `initiatives/<slug>/brief.md` and the deliverable next to it.

**Any chat**: copy `templates/initiative-brief.md`, fill it in, and paste it with a line such as
"Review this brief for gaps and ask me up to 5 questions before you plan."
