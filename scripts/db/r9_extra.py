"""R9: store non-Jira evidence (Confluence page list, Git repo access) in quality.sqlite. One-line summaries only."""
import os, sqlite3
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect(os.path.join(ROOT, "data", "db", "quality.sqlite"), timeout=60)
db.execute("DROP TABLE IF EXISTS confluence_pages")
db.execute("CREATE TABLE confluence_pages (page_id TEXT PRIMARY KEY, space TEXT, title TEXT, last_modified TEXT, topic TEXT, purpose TEXT, summary_1line TEXT, pulled_by TEXT)")
PAGES = [
    ("4072866234", "IN", "Findmatch Testing Gap Analysis Summary (Unit / Integration / E2E)", "2026-08-27", "test gaps", "analysis", "35 gaps (3 critical): no real Kafka/DB integration test, no concurrency test for claim retry, ~half of Playwright E2E suite fixme/skip, no CI skip visibility, no coverage gate."),
    ("1903493964", "IN", "AFM - Advanced FindMatch", "2026-09-14", "architecture", "design", "AFM = new Kafka Streams + Aurora matching service; outbound-matching sibling added 2026-08."),
    ("4076208133", "IN", "VFM (app-findmatch): Current Data Flow", "2026-08-27", "architecture", "design", "VFM = legacy Scala/Akka/Kinesis matching service, still live in parallel with AFM."),
    ("1903363038", "IN", "AFM - State Aggregator", "2026-08-27", "architecture", "design", "State Aggregator feeds AFM from shared topics; documents SKILL_ACTIVATE quirk and feedback loop."),
    ("1903853586", "IN", "AFM - Blender Service", "2026-09-14", "architecture", "design", "Blender service page, rewritten and source-verified 2026-09-14."),
    ("1903820843", "IN", "AFM - Match Distributor", "2026-09-14", "architecture", "design", "Match Distributor service page."),
    ("4076339502", "IN", "Contact Retry: Event Processing & Retry-Loop Logic", "2026-08-27", "architecture", "design", "Contact Retry = standalone Kafka Streams + PostgreSQL + Kinesis service tapping shared input topic."),
    ("4072014111", "IN", "Advanced Findmatch (AFM): Generic Rollback Plan", "2026-08-26", "release", "runbook", "Rollback for ~20 regional AFM deployments; afmEnabled flag decides AFM vs VFM per BU."),
    ("232817176", "CXONE", "EOR: routing-ng-advanced-findmatch", "2026-10-20", "readiness", "EOR", "Evidence of Readiness page for AFM microservice."),
    ("4246340207", "IN", "AFM Alarm RunBook", "2026-10-14", "operations", "runbook", "First-pass triage of AFM production alerts (Kinesis iterator age and dependencies)."),
    ("4221010179", "IN", "AFM Chaos scenarios", "2026-10-08", "resilience", "test plan", "5 chaos scenarios, 14 tests for AFM."),
    ("4086694457", "IN", "AFM Services Chaos Testing Plan - PFOR Environment", "2026-08-31", "resilience", "test plan", "32 chaos tests in 6 phases; status NOT STARTED at last edit."),
    ("4231365389", "IN", "2.4 Latency on AFM services, 10mins", "2026-10-08", "resilience", "test result", "50 ms injected latency for 10 min: matches fell ~60%, backlog grew."),
    ("4185359041", "IN", "New Region/Cluster Setup - Omnichannel Routing (FindMatch)", "2026-09-29", "operations", "runbook", "Routing-specific steps for new region / cluster bring-up."),
    ("4076470826", "IN", "RUNBOOK: VFM Load Test with Cortex XDR (perf)", "2026-08-27", "performance", "runbook", "Load test on legacy VFM to measure security agent CPU cost."),
    ("4228809169", "IN", "Tenant Migration - Impact Assessment - Team Advanced Omnichannel Routing", "2026-10-16", "change", "impact assessment", "Impact of moving tenants between ACD clusters."),
    ("3873800676", "CXONE", "Stuck Contact/Agent", "2026-10-21", "stuck contacts", "support response", "Standard support response: scheduled stuck-contact cleanup per region."),
    ("4256301562", "CXONE", "Stuck Contact - Resolved Swarms", "2026-10-21", "stuck contacts", "swarm log", "Auto-maintained CSV of resolved stuck-contact swarms; many root causes 'unknown', resolution = manual cleanup."),
    ("4256006416", "CVWCX", "Weekly RCA for Stuck contacts", "2026-10-16", "stuck contacts", "RCA tracker", "Weekly RCA meeting tracker for stuck contacts (alarm gaps, TTL changes)."),
    ("4252663877", "IN", "27.1 Stuck Contacts Cleanup Automation sync for old prod regions", "2026-10-20", "stuck contacts", "deployment", "Cleanup automation deployed to data lake util namespace (symptom cleanup, not cause fix)."),
    ("4258234458", "IN", "02919770 (P1) Possible stuck contacts and agent sessions", "2026-10-16", "incident", "MI page", "P1 MI, NA1 C18, multiple BUs, stuck contacts and agent sessions."),
    ("4150689943", "IN", "Voltron PHASE 1 Cache Conversion", "2026-10-21", "change", "runbook", "Cluster cache conversion to new NCache ID and MessagePack serialization."),
    ("4232414340", "CXONE", "2026 Voltron Build Status Summary", "2026-10-21", "change", "tracker", "Per-cluster Voltron decoupling build schedule (ongoing in 2026-10)."),
    ("4011033522", "IN", "Voltron Resilience Experiments Plan", "2026-10-01", "resilience", "test plan", "Voltron resilience experiments under Game Days program."),
    ("4213309445", "IN", "Voltron Customer-Centric SLIs and SLOs", "2026-10-02", "observability", "SLO", "Voltron uses ACD customer-journey SLIs from VCSvc."),
    ("3631251647", "IN", "Architecture for KDA to EKS Deployment of State Stream Transformers", "2026-10-15", "architecture", "design", "State Streams = Flink pipeline transforming EM, VC and DFO events; migrating KDA to EKS."),
    ("4170678316", "IN", "State-Streams EKS - Keeping KDA and EKS Transformers in Sync", "2026-09-22", "change", "process", "EKS repos are one-way forks of KDA repos; un-ported change = silent divergence."),
    ("4256694278", "IN", "State-Streams EKS - Rollback Plan (EKS -> KDA)", "2026-10-16", "release", "runbook", "Rollback plan; EKS rollback restarts a 92-day soak."),
    ("3795157075", "CXONE", "EOR: orch-entity-state-streams-unified-disposition", "2026-09-21", "architecture", "EOR", "Flink app merging EM (Kafka) and legacy VC (Kinesis) disposition events."),
    ("4041444339", "IN", "Telephony Feature Service (TFS) <-> Entity Management (EM) Integration", "2026-09-22", "architecture", "design", "New TFS service replacing VC telephony features; integration draft."),
]
for p in PAGES:
    db.execute("INSERT INTO confluence_pages VALUES (?,?,?,?,?,?,?,?)", (*p, "R9"))
db.execute("DROP TABLE IF EXISTS git_repos")
db.execute("CREATE TABLE git_repos (org TEXT, repo TEXT, pushed_at TEXT, language TEXT, access TEXT, commits_12m INTEGER, role TEXT, PRIMARY KEY(org, repo))")
REPOS = [
    ("inContact", "routing-ng-advanced-findmatch", "2026-10-22", "Java", "read", 254, "AFM matching (new)"),
    ("inContact", "app-findmatch", "2026-08-24", "Scala", "read", 20, "VFM matching (legacy)"),
    ("inContact", "routing-ng-contact-retry", "2026-10-13", "Java", "read", 182, "contact retry"),
    ("inContact", "orchestration-resolver", "2026-08-24", "Java", "read", 36, "resolver"),
    ("inContact", "routing-ng-agent-capacity-service", "2026-10-16", "Java", "read", 222, "agent capacity"),
    ("inContact", "routing-ng-blender", "2026-10-19", "Java", "read", 97, "blender"),
    ("inContact", "routing-ng-match-distributor", "2026-10-22", "Java", "read", 90, "match distributor"),
    ("inContact", "orch-entity-agent", "2026-10-16", "Go", "read", 26, "EM agent entity"),
    ("inContact", "orch-entity-orchestration", "2026-10-20", "Go", "read", 13, "EM orchestration"),
    ("inContact", "orch-entity-state-streams-common", "2026-10-20", "Java", "read", 26, "state streams common"),
    ("inContact", "routing-ng-integration-tests", "2026-10-22", "Java", "read", 312, "integration tests"),
    ("inContact", "acd-playwright-e2e", "2026-10-22", "TypeScript", "read", 1294, "E2E tests"),
    ("(TFS - not GitHub)", "VC monolith (VCSvc, ScriptHelper, WebScripting, stored procedures)", None, "C#/.NET, T-SQL", "not found in GitHub", None, "legacy monolith; RCAs cite TFS changesets"),
]
for r in REPOS:
    db.execute("INSERT INTO git_repos VALUES (?,?,?,?,?,?,?)", r)
db.commit()
print("confluence_pages", db.execute("select count(*) from confluence_pages").fetchone()[0], "git_repos", db.execute("select count(*) from git_repos").fetchone()[0])
