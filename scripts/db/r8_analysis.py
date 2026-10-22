"""R8: CFB-causing rate per resolved item, AI-implemented vs not. Writes data/aggregates/r8-ai-vs-nonai.csv."""
import csv, math, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"))
db.executescript(open(os.path.join(ROOT, "scripts", "db", "r8.sql")).read())
den = {(t, a, q): n for t, a, q, n in db.execute("SELECT issuetype, ai, rq, n FROM r8_denoms")}
Q = ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"]


def num(types, q, ai, primary_only):
    ph = ",".join("?" * len(types))
    sql = f"SELECT count(*) FROM r8_causing WHERE issuetype IN ({ph}) AND rq=? AND ai=?" + (" AND primary_src=1" if primary_only else "")
    return db.execute(sql, (*types, q, ai)).fetchone()[0]


def rr(a, na, b, nb):
    if not (a and b and na and nb):
        return None, None, None
    r = (a / na) / (b / nb)
    se = math.sqrt(1 / a - 1 / na + 1 / b - 1 / nb)
    return r, r * math.exp(-1.96 * se), r * math.exp(1.96 * se)


rows = []


def add(scope, types, quarters, primary_only, denom_not="all"):
    a = sum(num(types, q, "yes", primary_only) for q in quarters)
    b = sum(num(types, q, "not", primary_only) for q in quarters)
    na = sum(den.get((t, "yes", q), 0) for t in types for q in quarters)
    if denom_not == "all":
        nb = sum(den.get((t, "all", q), 0) for t in types for q in quarters) - na
    else:
        nb = sum(den.get((t, "notempty", q), 0) for t in types for q in quarters) - na
        b = sum(db.execute("SELECT count(*) FROM r8_causing WHERE issuetype=? AND rq=? AND ai_raw='No'" + (" AND primary_src=1" if primary_only else ""), (t, q)).fetchone()[0] for t in types for q in quarters)
    r, lo, hi = rr(a, na, b, nb)
    rows.append(dict(scope=scope, types="+".join(types), quarters=quarters[0] + ("" if len(quarters) == 1 else ".." + quarters[-1]),
                     source="primary" if primary_only else "all", ai_causing=a, ai_resolved=na, non_ai_causing=b, non_ai_resolved=nb,
                     ai_rate_per_1000=round(1000 * a / na, 2) if na else "", non_ai_rate_per_1000=round(1000 * b / nb, 2) if nb else "",
                     rate_ratio=round(r, 2) if r else "", ci_low=round(lo, 2) if lo else "", ci_high=round(hi, 2) if hi else ""))


for q in Q:
    add("quarter", ["Story", "Bug"], [q], False)
add("pooled", ["Story", "Bug"], ["2026-Q1", "2026-Q2"], False)
add("pooled", ["Story", "Bug"], ["2026-Q1", "2026-Q2"], True)
add("pooled", ["Story", "Bug"], ["2026-Q1", "2026-Q2", "2026-Q3"], False)
add("sens_b_stories_only", ["Story"], ["2026-Q1", "2026-Q2"], False)
add("sens_b_bugs_only", ["Bug"], ["2026-Q1", "2026-Q2"], False)
add("sens_a_reviewed_only(Yes vs No)", ["Story", "Bug"], ["2026-Q1", "2026-Q2"], False, denom_not="notempty")
add("sens_a_reviewed_only(Yes vs No)", ["Story", "Bug"], ["2026-Q1", "2026-Q2", "2026-Q3"], False, denom_not="notempty")

vpden = {}
for label, n in db.execute("SELECT label, count FROM jql_counts WHERE purpose='R8' AND label LIKE 'VP|%'"):
    _, vp, ai, _ = label.split("|")
    vpden[(vp, ai)] = n
for vp in sorted({k[0] for k in vpden}):
    a = db.execute("SELECT count(*) FROM r8_causing WHERE rnd_vp=? AND rq IN ('2026-Q1','2026-Q2','2026-Q3') AND ai='yes'", (vp,)).fetchone()[0]
    b = db.execute("SELECT count(*) FROM r8_causing WHERE rnd_vp=? AND rq IN ('2026-Q1','2026-Q2','2026-Q3') AND ai='not'", (vp,)).fetchone()[0]
    na, nb = vpden[(vp, "yes")], vpden[(vp, "all")] - vpden[(vp, "yes")]
    r, lo, hi = rr(a, na, b, nb)
    rows.append(dict(scope="sens_c_vp:" + vp, types="Story+Bug", quarters="2026-Q1..2026-Q3", source="all", ai_causing=a, ai_resolved=na,
                     non_ai_causing=b, non_ai_resolved=nb, ai_rate_per_1000=round(1000 * a / na, 2), non_ai_rate_per_1000=round(1000 * b / nb, 2),
                     rate_ratio=round(r, 2) if r else "", ci_low=round(lo, 2) if lo else "", ci_high=round(hi, 2) if hi else ""))

ep = dict(db.execute("SELECT label, count FROM jql_counts WHERE purpose='R8' AND label LIKE 'Epic|%'").fetchall())
EPQ = "substr(i.resolved,1,7) BETWEEN '2026-01' AND '2026-09'"
def ep_num(cond):
    return db.execute(f"SELECT count(DISTINCT i.key) FROM causal_links c JOIN issues i ON i.key=c.causing_key WHERE i.issuetype='Epic' AND i.project NOT IN ('CGY','ENG') AND {EPQ} AND {cond}").fetchone()[0]
for scope, b_cond, nb in (("epic_all", "COALESCE(i.ai_implemented,'')<>'Yes'", ep["Epic|all|2026-Q1..Q3"] - ep["Epic|yes|2026-Q1..Q3"]),
                          ("epic_reviewed(Yes vs No)", "i.ai_implemented='No'", ep["Epic|no|2026-Q1..Q3"])):
    a, b, na = ep_num("i.ai_implemented='Yes'"), ep_num(b_cond), ep["Epic|yes|2026-Q1..Q3"]
    r, lo, hi = rr(a, na, b, nb)
    rows.append(dict(scope=scope, types="Epic", quarters="2026-Q1..2026-Q3", source="all", ai_causing=a, ai_resolved=na, non_ai_causing=b, non_ai_resolved=nb,
                     ai_rate_per_1000=round(1000 * a / na, 2), non_ai_rate_per_1000=round(1000 * b / nb, 2),
                     rate_ratio=round(r, 2) if r else "", ci_low=round(lo, 2) if lo else "", ci_high=round(hi, 2) if hi else ""))

out = os.path.join(ROOT, "data", "aggregates", "r8-ai-vs-nonai.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r["scope"], r["types"], r["quarters"], r["source"], r["ai_causing"], "/", r["ai_resolved"], "vs", r["non_ai_causing"], "/", r["non_ai_resolved"],
          "RR", r["rate_ratio"], f"[{r['ci_low']}-{r['ci_high']}]")
print("\nDETECTION (share of fixed CFBs whose RCA names a causing key):")
for vp, fk, n, k in db.execute("SELECT vp, fix_kind, fixed_cfb, names_cause FROM r8_detection ORDER BY fixed_cfb DESC"):
    if n >= 15:
        print(f"  {vp} | {fk} | {k}/{n} = {100*k/n:.0f}%")
tot = db.execute("SELECT fix_kind, sum(fixed_cfb), sum(names_cause) FROM r8_detection GROUP BY 1").fetchall()
print("  total:", [(fk, f"{k}/{n} = {100*k/n:.0f}%") for fk, n, k in tot])
print("\nEXPOSURE (median days causing-item resolved -> CFB created), by AI flag:")
for ai in ("yes", "not"):
    d = sorted(x[0] for x in db.execute("""SELECT julianday(substr(cf.created,1,10)) - julianday(substr(ci.resolved,1,10))
        FROM causal_links c JOIN issues cf ON cf.key=c.cfb_key JOIN issues ci ON ci.key=c.causing_key
        JOIN r8_causing rc ON rc.key=ci.key WHERE rc.ai=? AND rc.rq LIKE '2026%'""", (ai,)) if x[0] is not None)
    if d:
        print(f"  {ai}: n={len(d)} median={d[len(d)//2]:.0f} days")
