"""D7 non-recurrence: repeat failures, fix-caused defects, duplicates. Writes repeat_pairs + recurrence_summary.

Run from repo root: python3 -I scripts/db/m2_d7_recurrence.py [threshold]
Summaries are read from raw_local.sqlite (local only); only keys and scores are stored.
"""
import collections
import datetime as dt
import math
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAW = os.path.join(ROOT, "data", "db", "raw_local.sqlite")
MI = re.compile(r"^\s*\[?\s*MI\b|investigatory ki|\bMI[- ]?\d{3,}|major incident", re.I)
INVALID = {"cannot reproduce", "not a bug", "won't do", "duplicate", "won't fix", "works as designed", "invalid"}
STOP = set("""a an the and or of to in on for with without from by at is are was were be been not no when after before
while during into via as it its this that these those can cannot can't does doesn't do don't did didn't has have had
issue issues error errors bug cfb customer customers user users unable working work works fail fails failed failing
incorrect wrong showing shows show displayed display some all any new old getting get gets being""".split())
WINDOW_DAYS = 180


def ts(s):
    return dt.datetime.fromisoformat(s[:19])


def tokens(text):
    words = re.findall(r"[a-z][a-z0-9_]{2,}", (text or "").lower())
    return [w for w in words if w not in STOP and not re.fullmatch(r"[a-z]+\d+", w)]


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round(100 * (c - h) / d, 1), round(100 * (c + h) / d, 1))


def load(db):
    db.execute("ATTACH DATABASE ? AS r", (RAW,))
    rows = db.execute(
        "SELECT i.key, i.created, i.team, i.rnd_vp, i.resolution, f.failure_type, t.summary "
        "FROM issues i JOIN failure_types f ON f.key = i.key LEFT JOIN r.issue_text t ON t.key = i.key "
        "WHERE i.is_cfb = 1 AND i.created >= '2025-01-01'").fetchall()
    out = []
    for key, created, team, vp, res, ftype, summ in rows:
        if res and res.lower() in INVALID:
            continue
        if summ and MI.search(summ):
            continue
        out.append(dict(key=key, created=ts(created), team=team or "(none)", vp=vp or "(none)", ftype=ftype, summ=summ or ""))
    return out


def tfidf(items):
    docs = [collections.Counter(tokens(x["summ"])) for x in items]
    df = collections.Counter(w for d in docs for w in d)
    n = len(docs)
    vecs = []
    for d in docs:
        v = {w: (1 + math.log(c)) * math.log((1 + n) / (1 + df[w])) for w, c in d.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({w: x / norm for w, x in v.items()})
    return vecs


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())


def pairs(items, vecs, threshold):
    found = []
    groups = collections.defaultdict(list)
    for i, x in enumerate(items):
        groups[(x["team"], x["ftype"])].append(i)
    for idx in groups.values():
        idx.sort(key=lambda i: items[i]["created"])
        for a_pos, j in enumerate(idx):
            best = None
            for i in idx[:a_pos]:
                gap = (items[j]["created"] - items[i]["created"]).days
                if gap > WINDOW_DAYS or gap < 0:
                    continue
                s = cos(vecs[i], vecs[j])
                if s >= threshold and (best is None or s > best[1]):
                    best = (i, s, gap)
            if best:
                found.append((items[best[0]]["key"], items[j]["key"], round(best[1], 3), best[2]))
    return found


def main():
    threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    db = sqlite3.connect(DB)
    items = load(db)
    vecs = tfidf(items)
    found = pairs(items, vecs, threshold)
    db.execute("DROP TABLE IF EXISTS repeat_pairs")
    db.execute("CREATE TABLE repeat_pairs (earlier_key TEXT, later_key TEXT, cosine REAL, gap_days INTEGER, threshold REAL, kind TEXT)")
    db.executemany("INSERT INTO repeat_pairs VALUES (?,?,?,?,?,NULL)", [(*p, threshold) for p in found])
    repeat_of = {later: earlier for earlier, later, _, _ in found}
    by_key = {x["key"]: x for x in items}

    # Fair window: each CFB needs 180 days of look-back inside the data (data start 2025-01-01).
    def period(x):
        c = x["created"]
        if dt.datetime(2025, 7, 1) <= c < dt.datetime(2026, 1, 1):
            return "2025-H2"
        if dt.datetime(2026, 1, 1) <= c < dt.datetime(2026, 7, 1):
            return "2026-H1"
        if dt.datetime(2026, 7, 1) <= c < dt.datetime(2026, 10, 23):
            return "2026-Q3+"
        return None

    rows = []
    def add(dim, value, sel):
        for per in ("2025-H2", "2026-H1", "2026-Q3+", "ALL"):
            xs = [x for x in sel if (per == "ALL" and period(x)) or period(x) == per]
            k = sum(1 for x in xs if x["key"] in repeat_of)
            lo, hi = wilson(k, len(xs))
            rows.append(dict(section="repeat", dimension=dim, value=value, period=per, n=len(xs), k=k,
                             rate_pct=round(100 * k / len(xs), 1) if xs else None, ci_low=lo, ci_high=hi))
    add("all", "all", items)
    for vp in sorted({x["vp"] for x in items}):
        add("rnd_vp", vp, [x for x in items if x["vp"] == vp])
    for ft in sorted({x["ftype"] for x in items}):
        add("failure_type", ft, [x for x in items if x["ftype"] == ft])
    team_n = collections.Counter(x["team"] for x in items if period(x))
    for team, n in team_n.most_common(15):
        add("team", team, [x for x in items if x["team"] == team])

    # Fix-caused defects: causing item is a Bug (bug fix) or a CFB.
    cl = db.execute("SELECT c.cfb_key, c.causing_key, i.issuetype, i.is_cfb FROM causal_links c "
                    "LEFT JOIN issues i ON i.key = c.causing_key").fetchall()
    cfb_meta = {k: (c, r) for k, c, r in db.execute("SELECT key, created, resolution FROM issues WHERE is_cfb = 1")}
    by_cfb = collections.defaultdict(list)
    for cfb, causing, itype, iscfb in cl:
        by_cfb[cfb].append((itype, iscfb))
    for yr in ("2025", "2026"):
        keys = [k for k in by_cfb if k in cfb_meta and cfb_meta[k][0][:4] == yr]
        known = [k for k in keys if any(t for t, _ in by_cfb[k])]
        fix = [k for k in known if any(t == "Bug" for t, _ in by_cfb[k])]
        cfbfix = [k for k in known if any(c == 1 for _, c in by_cfb[k])]
        lo, hi = wilson(len(fix), len(known))
        rows.append(dict(section="fix_caused", dimension="causing=Bug", value="cfb_year", period=yr, n=len(known), k=len(fix),
                         rate_pct=round(100 * len(fix) / len(known), 1) if known else None, ci_low=lo, ci_high=hi))
        lo, hi = wilson(len(cfbfix), len(known))
        rows.append(dict(section="fix_caused", dimension="causing=CFB", value="cfb_year", period=yr, n=len(known), k=len(cfbfix),
                         rate_pct=round(100 * len(cfbfix) / len(known), 1) if known else None, ci_low=lo, ci_high=hi))

    # Duplicates: share of all (non-MI) CFBs closed as Duplicate, by half-year.
    db_rows = db.execute("SELECT i.key, i.created, i.resolution, t.summary FROM issues i LEFT JOIN r.issue_text t "
                         "ON t.key = i.key WHERE i.is_cfb = 1 AND i.created >= '2025-01-01'").fetchall()
    halves = collections.defaultdict(lambda: [0, 0])
    for key, created, res, summ in db_rows:
        if summ and MI.search(summ):
            continue
        h = created[:4] + ("-H1" if created[5:7] <= "06" else "-H2")
        halves[h][0] += 1
        halves[h][1] += (res or "").lower() == "duplicate"
    for h, (n, k) in sorted(halves.items()):
        lo, hi = wilson(k, n)
        rows.append(dict(section="duplicate", dimension="resolution=Duplicate", value="all_nonMI_cfb", period=h, n=n, k=k,
                         rate_pct=round(100 * k / n, 1), ci_low=lo, ci_high=hi))

    # Prevention action of the earlier CFB vs later repeat (correlation only).
    prev = {}
    for key, ptype in db.execute("SELECT key, prevention_action_type FROM rca_class WHERE round IN ('R5-round1','R9')"):
        prev.setdefault(key, ptype)
    earlier_keys = {e for e, _, _, _ in found}
    cutoff = dt.datetime(2026, 10, 22) - dt.timedelta(days=WINDOW_DAYS)
    for ptype in sorted(set(prev.values())):
        ks = [k for k, p in prev.items() if p == ptype and k in by_key and by_key[k]["created"] <= cutoff]
        k = sum(1 for x in ks if x in earlier_keys)
        lo, hi = wilson(k, len(ks))
        rows.append(dict(section="prevention", dimension="earlier_prevention", value=ptype, period="followed 180d", n=len(ks), k=k,
                         rate_pct=round(100 * k / len(ks), 1) if ks else None, ci_low=lo, ci_high=hi))

    # Recurred after fix: earlier CFB resolved Fixed before the later one was created; else parallel report of an open defect.
    meta = {k: (r, res) for k, r, res in db.execute("SELECT key, resolved, resolution FROM issues WHERE is_cfb = 1")}
    kinds = collections.Counter()
    for e, l, _, _ in found:
        er, eres = meta.get(e, (None, None))
        after_fix = bool(er and (eres or "").lower().startswith("fixed") and ts(er) <= by_key[l]["created"])
        kinds["after_fix" if after_fix else "parallel_or_open"] += 1
        db.execute("UPDATE repeat_pairs SET kind = ? WHERE earlier_key = ? AND later_key = ?",
                   ("after_fix" if after_fix else "parallel_or_open", e, l))
    for kind, k in kinds.items():
        rows.append(dict(section="repeat_kind", dimension="kind", value=kind, period="ALL pairs", n=len(found), k=k,
                         rate_pct=round(100 * k / len(found), 1) if found else None, ci_low=None, ci_high=None))
    for per in ("2025-H2", "2026-H1", "2026-Q3+"):
        xs = [x for x in items if period(x) == per]
        k = 0
        for x in xs:
            e = repeat_of.get(x["key"])
            if e:
                er, eres = meta.get(e, (None, None))
                k += bool(er and (eres or "").lower().startswith("fixed") and ts(er) <= x["created"])
        lo, hi = wilson(k, len(xs))
        rows.append(dict(section="repeat_after_fix", dimension="all", value="all", period=per, n=len(xs), k=k,
                         rate_pct=round(100 * k / len(xs), 1) if xs else None, ci_low=lo, ci_high=hi))

    db.execute("DROP TABLE IF EXISTS recurrence_summary")
    cols = list(rows[0])
    db.execute(f"CREATE TABLE recurrence_summary ({', '.join(cols)})")
    db.executemany(f"INSERT INTO recurrence_summary VALUES ({','.join('?' * len(cols))})", [tuple(r[c] for c in cols) for r in rows])
    db.commit()
    out = os.path.join(ROOT, "data", "aggregates", "m2-d7-recurrence.csv")
    with open(out, "w") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join('"%s"' % str(r[c]).replace('"', "'") if r[c] is not None else "" for c in cols) + "\n")
    print(f"items={len(items)} pairs={len(found)} threshold={threshold}")


if __name__ == "__main__":
    main()
