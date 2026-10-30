#!/usr/bin/env python3
"""UserPromptSubmit hook: point the agent at the refine skill when a build request looks underspecified.

Reads the hook payload on stdin and, when the prompt asks for a change but gives little to go on,
prints a short note that the agent (Claude Code or Codex) adds to its context. It never blocks the prompt.

Skipped when:
- the prompt is a slash command, a question, or a short conversational reply;
- the prompt contains "--raw";
- PROMPTENGINE_NUDGE=off is set in the environment.
"""

import json
import os
import re
import sys

ACTION = re.compile(
    r"\b(create|build|implement|add|make|improve|fix|update|change|design|redesign|refactor|"
    r"integrate|develop|set ?up|write|migrate|revamp|clean ?up|polish|enhance|optimi[sz]e)\b",
    re.I,
)
VAGUE = re.compile(
    r"\b(improve|better|nicer?|modern|clean(er)?|proper(ly)?|good|polish|enhance|optimi[sz]e|"
    r"user[- ]friendly|intuitive|seamless|scalable|robust|some|various|etc|stuff|things|"
    r"this|that|it|asap|whatever|somehow)\b",
    re.I,
)
DOC_REF = re.compile(r"\b(based on|according to|as per|from|in) (this|the|that|attached) (doc|document|spec|prd|file|ticket|design)\b", re.I)
# Signs the user already gave specifics: paths, code identifiers, quoted text, lists, numbers with units.
SPECIFIC = re.compile(
    r"[\w-]+/[\w./-]+|\b[\w-]+\.(tsx?|jsx?|py|go|rb|java|kt|swift|css|scss|html|vue|svelte|sql|md|json|ya?ml)\b"
    r"|`[^`]+`|\"[^\"]{8,}\"|^\s*([-*]|\d+[.)])\s|\b\d+\s?(px|ms|s|rem|%|kb|mb)\b",
    re.I | re.M,
)
QUESTION = re.compile(r"^\s*(what|why|how|when|where|who|which|can|could|is|are|does|do|should|explain|tell me)\b", re.I)


def assess(prompt):
    text = prompt.strip()
    if not text or text.startswith("/") or "--raw" in text:
        return None
    words = re.findall(r"[\w'-]+", text)
    if len(words) < 4 or QUESTION.match(text) and not ACTION.search(text.split("?")[-1] or ""):
        return None
    if not (ACTION.search(text) or DOC_REF.search(text) or re.search(r"\b(please|pls|plz)\s+do\b", text, re.I)):
        return None

    signals = []
    vague = sorted({m.group(0).lower() for m in VAGUE.finditer(text)} - {"it", "this", "that"})
    pronouns = len(re.findall(r"\b(this|that|it)\b", text, re.I))
    specifics = len(SPECIFIC.findall(text))
    if len(words) < 25:
        signals.append("short request")
    if vague:
        signals.append("vague wording: " + ", ".join(vague[:4]))
    if pronouns >= 2 and specifics == 0:
        signals.append("refers to 'this/that/it' without naming it")
    if DOC_REF.search(text):
        signals.append("built from a document")
    if specifics == 0:
        signals.append("no files, names or criteria given")

    # Require at least two signals, and never nudge a request that is already concrete.
    if len(signals) < 2 or specifics >= 3:
        return None
    return signals


def main():
    if os.environ.get("PROMPTENGINE_NUDGE", "").lower() in ("off", "0", "false"):
        return 0
    try:
        payload = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    signals = assess(payload.get("prompt", "") or "")
    if not signals:
        return 0
    note = (
        "PromptEngine: this request may be underspecified (" + "; ".join(signals) + "). "
        "Unless the conversation already makes it clear, apply the promptengine:refine skill before editing: "
        "answer what you can from the codebase and any referenced docs, ask at most one round of questions "
        "with recommended defaults, confirm a short spec, then build and verify. "
        "If it is a small, clear change, just do it."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": note}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
