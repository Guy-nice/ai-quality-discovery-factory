"""R15: team AI adoption vs change in valid CFB, 2025 vs 2026 (same calendar window Jan 1 - Oct 22).

Jira story denominators per team were not available (Atlassian timeouts on 2026-10-22), so:
- AI adoption proxy = share of the team's 2026 CFBs with AI indicator (cf_15229 = Yes or AI label) = AI used in fix work.
- Outcome = valid CFB count ratio 2026 / 2025 (no workload normalization).
Writes table team_quarter + team_r15, CSV data/aggregates/r15-ai-teams.csv.
"""
import csv, math, os, random, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "r15-ai-teams.csv")
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}
W25, W26 = ("2025-01-01", "2025-10-23"), ("2026-01-01", "2026-10-23")
TOP_N, MIN_CFB_2026 = 40, 8


def quarter(d):
    return f"{d[:4]}-Q{(int(d[5:7]) - 1) // 3 + 1}"


def valid(res):
    return not (res and res.lower() in INVALID)


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def pearson(a, b, w=None):
    w = w or [1] * len(a)
    sw = sum(w)
    ma, mb = sum(x * y for x, y in zip(a, w)) / sw, sum(x * y for x, y in zip(b, w)) / sw
    cov = sum(wi * (x - ma) * (y - mb) for x, y, wi in zip(a, b, w))
    va = sum(wi * (x - ma) ** 2 for x, wi in zip(a, w))
    vb = sum(wi * (y - mb) ** 2 for y, wi in zip(b, w))
    return cov / math.sqrt(va * vb), cov / va


def main():
    db = sqlite3.connect(DB)
    rows = db.execute("SELECT team, created, resolution, priority, ai_implemented, ai_label FROM issues "
                      "WHERE is_cfb = 1 AND created >= '2025-01-01' AND team IS NOT NULL").fetchall()
    tot = {}
    for t, *_ in rows:
        tot[t] = tot.get(t, 0) + 1
    top = sorted(tot, key=lambda t: -tot[t])[:TOP_N]

    db.execute("DROP TABLE IF EXISTS team_quarter")
    db.execute("CREATE TABLE team_quarter (team TEXT, quarter TEXT, stories INTEGER, ai_stories INTEGER, "
               "cfb_all INTEGER, cfb_valid INTEGER, cfb_p12 INTEGER, cfb_ai_fix INTEGER, PRIMARY KEY (team, quarter))")
    tq = {}
    for t, c, res, pr, aii, ail in rows:
        if t not in top:
            continue
        k = (t, quarter(c))
        e = tq.setdefault(k, [0, 0, 0, 0])
        e[0] += 1
        e[1] += valid(res)
        e[2] += pr in ("P1", "P2")
        e[3] += (aii == "Yes" or ail == 1)
    db.executemany("INSERT INTO team_quarter VALUES (?,?,NULL,NULL,?,?,?,?)", [(t, q, *v) for (t, q), v in tq.items()])

    per = []
    for t in top:
        def agg(lo, hi):
            r = [x for x in rows if x[0] == t and lo <= x[1][:10] < hi]
            v = [x for x in r if valid(x[2])]
            return len(r), len(v), sum(1 for x in v if x[3] in ("P1", "P2")), sum(1 for x in r if x[4] == "Yes" or x[5] == 1)
        a25, v25, p25, _ = agg(*W25)
        a26, v26, p26, ai26 = agg(*W26)
        per.append(dict(team=t, cfb_2025=a25, valid_2025=v25, valid_p12_2025=p25, cfb_2026=a26, valid_2026=v26,
                        valid_p12_2026=p26, ai_fix_2026=ai26, ai_share_2026=round(ai26 / a26, 3) if a26 else None))

    ana = [p for p in per if p["cfb_2026"] >= MIN_CFB_2026 and p["valid_2025"] + p["valid_2026"] > 0]
    x = [p["ai_share_2026"] for p in ana]
    y = [math.log((p["valid_2026"] + 0.5) / (p["valid_2025"] + 0.5)) for p in ana]
    w = [p["valid_2025"] + p["valid_2026"] for p in ana]
    rho, _ = pearson(ranks(x), ranks(y))
    _, slope = pearson(x, y, w)

    s = sorted(ana, key=lambda p: p["ai_share_2026"])
    n3 = len(s) // 3
    low, high = s[:n3], s[-n3:]
    for p in per:
        p["tercile"] = "high" if p in high else "low" if p in low else ("mid" if p in ana else "excluded")

    def rr(grp):
        a = sum(p["valid_2026"] for p in grp) + 0.5
        b = sum(p["valid_2025"] for p in grp) + 0.5
        return a / b

    def p12(grp, yr):
        v = sum(p[f"valid_{yr}"] for p in grp)
        return sum(p[f"valid_p12_{yr}"] for p in grp) / v if v else float("nan")

    random.seed(20261022)
    boots = []
    for _ in range(2000):
        bh = [random.choice(high) for _ in high]
        bl = [random.choice(low) for _ in low]
        boots.append(rr(bh) / rr(bl))
    boots.sort()
    ratio = rr(high) / rr(low)
    ci = (boots[49], boots[1949])

    summary = dict(n_teams=len(ana), spearman=round(rho, 2), wls_slope_log_per_unit_share=round(slope, 2),
                   high_ai_share_median=round(sorted(p["ai_share_2026"] for p in high)[n3 // 2], 2),
                   low_ai_share_median=round(sorted(p["ai_share_2026"] for p in low)[n3 // 2], 2),
                   rr_high=round(rr(high), 2), rr_low=round(rr(low), 2), did_ratio=round(ratio, 2),
                   did_ci=(round(ci[0], 2), round(ci[1], 2)),
                   p12_high=(round(p12(high, "2025"), 2), round(p12(high, "2026"), 2)),
                   p12_low=(round(p12(low, "2025"), 2), round(p12(low, "2026"), 2)))

    db.execute("DROP TABLE IF EXISTS team_r15")
    cols = list(per[0])
    db.execute(f"CREATE TABLE team_r15 ({', '.join(cols)})")
    db.executemany(f"INSERT INTO team_r15 VALUES ({','.join('?' * len(cols))})", [tuple(p[c] for c in cols) for p in per])
    db.commit()
    with open(OUT, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        wr.writerows(per)
    print(summary)


if __name__ == "__main__":
    main()
