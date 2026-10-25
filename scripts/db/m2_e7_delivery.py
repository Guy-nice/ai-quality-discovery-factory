"""M2-E7 delivery and release outcomes. Reads fixVersion dumps (data/raw/e7), DB tables, ServiceNow monthly change counts.

Writes tables release_events, cfb_fix_channel, delivery_monthly; CSV data/aggregates/m2-e7-delivery.csv.
Run from repo root: python3 -I scripts/db/m2_e7_delivery.py
"""
import collections
import csv
import datetime as dt
import glob
import json
import os
import re
import sqlite3
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAW = os.path.join(ROOT, "data", "db", "raw_local.sqlite")
DUMPS = os.path.join(ROOT, "data", "raw", "e7", "*.json")
OUT = os.path.join(ROOT, "data", "aggregates", "m2-e7-delivery.csv")
MI = re.compile(r"^\s*\[?\s*MI\b|investigatory ki|\bMI[- ]?\d{3,}|major incident", re.I)
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}

# ServiceNow change_request counts by opened_at month (snow_get_stats group_by type, run 2026-10-25; 2026-10 partial).
SN = {
    "2025-01": (74, 1191, 2888), "2025-02": (71, 1293, 2162), "2025-03": (98, 1188, 2225), "2025-04": (97, 1291, 2391),
    "2025-05": (97, 1181, 2930), "2025-06": (106, 1318, 2472), "2025-07": (120, 1491, 2650), "2025-08": (109, 1261, 3753),
    "2025-09": (124, 1441, 2406), "2025-10": (158, 1261, 3308), "2025-11": (167, 824, 3118), "2025-12": (128, 584, 1132),
    "2026-01": (101, 1334, 3607), "2026-02": (130, 1218, 3808), "2026-03": (109, 1465, 4183), "2026-04": (109, 1468, 4185),
    "2026-05": (136, 1390, 4021), "2026-06": (269, 1271, 5006), "2026-07": (366, 1763, 4509), "2026-08": (377, 1178, 4002),
    "2026-09": (324, 2083, 3633), "2026-10": (202, 2529, 2392),
}
RANK = {"breakfix": 0, "cumulative_update": 1, "sprint": 2, "major": 3, "unscheduled": 4, "none": 5}


def version_class(v):
    name, desc = v.get("name", ""), (v.get("description") or "")
    text = f"{name} {desc}".lower()
    if re.search(r"\bbf\d*\b|break ?fix|\bhf\b|hotfix|\.hf-", text) or re.match(r"^\d+\.\d+\.\d+\.\d+", name):
        return "breakfix"
    if "cumulative update" in text or re.search(r"\bcu\d*\b", text) or re.match(r"^\d+\.\d+\.\d+(-agent)?$", name.lower()):
        return "cumulative_update"
    if "sprint" in text or re.match(r"^(cx\.)?\d+\.\d+\.\d{3}$|^\d+\.\d{3}-", name.lower()) or re.match(r"^\d+\.\d{3}-", name):
        return "sprint"
    if re.match(r"^(pm |cxws |sfv-|ms)?\d+\.\d+(-\w+)?$", name.lower()) or "combined release" in text or "pipeline release" in text or "major" in text:
        return "major"
    return "unscheduled"


def main():
    db = sqlite3.connect(DB)
    db.execute("ATTACH DATABASE ? AS r", (RAW,))
    summaries = dict(db.execute("SELECT key, summary FROM r.issue_text"))
    issues = {}
    for f in glob.glob(DUMPS):
        for n in json.load(open(f))["issues"]["nodes"]:
            issues[n["key"]] = n["fields"]
    versions = {}
    fix_rows = []
    for key, fl in issues.items():
        vs = fl.get("fixVersions") or []
        classes = []
        for v in vs:
            c = version_class(v)
            classes.append(c)
            versions[v["id"]] = (v["name"], v.get("releaseDate"), c)
        channel = min(classes, key=RANK.get) if classes else "none"
        is_mi = bool(MI.search(summaries.get(key) or ""))
        days = None
        if fl.get("resolutiondate"):
            days = (dt.date.fromisoformat(fl["resolutiondate"][:10]) - dt.date.fromisoformat(fl["created"][:10])).days
        fix_rows.append((key, fl["created"][:7], channel, int(is_mi), days))
    db.execute("DROP TABLE IF EXISTS release_events")
    db.execute("CREATE TABLE release_events (version_id TEXT PRIMARY KEY, name TEXT, release_date TEXT, class TEXT)")
    db.executemany("INSERT INTO release_events VALUES (?,?,?,?)", [(k, *v) for k, v in versions.items()])
    db.execute("DROP TABLE IF EXISTS cfb_fix_channel")
    db.execute("CREATE TABLE cfb_fix_channel (key TEXT PRIMARY KEY, created_month TEXT, channel TEXT, is_mi INTEGER, days_to_fix INTEGER)")
    db.executemany("INSERT INTO cfb_fix_channel VALUES (?,?,?,?,?)", fix_rows)

    valid = collections.Counter()
    for key, created, res in db.execute("SELECT key, created, resolution FROM issues WHERE is_cfb = 1 AND created >= '2025-01-01'"):
        if (res and res.lower() in INVALID) or MI.search(summaries.get(key) or ""):
            continue
        valid[created[:7]] += 1
    resolved = dict(db.execute("SELECT key, resolved FROM issues"))
    recent = collections.Counter()
    latency = collections.defaultdict(list)
    seen = set()
    for cfb, cause in db.execute("SELECT cfb_key, causing_key FROM causal_links"):
        created = db.execute("SELECT created FROM issues WHERE key = ?", (cfb,)).fetchone()
        if not created or cfb in seen or not resolved.get(cause) or MI.search(summaries.get(cfb) or ""):
            continue
        d = (dt.date.fromisoformat(created[0][:10]) - dt.date.fromisoformat(resolved[cause][:10])).days
        if d < 0:
            continue
        seen.add(cfb)
        latency[created[0][:7]].append(d)
        if d <= 90:
            recent[created[0][:7]] += 1
    rel = collections.defaultdict(collections.Counter)
    for _, (name, rdate, c) in versions.items():
        if rdate:
            rel[rdate[:7]][c] += 1
    ch = collections.defaultdict(collections.Counter)
    dfix = collections.defaultdict(list)
    for key, m, c, is_mi, days in fix_rows:
        if is_mi:
            continue
        ch[m][c] += 1
        if days is not None:
            dfix[m].append(days)

    db.execute("DROP TABLE IF EXISTS delivery_monthly")
    cols = ["month", "major_versions", "cu_versions", "breakfix_versions", "sn_emergency", "sn_normal", "sn_standard",
            "emergency_pct", "valid_cfb_ex_mi", "fixed_cfb_ex_mi", "fixed_via_breakfix", "fixed_via_cu", "breakfix_pct",
            "median_days_to_fix", "cfb_with_cause_known", "cause_within_90d", "median_latency_days"]
    db.execute(f"CREATE TABLE delivery_monthly ({', '.join(c + ' TEXT' if c == 'month' else c + ' REAL' for c in cols)})")
    rows = []
    for m in sorted(SN):
        em, no, st = SN[m]
        fixed = sum(ch[m].values())
        lat = latency.get(m, [])
        rows.append([m, rel[m]["major"], rel[m]["cumulative_update"], rel[m]["breakfix"], em, no, st,
                     round(100 * em / (em + no), 1), valid[m], fixed, ch[m]["breakfix"], ch[m]["cumulative_update"],
                     round(100 * ch[m]["breakfix"] / fixed, 1) if fixed else None,
                     statistics.median(dfix[m]) if dfix[m] else None, len(lat), recent[m],
                     statistics.median(lat) if lat else None])
    db.executemany(f"INSERT INTO delivery_monthly VALUES ({','.join('?' * len(cols))})", rows)
    db.commit()
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(rows)
    for r in rows:
        print(r)
    allc = collections.Counter(c for _, _, c, mi, _ in fix_rows if not mi)
    print("channel totals", allc, "issues", len(fix_rows))


if __name__ == "__main__":
    main()
