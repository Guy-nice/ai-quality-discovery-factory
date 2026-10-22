"""Extract causing Jira keys for fixed CFBs into causal_links.

Sources:
  rca_text  - keys in the RCA "How was it introduced" section (raw_local.sqlite).
  issuelink - Jira links whose type name suggests causation.
Usage: python3 -I scripts/db/extract_causes.py [--sample N]  (sample prints sections for precision check)
"""
import datetime, os, random, re, sqlite3, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"), timeout=60)
raw = sqlite3.connect(os.path.join(ROOT, "data", "db", "raw_local.sqlite"), timeout=60)

KEY = re.compile(r"\b([A-Z][A-Z0-9]{1,14}-\d{1,7})\b")
START = re.compile(r"How was it introduced\??", re.I)
NEXT = re.compile(r"How was it fixed|Long-term|Is there an opportunity|What will be done|What will different", re.I)
TEMPLATE = "Indicate JIRA item which caused this issue"
CAUSE_LINKS = {("Problem/Incident", "inward"): "issuelink:is_caused_by", ("Defect", "inward"): "issuelink:created_by"}


def section(text):
    m = START.search(text or "")
    if not m:
        return None
    rest = text[m.end():]
    n = NEXT.search(rest)
    s = rest[: n.start()] if n else rest[:600]
    return s.replace(TEMPLATE, "")


def main():
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    fixed = [r[0] for r in db.execute("SELECT key FROM issues WHERE is_cfb=1 AND resolution='Fixed'")]
    texts = dict(raw.execute("SELECT key, rca FROM issue_text"))
    db.execute("DELETE FROM causal_links WHERE extracted_by='extract_causes.py'")
    n_sec = n_key = 0
    sections = {}
    for k in fixed:
        s = section(texts.get(k))
        if s is None:
            continue
        n_sec += 1
        keys = [x for x in dict.fromkeys(KEY.findall(s)) if x != k and not x.startswith(("MI-", "SS0"))]
        if keys:
            n_key += 1
            sections[k] = (s, keys)
        for c in keys:
            db.execute("INSERT OR IGNORE INTO causal_links VALUES (?,?,?,?,?)", (k, c, "rca_text", "extract_causes.py", ts))
    n_link = 0
    for k, t, d, o in db.execute("SELECT l.key, l.link_type, l.direction, l.other_key FROM issue_links l JOIN issues i ON i.key=l.key WHERE i.is_cfb=1 AND i.resolution='Fixed'").fetchall():
        src = CAUSE_LINKS.get((t, d))
        if src:
            n_link += 1
            db.execute("INSERT OR IGNORE INTO causal_links VALUES (?,?,?,?,?)", (k, o, src, "extract_causes.py", ts))
    db.commit()
    print(f"fixed CFB={len(fixed)} with_section={n_sec} with_key_in_section={n_key} cause_links={n_link}")
    print("causal_links rows:", db.execute("SELECT count(*) FROM causal_links").fetchone()[0])
    print("link types seen:", db.execute("SELECT link_type, count(*) FROM issue_links GROUP BY 1 ORDER BY 2 DESC").fetchall()[:15])
    if "--sample" in sys.argv:
        random.seed(8)
        for k in random.sample(sorted(sections), int(sys.argv[sys.argv.index("--sample") + 1])):
            s, keys = sections[k]
            print(f"\n== {k} -> {keys}\n{re.sub(r'\s+', ' ', s)[:300]}")


if __name__ == "__main__":
    main()
