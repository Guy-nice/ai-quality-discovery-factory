"""SO-1 failure-mode catalog for race / stuck / ACD-state pilot CFBs (valid, in-flow, created >= 2025-10-22).

Modes were assigned by reading summary + RCA "How did it happen" (raw_local.sqlite). Only labels are stored.
Writes table failure_modes and data/aggregates/so1-failure-modes.csv. Run: python3 -I scripts/db/so1_modes.py
"""
import csv, os, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB = os.path.join(ROOT, "data", "db", "quality.sqlite")
RAW = os.path.join(ROOT, "data", "db", "raw_local.sqlite")
OUT = os.path.join(ROOT, "data", "aggregates", "so1-failure-modes.csv")

MODES = {
    "M1": "Out-of-order or stale event overwrites newer state",
    "M2": "Concurrent update of in-memory state in VC (double delivery, stale object, unsafe shared data)",
    "M3": "Event lost or not published / consumer stopped",
    "M4": "Match or delivery state not cleared after reject / timeout",
    "M5": "Capacity or throughput saturation (threads, rate limits, blocking calls)",
    "M6": "Non-race logic or data bug in ACD state (out of SO-1 scope)",
    "M7": "Unknown: RCA not filled",
}

LABELS = {
    "VOL-8004": ("M1", "Contact Retry Service (VC IVR + COR)"),
    "EM-146033": ("M1", "State Streams mixed-dfo-contact"),
    "EM-148596": ("M1", "State Streams DFO (out-of-order check regression)"),
    "AOR-9450": ("M1", "Routing requeue vs contact end"),
    "AOR-13256": ("M1", "AFM skill events (subsequence check)"),
    "AOR-15089": ("M1", "OBMS SkillRoutable ON/OFF"),
    "EM-137706": ("M1", "VC ContactStateChange vs gRPC response"),
    "VOL-8376": ("M2", "VC queue info cache + FindMatch"),
    "ORC-52711": ("M2", "VC agent session delivery flag"),
    "AOR-10487": ("M2", "Contact Retry in-memory contact (stale skill)"),
    "ORC-53647": ("M2", "VC MasterVariables shared dictionary"),
    "ORC-53838": ("M2", "VC PrepareForInbound trigger order"),
    "ORC-52396": ("M2", "VC agent global variable reset"),
    "VOL-9036": ("M2", "VC in-memory queue vs FindMatch (repeated ReqAgent)"),
    "ORC-47645": ("M3", "VC ContactRoutable not published to FindMatch"),
    "AOR-13364": ("M3", "VC -> Kinesis event drop (AgentSession)"),
    "EM-158368": ("M3", "State Streams Kinesis consumer (dependency upgrade)"),
    "EM-158691": ("M3", "State Streams KDA restart loop"),
    "AOR-9567": ("M3", "Contact Retry cluster list (events skipped)"),
    "ORC-55399": ("M3", "VC contact end reason not sent on logout"),
    "ORC-51076": ("M4", "VC wakeup queue / Sleeping state"),
    "AOR-15178": ("M4", "VC lastMatched not cleared after reject"),
    "VOL-8236": ("M4", "Agent script SUBMITDATA with missing script"),
    "ORC-52995": ("M5", "VC blocking thread limit"),
    "ORC-54317": ("M5", "VC REST max execution threads"),
    "AOR-10768": ("M5", "Resolver Kinesis read limit"),
    "AOR-15057": ("M5", "Agent Capacity blocking REST call in stream"),
    "ORC-47954": ("M5", "Customer snippet compute time (toggle)"),
    "AAD-47498": ("M5", "Stored procedure cost (agent list API)"),
    "AAD-38815": ("M6", "Agent list division filter"),
    "EM-162801": ("M6", "Malformed interaction ID validation"),
    "AAD-47814": ("M6", "User sync job setting change"),
    "AAD-49931": ("M6", "User sync stored procedure default"),
    "AAD-50039": ("M6", "Agents API input validation"),
    "EM-172483": ("M6", "MCH state change time not refreshed"),
    "ORC-52345": ("M6", "VCSvc build dependency (Extensions 9.0.9)"),
    "EM-172332": ("M6", "Feature toggle default"),
    "ORC-55190": ("M6", "Login report client type"),
}
UNKNOWN = ["EM-161103", "EM-161102", "ORC-52982", "ORC-54265", "ORC-54253", "ORC-54264", "ORC-54332",
           "AOR-16117", "ORC-55108", "VOL-11525", "ORC-55466", "AOR-16923", "ORC-55832"]


def detected_by(summary):
    s = (summary or "")
    if s.startswith("MI ") or " MI " in s or "MI:" in s or "MI 0" in s:
        return "major incident"
    if "XMatters" in s:
        return "alert (xMatters)"
    return "customer case"


def main():
    db = sqlite3.connect(DB, timeout=120)
    db.execute("ATTACH DATABASE ? AS r", (RAW,))
    db.execute("DROP TABLE IF EXISTS failure_modes")
    db.execute("CREATE TABLE failure_modes (key TEXT PRIMARY KEY, mode TEXT, mode_name TEXT, component TEXT, detected_by TEXT, sub_flow TEXT, priority TEXT, incidents INTEGER)")
    rows = []
    for k in list(LABELS) + UNKNOWN:
        mode, comp = LABELS.get(k, ("M7", "unknown"))
        r = db.execute("SELECT t.summary, f.sub_flow, i.priority, i.incidents FROM issues i JOIN flow_tags f ON f.key = i.key "
                       "LEFT JOIN r.issue_text t ON t.key = i.key WHERE i.key = ?", (k,)).fetchone()
        summ, sf, pr, inc = r
        row = (k, mode, MODES[mode], comp, detected_by(summ), sf, pr, inc)
        db.execute("INSERT INTO failure_modes VALUES (?,?,?,?,?,?,?,?)", row)
        rows.append(row)
    db.commit()
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "mode", "mode_name", "component", "detected_by", "sub_flow", "priority", "incidents"])
        w.writerows(rows)
    print(len(rows), "rows")
    for m in MODES:
        sel = [x for x in rows if x[1] == m]
        print(m, len(sel), "incidents", sum(x[7] or 0 for x in sel), "P1/P2", sum(1 for x in sel if x[6] in ("P1", "P2")),
              "MI", sum(1 for x in sel if x[4] != "customer case"))


if __name__ == "__main__":
    main()
