"""Ingest monthly-window CFB dumps: name by month, log exact JQL, flag months needing page 2."""
import json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
purpose, prefix = sys.argv[1], sys.argv[2]
for src in sys.argv[3:]:
    d = json.load(open(src))
    nodes = d["issues"]["nodes"]
    first = min(n["fields"]["created"][:10] for n in nodes)
    m = first[:7]
    y, mo = int(m[:4]), int(m[5:7])
    nxt = f"{y + (mo == 12)}-{(mo % 12) + 1:02d}"
    half = os.environ.get("HALF")
    if half:
        lo, hi = (f"{m}-01", f"{m}-16") if int(first[8:10]) < 16 else (f"{m}-16", f"{nxt}-01")
        m = lo
    pi = d["issues"].get("pageInfo", {})
    page = sys.argv[0] and ("p2" if os.environ.get("PAGE2") else "p1")
    dest = os.path.join(ROOT, "data", "raw", purpose, f"{prefix}-{m}-{page}.json")
    shutil.copy(src, dest)
    if not half:
        lo, hi = f"{m}-01", f"{nxt}-01"
    jql = f'issuetype = Bug and salesforceAssociatedTypes is not EMPTY and created >= "{lo}" and created < "{hi}" ORDER BY created ASC'
    subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts/db/load.py"), "dump", dest, "--purpose", purpose, "--jql", jql + (" [page2]" if page == "p2" else ""), "--cfb"], check=True)
    print(m, len(nodes), "NEXT:" + pi["endCursor"] if pi.get("hasNextPage") else "done")
