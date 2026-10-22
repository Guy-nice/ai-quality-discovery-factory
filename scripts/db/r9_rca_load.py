"""R9: load reader labels (data/raw/r9/labels.txt) into rca_class (round R9) and compute agreement with R5-round1."""
import os, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"), timeout=60)
N = {"esc": {"REQ": "requirements/spec gap", "NOTEST": "missing test coverage", "INEFF": "test existed but ineffective",
             "REGR": "regression from recent change (RIA miss)", "ENV": "environment/config/data difference",
             "THIRD": "third-party/integration/dependency", "SCALE": "scale/performance/concurrency/race",
             "LEGACY": "legacy/unknown behavior", "DEPLOY": "deployment/release process", "MON": "monitoring gap",
             "UNCLEAR": "unclear/not stated"},
     "intro": {"RECENT": "specific recent change", "LONG": "long-standing/legacy code", "EXT": "external change", "UNK": "unknown"},
     "reg": {"Y": "yes", "N": "no", "U": "unknown"}, "yn": {"y": "yes", "n": "no"},
     "prev": {"TEST": "test added", "MON": "monitoring/alert", "PROC": "process change", "CODE": "code fix only", "NONE": "none stated"}}
db.execute("DELETE FROM rca_class WHERE round='R9'")
skip = n = 0
for line in open(os.path.join(ROOT, "data", "raw", "r9", "labels.txt")):
    p = line.split()
    if not p: continue
    if p[1] == "SKIP": skip += 1; continue
    k, esc, intro, reg, leg, ai, prev = p
    db.execute("INSERT INTO rca_class VALUES (?,?,?,?,?,?,?,?,?)", (k, "R9", "claude-fork-r9", N["esc"][esc], N["intro"][intro],
               N["reg"][reg], N["yn"][leg], N["yn"][ai], N["prev"][prev])); n += 1
db.commit()
print("classified", n, "skipped (no usable RCA)", skip)
cols = ["escape_cause", "introduced_by", "regression", "legacy_mentioned", "ai_mentioned", "prevention_action_type"]
rows = db.execute(f"""SELECT {','.join('a.'+c+', b.'+c for c in cols)} FROM rca_class a JOIN rca_class b ON a.key=b.key
                      WHERE a.round='R5-round1' AND b.round='R9'""").fetchall()
print("overlap", len(rows))
for i, c in enumerate(cols):
    agree = sum(1 for r in rows if r[2*i] == r[2*i+1])
    print(f"{c}: {agree}/{len(rows)} = {100*agree/len(rows):.0f}%")
