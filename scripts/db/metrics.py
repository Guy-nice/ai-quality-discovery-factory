"""Monthly success measures S1-S7 for the pilot (Gate 4 package). Writes table metrics_monthly in quality.sqlite.

Run from repo root after each data refresh: python3 -I scripts/db/metrics.py
"""
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}
PILOT_REPOS = ("inContact", "app-findmatch", "orch-entity-agent", "orch-entity-orchestration",
               "orch-entity-state-streams-common", "orchestration-resolver", "routing-ng-advanced-findmatch",
               "routing-ng-agent-capacity-service", "routing-ng-blender", "routing-ng-contact-retry",
               "routing-ng-match-distributor")


def month(ts):
    return ts[:7] if ts else None


def main():
    db = sqlite3.connect(DB)
    pilot = db.execute(
        "SELECT i.key, i.created, i.resolution, i.priority, i.incidents FROM issues i "
        "JOIN flow_tags f ON f.key = i.key WHERE i.is_cfb = 1 AND f.in_flow_scope = 1").fetchall()
    classes = {k: (e, p) for k, e, p in db.execute(
        "SELECT key, escape_cause, prevention_action_type FROM rca_class WHERE round = 'R9'")}
    rows = {}
    for key, created, resolution, priority, incidents in pilot:
        m = rows.setdefault(month(created), {"all": 0, "valid": 0, "inc": [], "race": 0, "monitor": 0, "classified": 0})
        m["all"] += 1
        if not (resolution and resolution.lower() in INVALID):
            m["valid"] += 1
        if incidents is not None:
            m["inc"].append(incidents)
        if key in classes:
            m["classified"] += 1
            m["race"] += classes[key][0] == "scale/performance/concurrency/race"
            m["monitor"] += classes[key][1] == "monitoring/alert"
    keyed = {}
    for repo, date, keys in db.execute(
            f"SELECT repo, date, msg_keys FROM git_commits WHERE is_bot = 0 AND is_merge = 0 "
            f"AND repo IN ({','.join('?' * len(PILOT_REPOS))})", PILOT_REPOS):
        k = keyed.setdefault(month(date), [0, 0])
        k[0] += 1
        k[1] += bool(json.loads(keys or "[]"))
    min_bus = db.execute(
        "SELECT MIN(o.bus_factor_50) FROM r14_ownership o JOIN (SELECT repo, path FROM r3_dir_hotspots "
        "WHERE is_test_path = 0 ORDER BY pilot_fix_24m DESC LIMIT 10) h ON h.repo = o.repo AND h.path = o.path"
    ).fetchone()[0]
    db.execute("DROP TABLE IF EXISTS metrics_monthly")
    db.execute("CREATE TABLE metrics_monthly (month TEXT PRIMARY KEY, s1_valid_cfb INTEGER, all_cfb INTEGER, "
               "s2_race_share_pct REAL, s3_incidents_per_cfb REAL, s4_monitor_action_pct REAL, "
               "s5_min_bus_factor_top10 INTEGER, s6_jira_key_pct REAL, s7_invalid_pct REAL, rca_classified INTEGER)")
    for m in sorted(set(rows) | set(keyed)):
        if not m or m < "2024-10":
            continue
        r = rows.get(m, {"all": 0, "valid": 0, "inc": [], "race": 0, "monitor": 0, "classified": 0})
        c = r["classified"]
        k = keyed.get(m, [0, 0])
        db.execute("INSERT INTO metrics_monthly VALUES (?,?,?,?,?,?,?,?,?,?)", (
            m, r["valid"], r["all"],
            round(100 * r["race"] / c, 1) if c else None,
            round(sum(r["inc"]) / len(r["inc"]), 2) if r["inc"] else None,
            round(100 * r["monitor"] / c, 1) if c else None,
            min_bus,
            round(100 * k[1] / k[0], 1) if k[0] else None,
            round(100 * (r["all"] - r["valid"]) / r["all"], 1) if r["all"] else None,
            c))
    db.commit()
    for row in db.execute("SELECT * FROM metrics_monthly ORDER BY month"):
        print(row)


if __name__ == "__main__":
    main()
