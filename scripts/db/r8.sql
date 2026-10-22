-- R8 views. Causing item = Story or Bug named as cause of a fixed CFB (created >= 2025-01-01).
DROP VIEW IF EXISTS r8_causing;
CREATE VIEW r8_causing AS
SELECT DISTINCT i.key, i.issuetype, i.project, i.rnd_vp, i.team,
       CASE WHEN substr(i.resolved,6,2) BETWEEN '01' AND '03' THEN substr(i.resolved,1,4)||'-Q1'
            WHEN substr(i.resolved,6,2) BETWEEN '04' AND '06' THEN substr(i.resolved,1,4)||'-Q2'
            WHEN substr(i.resolved,6,2) BETWEEN '07' AND '09' THEN substr(i.resolved,1,4)||'-Q3'
            ELSE substr(i.resolved,1,4)||'-Q4' END AS rq,
       CASE WHEN i.ai_implemented = 'Yes' THEN 'yes' ELSE 'not' END AS ai,
       i.ai_implemented AS ai_raw,
       MAX(CASE WHEN c.source IN ('rca_text','issuelink:is_caused_by') THEN 1 ELSE 0 END) AS primary_src
FROM causal_links c JOIN issues i ON i.key = c.causing_key
WHERE i.issuetype IN ('Story','Bug') AND i.resolved IS NOT NULL AND i.project NOT IN ('CGY','ENG')
GROUP BY i.key;

DROP VIEW IF EXISTS r8_denoms;
CREATE VIEW r8_denoms AS
SELECT substr(label, 1, instr(label,'|')-1) AS issuetype,
       substr(label, instr(label,'|')+1, instr(substr(label, instr(label,'|')+1),'|')-1) AS ai,
       substr(label, length(label)-6) AS rq, count AS n
FROM jql_counts WHERE purpose='R8' AND label NOT LIKE 'VP|%' AND label NOT LIKE '%..%';

DROP VIEW IF EXISTS r8_detection;
CREATE VIEW r8_detection AS
SELECT COALESCE(i.rnd_vp,'(empty)') AS vp,
       CASE WHEN i.ai_label=1 OR i.ai_implemented='Yes' THEN 'ai_fix' ELSE 'other_fix' END AS fix_kind,
       count(*) AS fixed_cfb,
       sum(CASE WHEN EXISTS (SELECT 1 FROM causal_links c WHERE c.cfb_key=i.key AND c.source='rca_text') THEN 1 ELSE 0 END) AS names_cause
FROM issues i WHERE i.is_cfb=1 AND i.resolution='Fixed' AND i.created >= '2025-01-01'
GROUP BY 1,2;
