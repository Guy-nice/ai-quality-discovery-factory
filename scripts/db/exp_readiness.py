"""Experiment readiness for X1-X5 (quality-model-v0.md section 6).

Writes table exp_team_archetype (quality.sqlite) and data/aggregates/exp-readiness.csv.
Then load: python3 -I scripts/db/load.py csv data/aggregates/exp-readiness.csv agg_exp_readiness
Needs raw_local.sqlite (MI exclusion). Run from repo root: python3 -I scripts/db/exp_readiness.py
Assumptions: target effect = 30% relative; 1 quarter = 3 months; rates from 2026 Jan-Oct (10 months).
"""
import csv
import math
import os
import re
import sqlite3
import statistics as st
from statistics import NormalDist

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "exp-readiness.csv")
MI = re.compile(r"^\s*\[?\s*MI\b|investigatory ki|\bMI[- ]?\d{3,}|major incident", re.I)
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}
GAP = {"works as designed", "not a bug", "limitation"}
ZA, ZB = NormalDist().inv_cdf(0.975), NormalDist().inv_cdf(0.8)
TARGET = 0.30
MAXQ = 12
X1_GOAL = 0.8  # X1 target: fields present in 80% of valid CFBs (relative change = 0.8/baseline - 1)
MONTHS = 10  # 2026 Jan-Oct
MINVOL = 20  # min valid CFBs to rank a team (X2: half)


def mde_prop(p, n, up):
    """Min relative change in a rate p detectable with n units per arm (two-proportion, 80% power)."""
    if p <= 0 or n <= 0:
        return None
    lo, hi = 0.0, (1 / p - 1 if up else 1.0)
    if hi <= 0:
        return None

    def ok(r):
        p1 = p * (1 + r if up else 1 - r)
        pb = (p + p1) / 2
        need = ZA * math.sqrt(2 * pb * (1 - pb) / n) + ZB * math.sqrt((p * (1 - p) + p1 * (1 - p1)) / n)
        return abs(p1 - p) >= need
    if not ok(hi - 1e-9):
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if ok(mid) else (mid, hi)
    return hi


def mde_pois(mu, up):
    """Min relative change in a count (mean mu per arm-period), equal exposure, sqrt approximation."""
    if mu <= 0:
        return None
    d = (ZA + ZB) * math.sqrt(0.5) / math.sqrt(mu)
    if up:
        return (d + 1) ** 2 - 1
    return 1 - (1 - d) ** 2 if d < 1 else None


def quarters(kind, p, n1q, up, target=TARGET):
    for k in range(1, MAXQ + 1):
        m = mde_prop(p, n1q * k, up) if kind == "prop" else mde_pois(p * k, up)
        if m is not None and m <= target:
            return k
    return f">{MAXQ}"


def main():
    db = sqlite3.connect(DB)
    db.execute("ATTACH DATABASE ? AS r", (os.path.join(ROOT, "data", "db", "raw_local.sqlite"),))

    # ---- archetypes
    prof = {row[0]: (row[0], row[1], *map(float, row[2:])) for row in db.execute(
        "SELECT team, rnd_vp, valid_2025_janoct, valid_2026_janoct, p12_share_valid_pct, incidents_per_cfb, invalid_pct "
        "FROM agg_m2_team_profiles")}
    med_p = st.median(v[4] for v in prof.values())
    med_i = st.median(v[5] for v in prof.values())
    arch = {}
    for t, (_, vp, v25, v26, p12, inc, inv) in prof.items():
        growth = (v26 - v25) / v25 * 100 if v25 else None  # undefined growth (no 2025 base) is not B, as in m2_teams.py
        if p12 >= med_p and inc >= med_i:
            a = "A"
        elif growth is not None and growth >= 50:
            a = "B"
        elif inv >= 50:
            a = "C"
        else:
            a = "D"
        arch[t] = a
    db.execute("DROP TABLE IF EXISTS exp_team_archetype")
    db.execute("CREATE TABLE exp_team_archetype (team, rnd_vp, archetype, valid_2025_janoct, valid_2026_janoct, "
               "valid_change_pct, p12_share_valid_pct, incidents_per_cfb, invalid_pct, median_p12, median_incidents)")
    for t, a in arch.items():
        _, vp, v25, v26, p12, inc, inv = prof[t]
        db.execute("INSERT INTO exp_team_archetype VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                   (t, vp, a, v25, v26, round((v26 - v25) / v25 * 100, 1) if v25 else None, p12, inc, inv, med_p, med_i))

    db.commit()

    # ---- issue sets
    ftype = {k: f for k, f in db.execute("SELECT key, failure_type FROM failure_types")}
    cause = {c for (c,) in db.execute("SELECT DISTINCT cfb_key FROM causal_links")}
    fixcaused = {c for (c,) in db.execute(
        "SELECT DISTINCT l.cfb_key FROM causal_links l JOIN issues i ON i.key=l.causing_key WHERE i.issuetype='Bug'")}
    allc, valid = [], []
    for key, created, resolved, res, pr, team, summ in db.execute(
            "SELECT i.key, i.created, i.resolved, i.resolution, i.priority, i.team, t.summary FROM issues i "
            "LEFT JOIN r.issue_text t ON t.key=i.key WHERE i.is_cfb=1 AND i.team IS NOT NULL"):
        if summ and MI.search(summ):
            continue
        d = dict(key=key, c=created[:7], r=(resolved or "")[:7], res=(res or "").lower(), p12=pr in ("P1", "P2"), team=team)
        allc.append(d)
        if d["res"] not in INVALID:
            valid.append(d)
    teams = sorted(prof)
    by = lambda rows, t: [x for x in rows if x["team"] == t]
    v26 = lambda t: [x for x in by(valid, t) if x["c"] >= "2026-01"]

    # ---- matching
    vols = {t: math.log(prof[t][3] + 1) for t in teams}
    sd_v = st.pstdev(vols.values()) or 1
    sd_p = st.pstdev(prof[t][4] for t in teams) or 1

    def dist(a, b):
        return (abs(vols[a] - vols[b]) / sd_v + abs(prof[a][4] - prof[b][4]) / sd_p
                + (0 if prof[a][1] == prof[b][1] else 0.5))

    used = set()

    def control(t, same_arch=True, need=None):
        pool = [c for c in teams if c not in used and c != t and (arch[c] == arch[t] or not same_arch)
                and len(v26(c)) > 0 and (need is None or need(c))]
        if not pool:
            return None
        return min(pool, key=lambda c: dist(t, c))

    # ---- candidates (non-overlapping; picked in order X2, X5, X3, X4, X1)
    sel = {}
    typ = lambda t: [x for x in v26(t) if ftype.get(x["key"]) in ("ROUTING", "LIFECYCLE", "AGENTSTATE")]
    A = [t for t in teams if arch[t] == "A" and len(v26(t)) >= MINVOL // 2]
    x2 = max(A, key=lambda t: len(typ(t)) / len(v26(t)))
    sel["X2"] = [x2]
    used.add(x2)
    Cs = [t for t in teams if arch[t] == "C" and len(by(allc, t)) >= MINVOL]
    gapshare = lambda t: sum(x["res"] in GAP for x in by(allc, t)) / len(by(allc, t))
    x5 = max(Cs, key=gapshare)
    sel["X5"] = [x5]
    used.add(x5)

    hot = {}
    for t, n in db.execute("SELECT team, SUM(hotspot) FROM ai_matched WHERE team IS NOT NULL GROUP BY team"):
        hot[t] = n
    x3 = [t for t in sorted(hot, key=hot.get, reverse=True) if t in prof and t not in used][:2]
    sel["X3"] = x3
    used.update(x3)
    fx = lambda t: len([x for x in by(valid, t) if x["key"] in fixcaused]) / max(1, len(by(valid, t)))
    pool4 = [t for t in teams if t not in used and len(by(valid, t)) >= MINVOL]
    x4 = sorted(pool4, key=fx, reverse=True)[:2]
    sel["X4"] = x4
    used.update(x4)
    x1 = []
    for a in "ABC":
        pool = [t for t in teams if arch[t] == a and t not in used and len(v26(t)) > 0]
        pick = max(pool, key=lambda t: len(v26(t)))
        x1.append(pick)
        used.add(pick)
    sel["X1"] = x1

    ctrl = {}
    for e in ("X1", "X3", "X4"):
        ctrl[e] = []
        for t in sel[e]:
            need = (lambda c: hot.get(c, 0) >= 10) if e == "X3" else None
            c = control(t, True, need) or (control(t, False, need) if e == "X3" else None)
            ctrl[e].append(c)
            if c:
                used.add(c)

    rows = []

    def add(e, arm, team, metric, base, n1q, kind, up, target=TARGET):
        m = mde_prop(base, n1q, up) if kind == "prop" else mde_pois(base, up)
        rows.append(dict(experiment=e, arm=arm, team=team, archetype=arch.get(team, ""), metric=metric,
                         baseline=round(base, 4), n_per_quarter=round(n1q, 1),
                         mde_pct=round(m * 100, 1) if m is not None else "not detectable",
                         quarters_needed=quarters(kind, base, n1q, up, target)))

    def pooled(e, arm, ts, metric, num, den, n_of, up):
        a = sum(num(t) for t in ts)
        b = sum(den(t) for t in ts)
        n = sum(n_of(t) for t in ts)
        if b:
            add(e, arm, "POOLED:" + "|".join(ts), metric, a / b, n, "prop", up,
                X1_GOAL / (a / b) - 1 if e == "X1" and a else TARGET)

    q = lambda n: n * 3 / MONTHS  # 2026 Jan-Oct -> per quarter
    # X1
    for arm, ts in (("candidate", sel["X1"]), ("control", [c for c in ctrl["X1"] if c])):
        for t in ts:
            n = len(v26(t))
            for mname, f in (("share valid CFB with causing key", lambda x: x["key"] in cause),
                             ("share valid CFB with failure_type", lambda x: x["key"] in ftype)):
                b = sum(f(x) for x in v26(t)) / n
                add("X1", arm, t, mname, b, q(n), "prop", True, X1_GOAL / b - 1 if b else TARGET)
        for mname, f in (("share valid CFB with causing key", lambda x: x["key"] in cause),
                         ("share valid CFB with failure_type", lambda x: x["key"] in ftype)):
            pooled("X1", arm, ts, mname, lambda t: sum(f(x) for x in v26(t)), lambda t: len(v26(t)),
                   lambda t: q(len(v26(t))), True)
    # X2 (same team pre vs post; reduction of escaped CFBs of the type)
    t = x2
    ty = typ(t)
    add("X2", "candidate (pre vs post)", t, "monthly valid CFB of ROUTING/LIFECYCLE/AGENTSTATE",
        len(ty) / MONTHS, 3 * len(ty) / MONTHS, "pois", False)
    rows[-1]["quarters_needed"] = quarters("pois", len(ty) / MONTHS * 3, 0, False)
    add("X2", "candidate (pre vs post)", t, "P1/P2 share of those CFBs", sum(x["p12"] for x in ty) / len(ty),
        3 * len(ty) / MONTHS, "prop", False)
    # X3
    for arm, ts in (("candidate", sel["X3"]), ("control", [c for c in ctrl["X3"] if c])):
        def pr(t):
            return db.execute("SELECT COUNT(*), SUM(f90) FROM ai_matched WHERE team=? AND hotspot=1 AND f90 IS NOT NULL", (t,)).fetchone()
        def nq(t):
            n = db.execute("SELECT COUNT(*) FROM ai_matched WHERE team=? AND hotspot=1 AND month>='2026-01'", (t,)).fetchone()[0]
            return q(n)
        for t in ts:
            n, f = pr(t)
            if n:
                add("X3", arm, t, "90-day follow-up fix rate per hotspot PR", (f or 0) / n, nq(t), "prop", False)
        pooled("X3", arm, ts, "90-day follow-up fix rate per hotspot PR", lambda t: pr(t)[1] or 0, lambda t: pr(t)[0], nq, False)
    # X4
    for arm, ts in (("candidate", sel["X4"]), ("control", [c for c in ctrl["X4"] if c])):
        for t in ts:
            add("X4", arm, t, "fix-caused share of valid CFBs", fx(t), q(len(v26(t))), "prop", False)
        pooled("X4", arm, ts, "fix-caused share of valid CFBs",
               lambda t: sum(x["key"] in fixcaused for x in by(valid, t)), lambda t: len(by(valid, t)),
               lambda t: q(len(v26(t))), False)
    # X5
    t = x5
    gm = [x for x in by(allc, t) if x["res"] in GAP and x["r"] >= "2025-01"]
    m5 = 22  # 2025-01..2026-10: 2026 alone is too thin
    add("X5", "candidate (pre vs post)", t, "monthly WAD/not-a-bug/limitation closures (2025-01..2026-10)",
        len(gm) / m5, 3 * len(gm) / m5, "pois", False)
    rows[-1]["quarters_needed"] = quarters("pois", len(gm) / m5 * 3, 0, False)

    # fix Poisson baseline units: baseline = monthly count; mde uses quarterly mean
    for rw in rows:
        if rw["experiment"] in ("X2", "X5") and rw["metric"].startswith("monthly"):
            m = mde_pois(rw["n_per_quarter"], False)
            rw["mde_pct"] = round(m * 100, 1) if m is not None else "not detectable"

    cols = ["experiment", "arm", "team", "archetype", "metric", "baseline", "n_per_quarter", "mde_pct", "quarters_needed"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    db.commit()
    print("medians p12/inc", med_p, med_i, {a: sum(v == a for v in arch.values()) for a in "ABCD"})
    for e, ts in sel.items():
        print(e, ts, ctrl.get(e))
    for rw in rows:
        print(*[rw[c] for c in cols], sep=" | ")


main()
