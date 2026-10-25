"""Mission v2 (Q-B, E4): classify valid CFBs 2025-01..2026-10 into failure types.

Pass 1 = ordered keyword rules on summary (+ RCA text when the summary gives no hit).
Pass 2 = manual corrections after reading, in scripts/db/m2_failure_overrides.csv (key,failure_type).
Writes table failure_types(key, failure_type, correctness, method) in quality.sqlite.
Free text is read from raw_local.sqlite only; nothing textual is written to quality.sqlite.

Run from repo root: python3 -I scripts/db/m2_failure_types.py [--dump N OFFSET]
"""
import csv
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAW = os.path.join(ROOT, "data", "db", "raw_local.sqlite")
OVR = os.path.join(ROOT, "scripts", "db", "m2_failure_overrides.csv")
INVALID = ("cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid")

TYPES = {
    "DATA": ("Data / reporting correctness", "Y"),
    "BILLING": ("Billing / usage / license correctness", "Y"),
    "ROUTING": ("Routing correctness", "Y"),
    "LIFECYCLE": ("Contact lifecycle and media (stuck, lost, dropped, transfer, audio)", "Y"),
    "AGENTSTATE": ("Agent state / session correctness", "Y"),
    "WFM": ("WFM schedule / forecast / adherence correctness", "Y"),
    "RECQM": ("Recording / QM / analytics / AI-output correctness", "Y"),
    "AVAIL": ("Availability / outage / cannot log in or load", "N"),
    "FUNC": ("Feature failure / error (action fails, no wrong-data outcome)", "N"),
    "PERF": ("Performance / latency / timeout", "N"),
    "UI": ("UI / usability / display / localization", "N"),
    "INTEG": ("Integration / API / CRM / third-party contract", "N"),
    "SECURITY": ("Security / permission / access control", "N"),
}

# Ordered rules: first hit wins.
RULES = [
    ("SECURITY", r"\b(security|vulnerab|xss|csrf|permission|unauthori[sz]ed|access control|role[s]? (not|do)|privilege|cross[- ]?(bu|tenant)|sso|saml|mfa|password|pii|redact)"),
    ("PERF", r"\b(slow|latenc|performance|timeout|timing out|times out|delay(ed)?\b|lag\b|lagging|takes (a )?long|high cpu|memory leak|hang(s|ing)?\b|freez)"),
    ("BILLING", r"\b(billing|billable|invoice|usage report|usage data|licen[cs]e count|license usage|charg(e|ed|ing)\b|cost\b|minutes billed)"),
    ("LIFECYCLE", r"\b(stuck|lost contact|lost call|ghost|phantom|orphan|call(s)? drop|dropp(ed|ing) (call|contact|chat)|disconnect|one[- ]way audio|no audio|audio (issue|problem|loss)|dead air|transfer|conference|hold\b|contact(s)? (not )?(end|clos)|not ending|never end|abandon)"),
    ("ROUTING", r"\b(rout(e|ed|ing)|skill(s)? (not|assign|prior)|queue|priority boost|misrout|wrong agent|not deliver(ed)? to agent|offered to|acd distribut|find ?match|afm\b|vfm\b|longest available|proficiency)"),
    ("AGENTSTATE", r"\b(agent (state|status)|unavailable code|state (not|stuck|incorrect)|status (not|stuck|incorrect|showing)|logged out|log(s|ged)? (agent )?out|auto[- ]?logout|refused|outstate|acw\b|after call work|agent session|session (end|expire|drop))"),
    ("WFM", r"\b(wfm|schedul(e|ing)|forecast|adherence|shift|time off|intraday|staffing|erlang|capacity plan|strategic plan)"),
    ("RECQM", r"\b(record(ing|ings|er)|screen ?rec|qm\b|quality management|evaluation|scorecard|calibration|interaction analytics|\bia\b|transcri|sentiment|coaching)"),
    ("DATA", r"\b(incorrect|wrong|inaccurate|mismatch|discrepanc|missing (data|contacts|records|values|from report)|not (match|matching|accurate)|duplicat(e|ed) (data|record|row)|double count|count(s)? (are|is) (off|wrong)|data (issue|missing|delay|not)|report(s|ing)? (show|shows|showing|display)|dashboard (show|shows|showing|display)|values? (are|is) (wrong|incorrect|0|zero)|data ?share|data ?lake|csif|negative)"),
    ("AVAIL", r"\b(outage|down\b|unable to (log ?in|login|access|load|launch)|cannot (log ?in|login|access|load)|can't (log ?in|login|access|load)|not loading|fails? to load|failed to load|blank (page|screen)|white screen|503|502|500 error|service unavailable|unreachable|mi \d|major incident)"),
    ("INTEG", r"\b(api\b|integration|crm|salesforce|zendesk|servicenow|dynamics|teams\b|webhook|sftp|ftp\b|connector|sdk\b|oauth|third[- ]party|external|cti\b|middleware)"),
    ("UI", r"\b(ui\b|display|button|overflow|alignment|label|tooltip|translation|locali[sz]|language|font|icon|column|filter|sort|search|dropdown|scroll|layout|small ?view|max\b|pop ?up|modal|tab\b|view\b)"),
    ("FUNC", r"."),
]
RX = [(t, re.compile(p, re.I)) for t, p in RULES]

# Real-time dashboard / reporting projects: "stuck contact" here = stale display state, not a stuck live contact.
DASH_PROJECTS = {"CXDV", "CXDVI", "DAT", "RPT", "CXBI", "DL", "CXDBR"}

# Domain hints for summaries that only name a product area.
DATA_HINT = re.compile(r"\b(report|dashboard|widget|data|metric|kpi|export)", re.I)


def classify(summary, rca):
    s = summary or ""
    for t, rx in RX[:-1]:
        if rx.search(s):
            return t, "rule-summary"
    if DATA_HINT.search(s):
        return "DATA" if re.search(r"(show|display|value|count|total|number)", s, re.I) else "FUNC", "rule-hint"
    for t, rx in RX[:-1]:
        if rca and rx.search(rca[:1500]):
            return t, "rule-rca"
    return "FUNC", "rule-default"


def valid_keys(db):
    q = ("SELECT i.key FROM issues i WHERE i.is_cfb = 1 AND i.created >= '2025-01-01' AND i.created < '2026-10-23' "
         "AND (i.resolution IS NULL OR lower(i.resolution) NOT IN (%s))" % ",".join("?" * len(INVALID)))
    return [k for (k,) in db.execute(q, INVALID)]


def main():
    db = sqlite3.connect(DB)
    raw = sqlite3.connect(RAW)
    text = {k: (s, r) for k, s, r in raw.execute("SELECT key, summary, rca FROM issue_text")}
    overrides = {}
    if os.path.exists(OVR):
        with open(OVR) as f:
            for row in csv.DictReader(f):
                overrides[row["key"].strip()] = row["failure_type"].strip()
    keys = valid_keys(db)
    rows = []
    for k in keys:
        s, r = text.get(k, (None, None))
        t, m = classify(s, r)
        if t == "LIFECYCLE" and k.split("-")[0] in DASH_PROJECTS:
            t, m = "DATA", "rule-dashboard-state"
        if k in overrides:
            t, m = overrides[k], "manual"
        rows.append((k, t, TYPES[t][1], m))
    if len(sys.argv) > 1 and sys.argv[1] == "--dump":
        n, off = int(sys.argv[2]), int(sys.argv[3])
        for k, t, c, m in sorted(rows)[off:off + n]:
            s = (text.get(k, ("", ""))[0] or "")[:120]
            print(f"{k}|{t}|{s}")
        return
    db.execute("DROP TABLE IF EXISTS failure_types")
    db.execute("CREATE TABLE failure_types (key TEXT PRIMARY KEY, failure_type TEXT, correctness TEXT, method TEXT)")
    db.executemany("INSERT INTO failure_types VALUES (?,?,?,?)", rows)
    db.commit()
    from collections import Counter
    print(len(rows), Counter(t for _, t, _, _ in rows).most_common(), Counter(m for *_, m in rows))


if __name__ == "__main__":
    main()
