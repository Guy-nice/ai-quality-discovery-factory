"""R9: tag Orchestration Core CFBs with a sub-flow (first matching rule wins). Writes table flow_tags."""
import json, os, re, sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"), timeout=60)
db.execute(f"ATTACH '{os.path.join(ROOT, 'data', 'db', 'raw_local.sqlite')}' AS r")

STUCK_LABELS = {"stuck_contact", "loststuckcontacts", "loststuckagentcontacts", "stuckcontacts"}
RULES = [
    ("stuck/lost contact", r"stuck|hanging contact|phantom|orphan|lost .*contact|loststuck|remain(s|ed)? (in queue|queued|displayed as active)|still showing as|calls remain queued|old .*contacts are showing|stale"),
    ("dialer/outbound", r"dialer|personal connection|outbound|campaign|\bdnc\b|call suppression|\bobms\b"),
    ("transfer/conference", r"transfer|conferenc|consult|forward after|takeover|unlinkagent|multiparty"),
    ("digital routing", r"(digital|chat|e-?mail|sms|\bdfo\b|work ?item|\bcases?\b|\bdx\b).*(rout|assign|queue|deliver|match|capacity|refus|concurren)|(rout|assign|deliver).*(digital|chat|e-?mail|work ?item|cases?)\b|channel lock|inqueue state|e-?mails? .*merged|cherry-picked digital|digital hopper|number of chats"),
    ("routing/skill/queue", r"rout|findmatch|\bvfm\b|\bafm\b|resolver|longest avail|in queue|queue|skill.*(prof|reset|deactiv|reactiv|assignment|not working)|matched|available agent|overflow|priority|callback|requeue|refus|osh\b|preagent|reskill|receiv(e|ing) (contacts|calls|certain)|time to start receiving|taking different path|assigned to agents|deactivating and reactivating|prepareforinbound|concurrent agent limit"),
    ("IVR/Studio script", r"studio|script|\bivr\b|snippet|framework action|\baction\b|prompt|spawn|onanswer|ondata|asjson|returnvars|dynamicdata|page ?action|\bbot|variables|mcr meta|pageclose|omilia|transcribe|voicemail|reqagent|popurl|runapp"),
    ("ACD/contact state", r"agent session|login|logged|log ?out|logoff|\bstate\b|\bacw\b|call drop|dropped|dead air|media server|failover|recording|duration|sessiontimeout|status|unavailable code|\bvc\b|agent leg|hangup|audio|soft ?phone|unable to (make|receive|connect|answer)|inbound call|outage|degradation|platform|split traffic|unassigned|temporarily connected|voice control|call park|queue counter"),
    ("reporting/dashboard", r"dashboard|reporting|prebuilt report|report (page|template)|reports? show|custom reports|summary report|contact summary|data share|interaction(s)? hub|interactions|export|widget|billing|live.?monitoring|data download|contact history|snowflake|etl"),
    ("admin/config/API", r"acd|admin|user ?hub|users?\b|bulk|upload|address book|\bpoc\b|hours of operation|time ?zone|teams?\b|skills? page|api|audit|disposition|template|profile|extension|sync|toggle|notification|permission|role"),
]
COMPILED = [(n, re.compile(p, re.I)) for n, p in RULES]
FLOW_SCOPE = {"stuck/lost contact", "dialer/outbound", "transfer/conference", "digital routing",
              "routing/skill/queue", "IVR/Studio script", "ACD/contact state"}


def tag(summary, labels):
    if any(l.lower() in STUCK_LABELS for l in labels):
        return "stuck/lost contact", "label"
    if any(l.lower() == "wrong_routing" for l in labels):
        return "routing/skill/queue", "label"
    for name, rx in COMPILED:
        if rx.search(summary or ""):
            return name, f"summary:{name}"
    return "other", "none"


db.execute("DROP TABLE IF EXISTS flow_tags")
db.execute("CREATE TABLE flow_tags (key TEXT PRIMARY KEY, sub_flow TEXT, in_flow_scope INTEGER, rule TEXT)")
rows = db.execute("""SELECT i.key, t.summary, i.labels FROM issues i JOIN r.issue_text t USING(key)
                     WHERE i.rnd_vp='Orchestration Core' AND i.is_cfb=1 AND i.created >= '2024-10-22'""").fetchall()
for k, s, l in rows:
    sf, rule = tag(s, json.loads(l or "[]"))
    db.execute("INSERT INTO flow_tags VALUES (?,?,?,?)", (k, sf, 1 if sf in FLOW_SCOPE else 0, rule))
db.commit()
for r in db.execute("SELECT sub_flow, COUNT(*) FROM flow_tags GROUP BY 1 ORDER BY 2 DESC"):
    print(r)
