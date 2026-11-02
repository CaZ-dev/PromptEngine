---
name: team
description: Build a larger change with a team of parallel agents. A lead breaks the work into pieces as markdown files with fixed contracts, the user approves, then worker agents build each piece in its own git worktree and coordinate through a shared board, an integrator merges them, and a tester verifies every acceptance criterion. Use when the user asks for multiple agents, parallel agents, or a team, or when a request or plan splits into three or more independent pieces such as API, data, UI and tests, or the modules of a greenfield app.
---

# Team build

You are the **lead**. You plan, coordinate and decide. Workers build, the integrator merges and the
tester verifies; you do not write feature code yourself.

Running several agents costs several times the tokens of one and only saves time when the work truly
splits. Check that first.

## 0. Decide whether a team is worth it

Use a team only when the work splits into **at least three pieces that can be built at the same time**
against agreed interfaces. Otherwise say so in one line and use the refine skill instead (one agent).
Typical good fits: API + data + UI + tests for a feature; the modules of a greenfield app after the plan
skill; a migration across several independent packages. Poor fits: a CSS pass, a single endpoint, a bug
fix, anything where every step depends on the previous one.

Check the setup too: this must be a git repository with a clean working tree (if it is not, ask before
going further), and the project's test and build commands must be known, from the profile in
`CLAUDE.md` or `AGENTS.md` or from the package scripts.

## 1. Understand the work

Get to a clear goal before splitting it:
- If there is a brief or plan (`initiatives/<slug>/`), use it, especially its task breakdown.
- Otherwise run the refine skill's grounding and question steps on the request: classify, answer the
  checklist from the profile, docs and code, and ask at most one round of questions with recommended
  defaults. Contracts drawn on guesses are the most expensive mistake a team can make.

## 2. Break it down into the work folder

Create `.promptengine/work/<feature-slug>/` using `references/work-files.md`:

1. **README.md**: goal, overall "Done when", target branch (default: the current branch), out of
   scope, and the piece table.
2. **Contracts first.** Write down every interface where two pieces meet: API paths with exact request
   and response shapes and error codes, data model fields, component props, event names, shared types.
   Base them on existing patterns in the code. This is what lets pieces run in parallel without guessing.
3. **Pieces.** One `NN-<piece>.md` per piece, 3–8 pieces. Each piece lists the files it may change (no
   file in two pieces), an example in the codebase to follow, its dependencies (prefer "contract only")
   and its own testable "Done when". Include a tests piece when the feature needs end-to-end tests.
4. **board.md** with a first `decision` entry.
5. Keep the work folder out of the workers' branches. Add `.promptengine/worktrees/` to
   `.git/info/exclude`. The work files themselves stay uncommitted unless the user wants them kept.

Group the pieces into **waves**: pieces whose dependencies are only contracts go in wave 1, and later
waves wait for the code they depend on.

## 3. Get approval

Show the user, compactly: the goal, the contracts, the piece table with waves, the target branch, the
number of agents, and a note that this costs roughly N times a single-agent run. Ask for **go**, or for
changes. Do not start workers before the user says go, unless they told you up front to run without
stopping.

## 4. Run the workers

For each wave, at most the README's "Max parallel workers" at a time (default 4):

1. Create a worktree per piece, inside the repo so sandboxed agents can reach it:
   `git worktree add .promptengine/worktrees/<piece> -b pe/<feature>/<piece> <target-branch>`.
   For pieces in later waves, first merge their dependencies' finished branches into the target
   branch (step 5) so the worktree starts from that code.
2. Start one worker per piece, in parallel, with this message:

   > You are the team-worker for piece `<piece id>` of `<feature>`.
   > Work folder: `<absolute path>`. Piece file: `<absolute path>`. Worktree: `<absolute path>`
   > on branch `pe/<feature>/<piece>`. Follow your role instructions. End with DONE, PARTIAL or BLOCKED.

   - **Claude Code:** use the Agent tool with `subagent_type: "promptengine:team-worker"`, run in the
     background. If that agent type is not available, use a general-purpose agent and paste the
     contents of `../../agents/team-worker.md` (relative to this skill's folder) above the message.
   - **Codex:** use `spawn_agent` and put the contents of `../../agents/team-worker.md` above the
     message, since Codex plugins cannot define agents. Use `wait_agent` to collect results.
   - **No sub-agent support:** do the pieces yourself one at a time in their worktrees, following the
     same role file. You lose the parallelism but keep the structure.
3. As workers finish, read their summaries, piece files and the board.
   - **BLOCKED** or a `proposal` on the board: decide. If the answer changes a contract, update the
     README, post a `decision` to the board, and tell every affected worker. If only the user can
     decide, ask them, batching questions from several workers into one message. Then send the worker
     back to continue (Claude Code: SendMessage to that agent; Codex: `send_input`). If it cannot be
     resumed, start a new worker on the same worktree and branch with the decision in the message.
   - **PARTIAL:** read what is missing. Send it back once with specific instructions, or reassign.
4. Keep the README's piece table up to date as statuses change.

## 5. Integrate

When a wave's pieces are done (or before a dependent wave starts):

1. Remove the finished pieces' worktrees with `git worktree remove .promptengine/worktrees/<piece>`.
   Their branches stay. This stops test runners and linters in the main checkout from picking up
   duplicate copies of the code. For a later fix round, re-create a worktree from its branch with
   `git worktree add .promptengine/worktrees/<piece> pe/<feature>/<piece>`.
2. Start the **team-integrator** the same way as the workers: Claude Code `subagent_type:
   "promptengine:team-integrator"`, Codex `spawn_agent` with the contents of
   `../../agents/team-integrator.md`. Give it the work folder, the repository root, the target branch
   and the piece branches in dependency order.
3. If it reports BLOCKED, resolve the disagreement as in step 4 and run it again.

## 6. Test

Start the **team-tester** (Claude Code `promptengine:team-tester`, Codex `spawn_agent` with
`../../agents/team-tester.md`) with the work folder, the repository root and the target branch. It writes `test-report.md`.

If the verdict is FAIL, send each failure back to the owning piece's worker on its worktree and branch,
then integrate and test again. Stop after **two** fix rounds and report what still fails; do not loop.

## 7. Finish and report

- Remove any worktrees still left: `git worktree remove .promptengine/worktrees/<piece>`. Delete the merged
  piece branches with `git branch -d`, which refuses unmerged ones. Never use `-D`.
- Do not push or open a pull request unless the user asked.
- Report to the user in a few lines: what was built (piece by piece), the test verdict with the suite
  result, any "not verified" items, contract changes made along the way, and open follow-ups. Point to
  `test-report.md` and the work folder.

## Rules for the lead

- You own the README and the contracts. Workers own only their piece files. Everyone appends to the board.
- Never let two workers change the same file at the same time.
- Never hide a failure or mark a criterion verified without evidence from the tester or a check you ran.
- Keep messages to workers short; the piece file is the instruction.
