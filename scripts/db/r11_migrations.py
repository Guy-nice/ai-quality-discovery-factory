"""R11: migration events, migration mentions in pilot CFBs, monthly series, event study. Run: python3 -I scripts/db/r11_migrations.py"""
import csv, math, os, re, sqlite3, datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"))
db.execute(f"ATTACH '{os.path.join(ROOT, 'data', 'db', 'raw_local.sqlite')}' AS r")
AGG = os.path.join(ROOT, "data", "aggregates")

# Events: from Git only (Atlassian unavailable 2026-10-22). Code dates, not production rollout dates.
EVENTS = [
    ("E01", "VFM->AFM", "AFM repo created", "2022-03-28", "code_start", "-", "git", "inContact/routing-ng-advanced-findmatch created_at", "High (code), Low (rollout)"),
    ("E02", "Voltron / cache", "MessagePack serializer work starts in VCSvc", "2026-01-15", "code_start", "-", "git", "inContact/inContact commits 'MessagePack' 2026-01..05 (14)", "Medium (code)"),
    ("E03", ".NET upgrade", "net10 / multi-TFM work starts in monolith", "2026-03-15", "code_start", "-", "git", "inContact/inContact commits 'net10' 2026-03..10 (22)", "Medium (code)"),
    ("E04", "TFS telephony", "media-services-telephony-feature-service repo created", "2026-04-08", "code_start", "-", "git", "inContact/media-services-telephony-feature-service created_at", "High (code)"),
    ("E05", "Voltron / cache", "voltron-agent repo created", "2026-04-28", "code_start", "-", "git", "inContact/voltron-agent created_at", "High (code)"),
    ("E06", "State Streams KDA->EKS", "EKS transformer repos created", "2026-05-06", "code_start", "-", "git", "inContact/orch-entity-state-streams-eks, -multi-event-eks created_at", "High (code)"),
    ("E07", "State Streams KDA->EKS", "Rollback plan EKS->KDA published", "2026-10-16", "doc", "-", "confluence", "IN 4256694278 (last modified)", "Low (doc date only)"),
    ("E08", "Voltron / cache", "Voltron build status tracker active, per-cluster schedule", "2026-10-21", "doc", "per cluster", "confluence", "CXONE 4232414340 (last modified)", "Low (doc date only)"),
    ("E09", "Tenant moves", "Tenant migration impact assessment (AOR team)", "2026-10-16", "doc", "tenant", "confluence", "IN 4228809169 (last modified)", "Low (doc date only)"),
]

PATTERNS = {
    "VFM->AFM": r"\bAFM\b|advanced ?find ?match|\bVFM\b|app-findmatch|afmEnabled",
    "Voltron / cache": r"voltron|decoupl|cache conversion|\bncache\b|messagepack",
    "State Streams KDA->EKS": r"\bEKS\b|\bKDA\b|state[- ]?streams?",
    ".NET upgrade": r"\.net ?(core|[5-9]|10)\b|\bnet(48|8|10|standard)|multi-tfm|framework upgrade|newtonsoft|runtime upgrade",
    "Tenant moves": r"tenant (migration|move)|cluster (migration|move)|moved (to|from) (another |a new )?cluster|\bBU (migration|move)",
    "TFS telephony": r"telephony feature service|\bTFS service\b",
}
INVALID = ("Not a bug", "Duplicate", "Works as Designed", "Cannot Reproduce", "Won't Fix", "Removed", "Limitation")


def month(s):
    return s[:7]


def rr_ci(a, b):
    if a == 0 or b == 0:
        return (None, None, None)
    rr = a / b
    se = math.sqrt(1 / a + 1 / b)
    return (round(rr, 2), round(rr * math.exp(-1.96 * se), 2), round(rr * math.exp(1.96 * se), 2))


def main():
    db.execute("DROP TABLE IF EXISTS migration_events")
    db.execute("CREATE TABLE migration_events (event_id TEXT PRIMARY KEY, migration TEXT, step TEXT, date TEXT, date_type TEXT, scope TEXT, source_kind TEXT, source_ref TEXT, confidence TEXT)")
    db.executemany("INSERT INTO migration_events VALUES (?,?,?,?,?,?,?,?,?)", EVENTS)

    pilot = db.execute("""SELECT i.key, i.created, i.priority, i.resolution, f.sub_flow, f.in_flow_scope, coalesce(t.summary,''), coalesce(t.rca,'')
        FROM issues i LEFT JOIN flow_tags f ON f.key=i.key LEFT JOIN r.issue_text t ON t.key=i.key
        WHERE i.is_cfb=1 AND i.rnd_vp='Orchestration Core' AND i.created >= '2024-10-22'""").fetchall()

    db.execute("DROP TABLE IF EXISTS migration_mentions")
    db.execute("CREATE TABLE migration_mentions (key TEXT, migration TEXT, field TEXT, PRIMARY KEY (key, migration, field))")
    tagged = {}
    for k, cr, pr, res, sf, inflow, summ, rca in pilot:
        for mig, pat in PATTERNS.items():
            for field, txt in (("summary", summ), ("rca", rca)):
                if re.search(pat, txt, re.I):
                    db.execute("INSERT OR IGNORE INTO migration_mentions VALUES (?,?,?)", (k, mig, field))
                    tagged.setdefault(k, set()).add(mig)
    db.commit()

    # Monthly series
    months = {}
    for k, cr, pr, res, sf, inflow, summ, rca in pilot:
        m = month(cr)
        d = months.setdefault(m, dict(month=m, cfb=0, valid=0, p12=0, in_flow=0, mig_any=0, mig_valid=0))
        d["cfb"] += 1
        valid = res not in INVALID
        d["valid"] += valid
        d["p12"] += pr in ("P1", "P2")
        d["in_flow"] += 1 if str(inflow) in ("1", "True", "yes", "in") else 0
        d["mig_any"] += k in tagged
        d["mig_valid"] += (k in tagged) and valid
    with open(os.path.join(AGG, "r11-pilot-monthly.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(next(iter(months.values()))))
        w.writeheader()
        w.writerows([months[m] for m in sorted(months)])

    # Window comparison
    def win(lo, hi):
        rows = [p for p in pilot if lo <= p[1][:10] < hi]
        return len(rows), sum(1 for p in rows if p[0] in tagged), {m: sum(1 for p in rows if m in tagged.get(p[0], ())) for m in PATTERNS}
    prev = win("2024-10-22", "2025-10-22")
    last = win("2025-10-22", "2026-10-23")

    # Event study: 8 weeks before vs after, pilot vs control (other VPs, CFBs 2025+)
    control = db.execute("SELECT created FROM issues WHERE is_cfb=1 AND coalesce(rnd_vp,'')<>'Orchestration Core' AND created >= '2025-01-01'").fetchall()
    out = []
    for e in EVENTS:
        if e[4] != "code_start" or e[3] < "2025-03-01":
            continue
        d0 = dt.date.fromisoformat(e[3])
        b0, a1 = (d0 - dt.timedelta(weeks=8)).isoformat(), (d0 + dt.timedelta(weeks=8)).isoformat()
        if a1 > "2026-10-22":
            continue
        def cnt(rows, lo, hi, pred=lambda r: True):
            return sum(1 for r in rows if lo <= r[1][:10] < hi and pred(r))
        pb = cnt(pilot, b0, e[3]); pa = cnt(pilot, e[3], a1)
        mb = cnt(pilot, b0, e[3], lambda r: e[1] in tagged.get(r[0], ())); ma = cnt(pilot, e[3], a1, lambda r: e[1] in tagged.get(r[0], ()))
        cb = sum(1 for (c,) in control if b0 <= c[:10] < e[3]); ca = sum(1 for (c,) in control if e[3] <= c[:10] < a1)
        rp, rc = rr_ci(pa, pb), rr_ci(ca, cb)
        ratio = round((pa / pb) / (ca / cb), 2) if pb and cb and ca else None
        out.append(dict(event_id=e[0], migration=e[1], date=e[3], pilot_before=pb, pilot_after=pa, pilot_rr=rp[0], pilot_lo=rp[1], pilot_hi=rp[2],
                        mention_before=mb, mention_after=ma, control_before=cb, control_after=ca, control_rr=rc[0], pilot_vs_control=ratio))
    with open(os.path.join(AGG, "r11-event-study.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader(); w.writerows(out)
    with open(os.path.join(AGG, "r11-migration-events.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["event_id", "migration", "step", "date", "date_type", "scope", "source_kind", "source_ref", "confidence"]); w.writerows(EVENTS)

    # RCA classes vs migration mention
    rca = db.execute("SELECT key, escape_cause, introduced_by FROM rca_class WHERE round='R9'").fetchall()
    rc_m = [r for r in rca if r[0] in tagged]
    print("pilot CFBs", len(pilot), "with migration mention", len(tagged))
    print("W_prev", prev[0], "mention", prev[1], prev[2])
    print("W_last", last[0], "mention", last[1], last[2])
    print("growth total", last[0] - prev[0], "growth mention", last[1] - prev[1])
    print("R9 RCAs", len(rca), "with mention", len(rc_m))
    from collections import Counter
    print("escape cause (mention)", Counter(r[1] for r in rc_m).most_common())
    print("introduced_by (mention)", Counter(r[2] for r in rc_m).most_common())
    print("introduced_by (no mention)", Counter(r[2] for r in rca if r[0] not in tagged).most_common())
    for o in out: print(o)


if __name__ == "__main__":
    main()


# Manual judgments (R11 rater, 2026-10-22): is the causing change a migration step? Read from RCA "How was it introduced".
JUDGED = {
    "SCRX-1394": ("yes", "Voltron / cache", "MessagePack added to ScriptHelper for NCache serialization change"),
    "API-21156": ("yes", ".NET upgrade", "System.Web removed for netstandard2.0"),
    "API-21286": ("yes", ".NET upgrade", "JSON handling change in 26.1 (library swap)"),
    "API-21358": ("yes", ".NET upgrade", "JavaScriptSerializer -> Newtonsoft conversion"),
    "EM-158368": ("yes", "State Streams KDA->EKS", "state-streams-common upgrade of flink-connector-kinesis"),
    "EM-158691": ("yes", "State Streams KDA->EKS", "Kinesis connector change exposed restart-loop bug"),
    "AOR-13252": ("yes", "Tenant moves", "Bulk BU move between AFM and VFM without backlog clear"),
    "AOR-14448": ("yes", "VFM->AFM", "DB migration script after AFM pod count change"),
    "AOR-16073": ("yes", "VFM->AFM", "Manual move of customers VFM -> AFM during MI restore"),
    "API-22840": ("yes", ".NET upgrade", "Missing DLLs after dependency changes by 2 teams"),
    "API-22976": ("partial", ".NET upgrade", "dynamicjson serialization regression"),
}


def judged():
    db.execute("DROP TABLE IF EXISTS migration_causal")
    db.execute("CREATE TABLE migration_causal (key TEXT PRIMARY KEY, judgment TEXT, migration TEXT, note TEXT, rater TEXT)")
    tagged_last = [k for (k,) in db.execute("SELECT DISTINCT mm.key FROM migration_mentions mm JOIN issues i ON i.key=mm.key WHERE i.created >= '2025-10-22'")]
    for k in tagged_last:
        j = JUDGED.get(k, ("no", "", "component mentioned; latent, infra or feature change"))
        db.execute("INSERT INTO migration_causal VALUES (?,?,?,?,?)", (k, *j, "claude-fork-r11"))
    db.commit()
    print("judged", len(tagged_last), db.execute("SELECT judgment, count(*) FROM migration_causal GROUP BY 1").fetchall())


if __name__ == "__main__":
    judged()
