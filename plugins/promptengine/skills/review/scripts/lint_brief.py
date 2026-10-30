#!/usr/bin/env python3
"""Mechanical clarity checks for an Initiative Brief written with the plugin's template.

Usage:
    python3 lint_brief.py path/to/brief.md [--json]
    cat brief.md | python3 lint_brief.py - [--json]

Finds empty required sections, vague wording, goals without numbers, timelines
without dates, unprioritised requirements, undefined abbreviations and similar.
It only catches what a pattern can catch; the review skill adds judgement on top.
Exit code is 0 when there are no blocking issues, 1 otherwise.
"""

import json
import re
import sys

# (key, heading, required, recommended, min_words, checks)
SECTIONS = [
    ("title", "Title", True, False, 2, []),
    ("summary", "One-line summary", True, False, 10, []),
    ("problem", "Problem and why now", True, False, 30, ["solution_first"]),
    ("goals", "Goals and success metrics", True, False, 12, ["metric", "list"]),
    ("users", "Users and stakeholders", True, False, 6, []),
    ("in_scope", "In scope", True, False, 6, ["list"]),
    ("out_scope", "Out of scope", False, True, 3, ["list"]),
    ("requirements", "Requirements", True, False, 15, ["list", "priority"]),
    ("constraints", "Constraints", False, True, 6, []),
    ("context", "Existing context", False, False, 0, []),
    ("timeline", "Timeline and milestones", False, True, 4, ["date"]),
    ("risks", "Risks and dependencies", False, False, 0, []),
    ("assumptions", "Assumptions and open questions", False, False, 0, []),
    ("ask", "What I want from the agent", True, False, 4, []),
]

EMPTY_REASON = {
    "out_scope": "Without explicit exclusions the agent plans for everything that seems related.",
    "constraints": "Without limits, the agent plans for an unconstrained team, budget and stack.",
    "timeline": "Without dates, the agent cannot sequence or size the work.",
}

VAGUE = {
    "better": "Better than what, by how much?",
    "improve": "State today's value and the target value.",
    "improved": "State today's value and the target value.",
    "improving": "State today's value and the target value.",
    "enhance": "Say what changes and how you would measure it.",
    "optimize": "Name the metric being optimized and its target.",
    "optimise": "Name the metric being optimised and its target.",
    "fast": "Give a time, e.g. under 2 seconds or within 1 day.",
    "faster": "Give a time: from X to Y.",
    "quick": "Give a time or a step count.",
    "quickly": "Give a time or a step count.",
    "easy": "Say who it must be easy for and how you would test it.",
    "easily": "Say who it must be easy for and how you would test it.",
    "simple": "Simple for whom? Name a step count or a limit.",
    "user-friendly": "Replace with a testable behaviour, e.g. done in under 3 clicks.",
    "intuitive": "Replace with a testable behaviour, e.g. no training needed for first use.",
    "seamless": "Name the handoff that must not break.",
    "seamlessly": "Name the handoff that must not break.",
    "scalable": "Give the load it must handle: users, requests per second, records.",
    "robust": "Name the failure it must survive.",
    "efficient": "Efficient in time, cost or effort? Give a number.",
    "modern": "Name the actual technology or standard.",
    "flexible": "Say which variations it must support.",
    "streamline": "Name the steps being removed.",
    "leverage": "Say exactly what is reused and how.",
    "significant": "Give the number.",
    "significantly": "Give the number.",
    "some": "How many, or which ones?",
    "various": "List them.",
    "several": "How many?",
    "many": "How many?",
    "etc": "Finish the list; the agent will guess what 'etc' covers.",
    "stuff": "Name the actual items.",
    "things": "Name the actual items.",
    "asap": "Give a date.",
    "soon": "Give a date.",
    "good": "Define good with a measurable bar.",
    "nice": "Say whether it is required or optional.",
    "high quality": "Define the bar: error rate, review step, test coverage.",
    "best-in-class": "Name the benchmark you compare against.",
    "world-class": "Name the benchmark you compare against.",
}

KNOWN_ACRONYMS = set(
    "API APIS UI UX URL ID IDS SQL AWS GCP PDF CSV KPI KPIS MVP SLA HTML CSS JSON XML HTTP HTTPS "
    "SSO SAML OAUTH CRM ERP AI ML LLM PM QA CEO CTO CFO COO VP HR IT EU US UK USD EUR GDPR HIPAA "
    "SOC GA B2B B2C SAAS MUST SHOULD COULD WONT ASSUMPTION QUESTION TBD TODO TBC FAQ IOS OK AM ETA "
    "ASAP ROI OKR OKRS PR PRD".split()
)

DELIVERABLE_WORDS = r"\b(plan|prd|requirements doc|design|breakdown|tasks?|review|roadmap|estimate|spec)\b"
DATE_RE = re.compile(
    r"\b(19|20)\d{2}\b|\bQ[1-4]\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\b"
    r"|\b\d+\s*(day|week|month|sprint)s?\b|\b(week|sprint|month)\s*\d+\b|\b\d{1,2}[/.-]\d{1,2}([/.-]\d{2,4})?\b",
    re.I,
)
LIST_LINE = re.compile(r"^\s*([-*•]|\d+[.)])\s+\S")
WEIGHT = {"blocking": 12, "unclear": 5, "suggestion": 2}


def parse(md):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    by_heading = {h.lower(): k for k, h, *_ in SECTIONS}
    by_heading["what i want from claude"] = "ask"  # heading used by earlier versions of the template
    found = {k: "" for k, *_ in SECTIONS}
    present = set()
    for part in re.split(r"^##\s+", md, flags=re.M)[1:]:
        head, _, body = part.partition("\n")
        key = by_heading.get(head.strip().lower())
        if key:
            present.add(key)
            # A lone "-" left over from the template counts as empty.
            found[key] = re.sub(r"^\s*-\s*$", "", body, flags=re.M).strip()
    return found, present


def words(text):
    return len(re.findall(r"[^\W_][\w'’-]*", text))


def vague_terms(text):
    hits = []
    for term in VAGUE:
        if re.search(r"(^|[^\w-])" + re.escape(term) + r"(?=$|[^\w-])", text, re.I):
            hits.append(term)
    return hits


def lint(md):
    sections, present = parse(md)
    issues = []

    def add(sev, key, msg, tip=""):
        label = next(h for k, h, *_ in SECTIONS if k == key)
        issues.append({"severity": sev, "section": label, "message": msg, "tip": tip})

    if not present:
        add("blocking", "title", "No template headings found.",
            "Write the brief with the ## headings from the intake skill's brief-template.md.")

    for key, heading, required, recommended, min_words, checks in SECTIONS:
        text = sections[key]
        n = words(text)
        if not text:
            if required:
                add("blocking", key, f"{heading} is empty.")
            elif recommended:
                add("unclear", key, f"{heading} is empty.", EMPTY_REASON.get(key, ""))
            continue
        if min_words and n < min_words:
            add("unclear", key, f"{heading} is thin ({n} word{'s' if n != 1 else ''}).")

        vague = vague_terms(text)
        if vague:
            add("unclear", key, "Vague wording: " + ", ".join(f'"{v}"' for v in vague) + ".",
                " ".join(f"{v}: {VAGUE[v]}" for v in vague))
        if key != "assumptions" and re.search(r"\b(TBD|TODO|TBC)\b|\?\?+", text, re.I):
            add("suggestion", key, "Contains a placeholder (TBD / TODO / ??).",
                "Move the unknown to Assumptions and open questions.")

        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if "metric" in checks:
            no_num = [l for l in lines if not re.search(r"\d", l)]
            if no_num:
                add("unclear", key, f"{len(no_num)} goal(s) have no number, e.g. \"{no_num[0].lstrip('-*• ')[:60]}\".",
                    "Give each goal a baseline and a target, e.g. from 9 days to 3 days.")
        if "list" in checks and n > 25 and sum(bool(LIST_LINE.match(l)) for l in text.splitlines()) < 2:
            add("suggestion", key, f"{heading} is written as a paragraph.", "Put one item per line starting with '- '.")
        if "priority" in checks:
            missing = [l for l in lines if not re.search(r"\b(MUST|SHOULD|COULD|WON'?T)\b", l)]
            if missing:
                add("suggestion", key, f"{len(missing)} requirement(s) have no MUST / SHOULD / COULD.",
                    "Without priorities the agent treats every requirement as mandatory.")
        if "date" in checks and not DATE_RE.search(text):
            add("unclear", key, "No date or duration found.",
                "Add at least one date, quarter or duration, e.g. 'by 15 Jan 2027' or 'within 6 weeks'.")
        if "solution_first" in checks and re.match(
                r"^\s*(we\s+(need|want)\s+to\s+)?(build|create|make|develop|implement|add|launch)\b", text, re.I):
            add("suggestion", key, "Starts with a solution, not a problem.",
                "Describe who is hurting and how much first.")

    if sections["ask"] and not re.search(DELIVERABLE_WORDS, sections["ask"], re.I):
        add("blocking", "ask", "The deliverable is not named.",
            "Say which one: project plan, PRD, technical design, task breakdown or readiness review.")

    norm = lambda t: {l.lstrip("-*• ").strip().lower() for l in t.splitlines() if l.strip()}
    both = norm(sections["in_scope"]) & norm(sections["out_scope"])
    if both:
        add("blocking", "out_scope", f"\"{sorted(both)[0]}\" is listed as both in and out of scope.", "Pick one.")

    body = "\n".join(sections.values())
    acronyms = []
    for a in dict.fromkeys(re.findall(r"\b[A-Z][A-Z0-9]{1,5}\b", body)):
        base = a[:-1] if a.endswith("S") and a[:-1] in KNOWN_ACRONYMS else a
        if base in KNOWN_ACRONYMS or re.fullmatch(r"Q[1-4]", base):
            continue
        if re.search(rf"\({base}\)|\b{base}\s*(\(|=|:|—|-\s)", body):
            continue
        acronyms.append(base)
    if acronyms:
        where = next((k for k, *_ in SECTIONS if re.search(rf"\b{acronyms[0]}\b", sections[k])), "context")
        add("suggestion", where, "Undefined abbreviation(s): " + ", ".join(acronyms[:6]) + ".",
            "Spell each out once, e.g. 'AR (accounts receivable)'.")

    if re.search(r"technical design|architecture", sections["ask"], re.I) and not re.search(
            r"\b(stack|postgres|mysql|mongo|aws|gcp|azure|python|java|node|react|go|kotlin|swift|database|api|\.net|rails|django)\b",
            sections["constraints"] + " " + sections["context"], re.I):
        add("unclear", "constraints", "A technical design is requested but no tech stack is named.",
            "List the languages, frameworks, databases and hosting you must use.")

    score = max(0, 100 - sum(WEIGHT[i["severity"]] for i in issues))
    blocking = sum(i["severity"] == "blocking" for i in issues)
    verdict = "Not ready" if blocking else "Ready" if score >= 80 else "Needs work"
    order = {"blocking": 0, "unclear": 1, "suggestion": 2}
    issues.sort(key=lambda i: order[i["severity"]])
    return {"score": score, "verdict": verdict, "issues": issues}


def main(argv):
    args = [a for a in argv if a != "--json"]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    md = sys.stdin.read() if args[0] == "-" else open(args[0], encoding="utf-8").read()
    result = lint(md)
    if "--json" in argv:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Clarity score: {result['score']}/100 ({result['verdict']})")
        for i in result["issues"]:
            print(f"[{i['severity']}] {i['section']}: {i['message']}")
            if i["tip"]:
                print(f"    -> {i['tip']}")
        if not result["issues"]:
            print("No issues found by the mechanical checks.")
    return 1 if result["verdict"] == "Not ready" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
