"""Load Atlassian MCP Jira JSON dumps into quality.sqlite (structured) and raw_local.sqlite (text, gitignored).

Usage:
  python3 -I scripts/db/load.py dump <file.json> --purpose R8 --jql "..."
  python3 -I scripts/db/load.py count --purpose R8 --label "2026-Q1 ai stories" --jql "..." --count 123
  python3 -I scripts/db/load.py csv <file.csv> <table>
"""
import argparse, csv, datetime, json, os, re, sqlite3, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAW = os.path.join(ROOT, "data", "db", "raw_local.sqlite")
SCHEMA = os.path.join(ROOT, "scripts", "db", "schema.sql")

RCA_MARKERS = ["Describe functional impact of the issue", "Describe technical reason for the issue",
               "Indicate the root cause for the issue", "Indicate JIRA item which caused this issue",
               "Indicate how the issue was fixed"]
RIA_MARKERS = ["Describe functionality or issue to be fixed", "Identify specific components, files, libraries",
               "Identify and document impact areas", "Identify and document specific tests"]
AI_LABEL = re.compile(r"(AGENTIC|AGENT_AI|AI[-_]|_AI|copilot|claude|cursor|UseAIAgent)", re.I)


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def connect():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    db = sqlite3.connect(DB, timeout=60)
    db.executescript(open(SCHEMA).read())
    raw = sqlite3.connect(RAW, timeout=60)
    raw.execute("CREATE TABLE IF NOT EXISTS issue_text (key TEXT PRIMARY KEY, summary TEXT, rca TEXT, ria TEXT, pulled_at TEXT)")
    return db, raw


def as_text(v):
    if v is None or isinstance(v, str):
        return v
    out = []
    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "text":
                out.append(n.get("text", ""))
            for c in n.get("content", []) or []:
                walk(c)
            if n.get("type") in ("paragraph", "heading", "listItem"):
                out.append("\n")
        elif isinstance(n, list):
            for c in n:
                walk(c)
    walk(v)
    return "".join(out)


def text_state(t, markers, template_max):
    t = as_text(t) or ""
    if not t.strip():
        return "empty"
    hits = sum(m in t for m in markers)
    if hits >= len(markers) - 1 and len(t) < template_max:
        return "template"
    return "filled"


def opt(v):
    if isinstance(v, dict):
        return v.get("value") or v.get("name")
    if isinstance(v, list):
        return ",".join(str(opt(x)) for x in v) if v else None
    return v


def nodes_of(doc):
    if "issues" in doc and isinstance(doc["issues"], dict):
        return doc["issues"].get("nodes", [])
    if "issues" in doc and isinstance(doc["issues"], list):
        return doc["issues"]
    if "key" in doc and "fields" in doc:
        return [doc]
    return []


def load_dump(path, purpose, jql, cfb=False):
    db, raw = connect()
    doc = json.load(open(path))
    ts, n = now(), 0
    for node in nodes_of(doc):
        k, f = node["key"], node.get("fields", {})
        labels = f.get("labels")
        cols = {
            "project": (f.get("project") or {}).get("key") if "project" in f else k.split("-")[0],
            "issuetype": opt(f.get("issuetype")) if "issuetype" in f else None,
            "created": f.get("created"), "resolved": f.get("resolutiondate"),
            "status": opt(f.get("status")) if "status" in f else None,
            "status_category": ((f.get("status") or {}).get("statusCategory") or {}).get("key") if "status" in f else None,
            "resolution": opt(f.get("resolution")) if "resolution" in f else None,
            "priority": opt(f.get("priority")) if "priority" in f else None,
            "rnd_vp": opt(f.get("customfield_14852")) if "customfield_14852" in f else None,
            "team": opt(f.get("customfield_10098")) if "customfield_10098" in f else None,
            "bug_type": opt(f.get("customfield_10104")) if "customfield_10104" in f else None,
            "incidents": f.get("customfield_10068"),
            "impact_rank": f.get("customfield_10081"),
            "sf_association_count": f.get("customfield_10036"),
            "ai_implemented": opt(f.get("customfield_15229")) if "customfield_15229" in f else None,
            "labels": json.dumps(labels) if labels is not None else None,
            "ai_label": (1 if any(AI_LABEL.search(l) for l in labels) else 0) if labels is not None else None,
            "rca_state": text_state(f.get("customfield_10117"), RCA_MARKERS, 1100) if "customfield_10117" in f else None,
            "ria_state": text_state(f.get("customfield_12794"), RIA_MARKERS, 1300) if "customfield_12794" in f else None,
        }
        if cfb:
            cols["is_cfb"] = 1
        elif "customfield_10036" in f:
            cols["is_cfb"] = 1 if (f.get("customfield_10036") or 0) > 0 else 0
        present = {c: v for c, v in cols.items() if v is not None}
        db.execute("INSERT OR IGNORE INTO issues(key, first_pulled_at) VALUES (?,?)", (k, ts))
        if present:
            sets = ", ".join(f"{c}=?" for c in present) + ", last_pulled_at=?"
            db.execute(f"UPDATE issues SET {sets} WHERE key=?", (*present.values(), ts, k))
        for l in f.get("issuelinks") or []:
            t = (l.get("type") or {}).get("name")
            if "outwardIssue" in l:
                db.execute("INSERT OR IGNORE INTO issue_links VALUES (?,?,?,?)", (k, t, "outward", l["outwardIssue"]["key"]))
            if "inwardIssue" in l:
                db.execute("INSERT OR IGNORE INTO issue_links VALUES (?,?,?,?)", (k, t, "inward", l["inwardIssue"]["key"]))
        if any(x in f for x in ("summary", "customfield_10117", "customfield_12794")):
            raw.execute("INSERT OR IGNORE INTO issue_text(key) VALUES (?)", (k,))
            for col, fld in (("summary", "summary"), ("rca", "customfield_10117"), ("ria", "customfield_12794")):
                if fld in f:
                    raw.execute(f"UPDATE issue_text SET {col}=?, pulled_at=? WHERE key=?", (as_text(f.get(fld)), ts, k))
        n += 1
    db.execute("INSERT INTO query_log(run_at,purpose,source,jql,dump_file,issues_loaded) VALUES (?,?,?,?,?,?)",
               (ts, purpose, "jira-mcp", jql, os.path.basename(path), n))
    db.commit(); raw.commit()
    print(f"loaded {n} issues from {path}")


def load_count(purpose, label, jql, count):
    db, _ = connect()
    db.execute("INSERT OR REPLACE INTO jql_counts VALUES (?,?,?,?,?)", (now(), purpose, label, jql, count))
    db.commit()


def load_csv(path, table):
    db, _ = connect()
    rows = list(csv.DictReader(open(path)))
    if not rows:
        return
    cols = list(rows[0])
    db.execute(f'DROP TABLE IF EXISTS "{table}"')
    db.execute(f'CREATE TABLE "{table}" ({", ".join(chr(34)+c+chr(34) for c in cols)})')
    db.executemany(f'INSERT INTO "{table}" VALUES ({",".join("?"*len(cols))})', [tuple(r[c] for c in cols) for r in rows])
    db.commit()
    print(f"{table}: {len(rows)} rows")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["dump", "count", "csv"])
    ap.add_argument("path", nargs="?")
    ap.add_argument("table", nargs="?")
    ap.add_argument("--purpose", default="")
    ap.add_argument("--jql", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--count", type=int)
    ap.add_argument("--cfb", action="store_true", help="all issues in dump come from the CFB query")
    a = ap.parse_args()
    if a.mode == "dump":
        load_dump(a.path, a.purpose, a.jql, a.cfb)
    elif a.mode == "count":
        load_count(a.purpose, a.label, a.jql, a.count)
    else:
        load_csv(a.path, a.table)
