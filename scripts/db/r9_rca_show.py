"""R9: print compact RCA sections for reading (local only, prints to stdout, writes nothing)."""
import os, re, sqlite3, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"))
db.execute(f"ATTACH '{os.path.join(ROOT, 'data', 'db', 'raw_local.sqlite')}' AS r")
BOIL = ["Describe functional impact of the issue.", "Describe technical reason for the issue.",
        "Indicate the root cause for the issue (gap in process, documentation, workflow, SDLC, etc.).",
        "If regression bug, indicate why Regression Impact Analysis (RIA) didn’t catch the issue in causing epic/story/bug?",
        "Indicate JIRA item which caused this issue.", "Indicate how the issue was fixed.",
        "Identify any long term work needed to resolve.", "Indicate if the team can add any  alarms or monitors to catch the issue sooner.",
        "Describe changes team will implement in form of work items (JIRA, confluence, templates, process, etc.) to close gap identified on how it was missed."]
HEADS = ["What happened", "How did it happen", "How was it missed", "How was it introduced", "How was it fixed", "Long-term", "Is there an opportunity", "What will be done"]
KEEP = {"How did it happen": 260, "How was it missed": 380, "How was it introduced": 180, "What will be done": 180}
rows = db.execute("""SELECT i.key, i.team, i.priority, t.rca FROM issues i JOIN r.issue_text t USING(key)
  WHERE i.rnd_vp='Orchestration Core' AND i.is_cfb=1 AND i.created>='2025-10-22' AND i.resolution IN ('Fixed','Fixed - Config')
  ORDER BY i.key""").fetchall()
a, b = int(sys.argv[1]), int(sys.argv[2])
for i, (k, team, pr, t) in enumerate(rows[a:b], a):
    t = t or ""
    for x in BOIL: t = t.replace(x, "")
    t = re.sub(r"[*\\#>]", "", t); t = re.sub(r"\s+", " ", t)
    pos = sorted((t.find(h), h) for h in HEADS if t.find(h) >= 0)
    out = []
    for j, (p, h) in enumerate(pos):
        e = pos[j + 1][0] if j + 1 < len(pos) else len(t)
        if h in KEEP:
            out.append(f"{h.split()[-1].upper()}:{t[p + len(h):e].strip(' ?:-')[:KEEP[h]]}")
    if not out: out = [t[:700]]
    print(f"#{i} {k} {(team or '')[:12]} {pr} | " + " | ".join(out))
print("total", len(rows))
