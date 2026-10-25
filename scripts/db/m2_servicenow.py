"""Load ServiceNow aggregate stats (M2-IMPACT) into quality.sqlite and write data/aggregates/m2-impact.csv.

Input: data/raw/servicenow/m2-stats-2026-10-25.json (aggregate counts only; no records, no names).
Run from repo root: python3 -I scripts/db/m2_servicenow.py
"""
import csv
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "data", "raw", "servicenow", "m2-stats-2026-10-25.json")
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
CSV = os.path.join(ROOT, "data", "aggregates", "m2-impact.csv")


def main():
    d = json.load(open(SRC))
    rows = []
    for q, v in d["sf_channel_by_quarter"].items():
        if q in ("query", "group_by"):
            continue
        total = sum(v.values())
        rows.append(("incident_sf_channel", q, "P1", v["1"], total))
        rows.append(("incident_sf_channel", q, "P2", v["2"], total))
        rows.append(("incident_sf_channel", q, "all", total, total))
    for h, v in d["changes_by_half"].items():
        if h in ("query", "group_by"):
            continue
        ne = v["normal"] + v["emergency"]
        rows.append(("change", h, "emergency", v["emergency"], ne))
        rows.append(("change", h, "normal", v["normal"], ne))
    for h, v in d["normal_change_close_by_half"].items():
        if h == "group_by":
            continue
        decided = v["failed_backed_out"] + v["failed_goal_not_met"] + v["success_with_issues"] + v["success_goal_met"]
        rows.append(("normal_change_outcome", h, "failed", v["failed_backed_out"] + v["failed_goal_not_met"], decided))
        rows.append(("normal_change_outcome", h, "success_with_issues", v["success_with_issues"], decided))
    r = d["p1_restore_buckets"]
    n = r["lt_4h"] + r["4h_24h"] + r["gt_24h"]
    for k in ("lt_4h", "4h_24h", "gt_24h"):
        rows.append(("p1_time_to_resolve", "2025-01..2026-10", k, r[k], n))
    p = d["p1_contact_type"]["counts"]
    for k, v in p.items():
        rows.append(("p1_channel", "2025-01..2026-10", k, v, sum(p.values())))
    db = sqlite3.connect(DB)
    db.execute("DROP TABLE IF EXISTS sn_aggregates")
    db.execute("CREATE TABLE sn_aggregates (metric TEXT, period TEXT, part TEXT, count INTEGER, denominator INTEGER, pct REAL)")
    out = [(m, per, part, c, den, round(100 * c / den, 1) if den else None) for m, per, part, c, den in rows]
    db.executemany("INSERT INTO sn_aggregates VALUES (?,?,?,?,?,?)", out)
    db.execute("INSERT INTO query_log(run_at,purpose,source,jql,dump_file,issues_loaded) VALUES (?,?,?,?,?,?)",
               (d["run_at"], "M2-IMPACT", "servicenow-stats", "see m2-stats json", os.path.basename(SRC), 0))
    db.commit()
    with open(CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "period", "part", "count", "denominator", "pct"])
        w.writerows(out)
    print(len(out), "rows")


if __name__ == "__main__":
    main()
