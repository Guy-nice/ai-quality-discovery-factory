"""M2-E8 requirements quality signals -> tables req_signals, e8_expectation_sample; CSV data/aggregates/m2-e8-requirements.csv.

Inputs: quality.sqlite, raw_local.sqlite (summaries, local), data/raw/m2e8/*.json (feature extracts made by
m2_e8_features.py from Jira searches; gitignored). Run from repo root: python3 -I scripts/db/m2_e8_requirements.py
"""
import csv, json, math, os, re, sqlite3, collections as C

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAWDB = os.path.join(ROOT, "data", "db", "raw_local.sqlite")
RAW = os.path.join(ROOT, "data", "raw", "m2e8")
OUT = os.path.join(ROOT, "data", "aggregates", "m2-e8-requirements.csv")
MI = re.compile(r"^\s*\[?\s*MI\b|investigatory ki|\bMI[- ]?\d{3,}|major incident", re.I)
EXP = {"works as designed", "not a bug", "limitation"}

# Manual classification (read summary + Jira comments + RCA), sample seed 20261025, n=40. Keys and codes only.
SAMPLE = {
    "PMSTND-2928": "expectation_gap", "DAT-31575": "expectation_gap", "CXWFM-61655": "expectation_gap",
    "CXDV-72718": "expectation_gap", "CXDV-72714": "expectation_gap", "CSA-83780": "expectation_gap",
    "DE-145954": "expectation_gap", "CXIA-5378": "expectation_gap", "CSA-85751": "expectation_gap",
    "AW-37399": "expectation_gap", "AW-36085": "expectation_gap",
    "PMSTND-1736": "documentation_gap", "AW-36736": "documentation_gap", "CXIA-8399": "documentation_gap",
    "RPT-52645": "documentation_gap", "CXIA-9447": "documentation_gap", "CXBI-6766": "documentation_gap",
    "PMSTND-2340": "user_or_config", "PMSTND-1843": "user_or_config", "CXDV-51660": "user_or_config",
    "DE-129109": "user_or_config", "DAT-32264": "user_or_config", "CXWFM-68792": "user_or_config",
    "ORC-51122": "misrouted_process_3rdparty", "ORC-40707": "misrouted_process_3rdparty",
    "CXREC-138532": "misrouted_process_3rdparty", "AAI-40990": "misrouted_process_3rdparty",
    "WFM-180367": "misrouted_process_3rdparty", "DE-149435": "misrouted_process_3rdparty",
    "CXDVI-15774": "real_defect_misclosed", "AW-40611": "real_defect_misclosed", "PAPI-10056": "real_defect_misclosed",
    "DE-126460": "real_defect_misclosed", "CXWFM-59911": "real_defect_misclosed", "AN-63970": "real_defect_misclosed",
    "CXQM-53651": "not_reproducible", "AW-42427": "not_reproducible",
    "PMSTND-2903": "unclear", "CXWFM-92578": "unclear", "AOR-15110": "unclear",
}


def wilson(k, n, z=1.96):
    if not n:
        return (None, None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(100 * p, 1), round(100 * (c - h), 1), round(100 * (c + h), 1))


def main():
    db = sqlite3.connect(DB)
    db.execute(f"ATTACH DATABASE '{RAWDB}' AS r")
    rows = db.execute(
        "SELECT i.key, i.created, i.resolution, i.rnd_vp, i.priority, i.incidents, t.summary FROM issues i "
        "LEFT JOIN r.issue_text t ON t.key = i.key WHERE i.is_cfb = 1 AND i.created >= '2025-01-01' "
        "AND i.created < '2026-10-23'").fetchall()
    rows = [x for x in rows if not (x[6] and MI.search(x[6]))]
    out = []

    def add(signal, scope, k, n, note=""):
        p, lo, hi = wilson(k, n)
        out.append(dict(signal=signal, scope=scope, k=k, n=n, pct=p, ci_low=lo, ci_high=hi, note=note))

    for y in ("2025", "2026"):
        ys = [x for x in rows if x[1][:4] == y and x[1][5:7] <= "10"]
        add("expectation_closure", f"all {y} Jan-Oct", sum(1 for x in ys if x[2] and x[2].lower() in EXP), len(ys))
    vp = C.defaultdict(lambda: [0, 0])
    for x in rows:
        v = x[3] or "(empty)"
        vp[v][1] += 1
        vp[v][0] += bool(x[2] and x[2].lower() in EXP)
    for v, (k, n) in sorted(vp.items()):
        add("expectation_closure", f"VP {v} 2025-01..2026-10", k, n)
    e = [x for x in rows if x[2] and x[2].lower() in EXP]
    add("expectation_closure_p1p2", "2025-01..2026-10", sum(1 for x in e if x[4] in ("P1", "P2")), len(e),
        f"avg incidents {round(sum(x[5] or 0 for x in e) / len(e), 2)}")

    cnt = C.Counter(SAMPLE.values())
    for c, k in sorted(cnt.items()):
        add("expectation_sample_class", c, k, len(SAMPLE), "n=40 random, seed 20261025")
    req = cnt["expectation_gap"] + cnt["documentation_gap"]
    add("expectation_sample_class", "requirements_or_doc_gap (combined)", req, len(SAMPLE))
    db.execute("DROP TABLE IF EXISTS e8_expectation_sample")
    db.execute("CREATE TABLE e8_expectation_sample (key TEXT PRIMARY KEY, class TEXT)")
    db.executemany("INSERT INTO e8_expectation_sample VALUES (?,?)", SAMPLE.items())

    seen = {}
    for k, ec, v in db.execute(
            "SELECT c.key, c.escape_cause, i.rnd_vp FROM rca_class c JOIN issues i ON i.key = c.key "
            "WHERE c.round IN ('R9','R5-round1') ORDER BY CASE c.round WHEN 'R9' THEN 0 ELSE 1 END"):
        seen.setdefault(k, (ec, v))
    add("rca_requirements_gap", "all classified fixed CFBs", sum(1 for ec, _ in seen.values()
        if ec == "requirements/spec gap"), len(seen))
    for v in sorted({v for _, v in seen.values()}, key=lambda s: s or ""):
        sub = [ec for ec, vv in seen.values() if vv == v]
        add("rca_requirements_gap", f"VP {v}", sum(1 for ec in sub if ec == "requirements/spec gap"), len(sub))

    cau = json.load(open(os.path.join(RAW, "causing.json")))
    ctl = json.load(open(os.path.join(RAW, "match.json")))["ctrl"]
    cp = C.Counter(x["project"] for x in ctl)
    left, sub = C.Counter(cp), []
    for c in cau:
        if left[c["project"]] > 0:
            sub.append(c)
            left[c["project"]] -= 1
    for f in ("ac_real", "spec_link"):
        add(f"story_{f}", "causing stories (project-matched)", sum(x[f] for x in sub), len(sub))
        add(f"story_{f}", "control stories", sum(x[f] for x in ctl), len(ctl))
    ef = {x["key"]: x for x in json.load(open(os.path.join(RAW, "epicfeat.json")))}
    mp = json.load(open(os.path.join(RAW, "epics.json")))["map"]
    for name, s in (("causing", cau), ("control", ctl)):
        eps = [ef.get(mp.get(x["key"])) for x in s]
        eps = [x for x in eps if x]
        add("epic_ac_real", f"{name} stories' epics", sum(x["ac_real"] for x in eps), len(eps))
        add("epic_spec_link", f"{name} stories' epics", sum(x["spec_link"] for x in eps), len(eps))
        both = [max(x["spec_link"], (ef.get(mp.get(x["key"])) or {}).get("spec_link", 0)) for x in s]
        add("story_or_epic_spec_link", name, sum(both), len(both))

    db.execute("DROP TABLE IF EXISTS req_signals")
    db.execute("CREATE TABLE req_signals (signal TEXT, scope TEXT, k INTEGER, n INTEGER, pct REAL, "
               "ci_low REAL, ci_high REAL, note TEXT)")
    db.executemany("INSERT INTO req_signals VALUES (:signal,:scope,:k,:n,:pct,:ci_low,:ci_high,:note)", out)
    db.commit()
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for o in out:
        print(o)


if __name__ == "__main__":
    main()
