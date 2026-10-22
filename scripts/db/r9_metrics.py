"""R9: pilot metrics per sub-flow and team -> data/aggregates/r9-pilot-*.csv (aggregates only)."""
import collections, csv, datetime, os, sqlite3, statistics
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"), timeout=60)
AGG = os.path.join(ROOT, "data", "aggregates")
INVALID = {"Cannot Reproduce", "Duplicate", "Not a bug", "Works as Designed"}
rows = db.execute("""SELECT i.key, i.created, i.resolved, i.resolution, i.priority, i.team, i.incidents, i.ria_state, i.ai_label,
                     f.sub_flow, f.in_flow_scope, c.escape_cause, c.legacy_mentioned, c.regression
                     FROM issues i JOIN flow_tags f USING(key)
                     LEFT JOIN rca_class c ON c.key=i.key AND c.round='R9'""").fetchall()
def win(created): return "W_last" if created >= "2025-10-22" else "W_prev"
def days(a, b):
    if not b: return None
    f = lambda s: datetime.datetime.fromisoformat(s[:19])
    return (f(b) - f(a)).days

def metrics(group_rows):
    last = [r for r in group_rows if win(r[1]) == "W_last"]
    prev = [r for r in group_rows if win(r[1]) == "W_prev"]
    inc = [r[6] or 0 for r in last]
    res = [d for d in (days(r[1], r[2]) for r in last if r[3] and r[3].startswith("Fixed")) if d is not None]
    cls = [r for r in last if r[11]]
    esc = collections.Counter(r[11] for r in cls)
    fixes = [r for r in last if r[3] and r[3].startswith("Fixed")]
    return {
        "w_prev": len(prev), "w_last": len(last),
        "change_pct": round(100 * (len(last) - len(prev)) / len(prev)) if prev else "",
        "p1p2_pct_last": round(100 * sum(r[4] in ("P1", "P2") for r in last) / len(last)) if last else "",
        "incidents_sum_last": sum(inc), "incidents_avg_last": round(sum(inc) / len(inc), 1) if inc else "",
        "incidents_5plus_pct_last": round(100 * sum(i >= 5 for i in inc) / len(inc)) if inc else "",
        "median_days_to_fix_last": statistics.median(res) if res else "",
        "invalid_pct_last": round(100 * sum((r[3] or "") in INVALID for r in last) / len(last)) if last else "",
        "open_last": sum(1 for r in last if not r[3]),
        "rca_classified_last": len(cls),
        "top_escape_causes": "; ".join(f"{k} {v}" for k, v in esc.most_common(3)),
        "legacy_pct_classified": round(100 * sum(r[12] == "yes" for r in cls) / len(cls)) if cls else "",
        "regression_yes_pct_classified": round(100 * sum(r[13] == "yes" for r in cls) / len(cls)) if cls else "",
        "fix_ria_filled_pct": round(100 * sum(r[7] == "filled" for r in fixes) / len(fixes)) if fixes else "",
        "ai_label_last": sum(1 for r in last if r[8]),
    }

def write(name, key_name, groups):
    out = []
    for g, gr in sorted(groups.items(), key=lambda x: -len(x[1])):
        m = metrics(gr); m = {key_name: g, **m}; out.append(m)
    path = os.path.join(AGG, name)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
    print(path, len(out))

sub = collections.defaultdict(list); team = collections.defaultdict(list)
for r in rows:
    sub[r[9]].append(r); team[r[5] or "(empty)"].append(r)
sub["ALL in-flow scope"] = [r for r in rows if r[10] == 1]
sub["ALL Orchestration Core"] = list(rows)
write("r9-pilot-subflow.csv", "sub_flow", sub)
write("r9-pilot-team.csv", "team", {k: v for k, v in team.items() if len(v) >= 8})

# escape-cause profile: pilot (R9) vs all-CFB sample (R5-round1, excluding Orchestration Core keys)
def prof(sql):
    c = collections.Counter(x for (x,) in db.execute(sql)); n = sum(c.values()); return c, n
p9, n9 = prof("SELECT escape_cause FROM rca_class WHERE round='R9'")
p9f, n9f = prof("SELECT c.escape_cause FROM rca_class c JOIN flow_tags f USING(key) WHERE c.round='R9' AND f.in_flow_scope=1")
p5, n5 = prof("SELECT escape_cause FROM rca_class WHERE round='R5-round1' AND key NOT IN (SELECT key FROM flow_tags)")
with open(os.path.join(AGG, "r9-pilot-escape-profile.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["escape_cause", "pilot_n", "pilot_pct", "pilot_inflow_n", "pilot_inflow_pct", "other_vp_r5_n", "other_vp_r5_pct"])
    for k in sorted(set(p9) | set(p5), key=lambda k: -p9.get(k, 0)):
        w.writerow([k, p9.get(k, 0), round(100*p9.get(k, 0)/n9, 1), p9f.get(k, 0), round(100*p9f.get(k, 0)/n9f, 1), p5.get(k, 0), round(100*p5.get(k, 0)/n5, 1)])
    w.writerow(["TOTAL", n9, 100, n9f, 100, n5, 100])
print("profile n9", n9, "inflow", n9f, "r5 other", n5)

# cross-tab escape cause x introduced_by for pilot
ct = collections.Counter(db.execute("SELECT escape_cause, introduced_by FROM rca_class WHERE round='R9'").fetchall())
with open(os.path.join(AGG, "r9-pilot-escape-x-introduced.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["escape_cause", "introduced_by", "n"])
    for (a, b), n in sorted(ct.items(), key=lambda x: -x[1]): w.writerow([a, b, n])
