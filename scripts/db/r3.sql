-- R3/R14 queries (run: sqlite3 data/db/quality.sqlite < scripts/db/r3.sql)
-- Link rate per repo (non-merge, non-bot, 24 months)
SELECT repo, COUNT(*) commits, ROUND(100.0*SUM(has_key)/COUNT(*),1) key_pct, SUM(cfb_fix) cfb_fix, SUM(pilot_fix) pilot_fix, SUM(causing) causing
FROM r3_commit_flags WHERE merge=0 AND bot=0 AND bulk=0 AND date>='2024-10-22' GROUP BY repo;
-- PH-3: dependency / runtime commits vs other commits in the monolith (causing + CFB-fix rates)
WITH dep AS (
  SELECT DISTINCT repo, sha FROM git_file_changes
  WHERE repo='inContact' AND (path LIKE '%.csproj' OR path LIKE '%packages.config' OR path LIKE '%Directory.Packages.props'
        OR path LIKE '%Directory.Build.props' OR path LIKE '%.props' OR path LIKE '%app.config' OR path LIKE '%web.config' OR path LIKE '%global.json'))
SELECT CASE WHEN d.sha IS NULL THEN 'other' ELSE 'touches dependency/runtime files' END kind,
       COUNT(*) commits, SUM(f.causing) causing, ROUND(100.0*SUM(f.causing)/COUNT(*),2) causing_pct,
       SUM(f.cfb_fix) cfb_fix, ROUND(100.0*SUM(f.cfb_fix)/COUNT(*),2) cfb_fix_pct
FROM r3_commit_flags f LEFT JOIN dep d ON d.repo=f.repo AND d.sha=f.sha
WHERE f.repo='inContact' AND f.merge=0 AND f.bot=0 AND f.bulk=0 AND f.date>='2024-10-22' GROUP BY 1;
-- Pilot-flow hotspot dirs
SELECT repo, path, commits_24m, pilot_fix_24m, causing_24m, test_touch_pct FROM r3_dir_hotspots
WHERE is_test_path=0 AND area!='test' AND pilot_fix_24m>=3 ORDER BY pilot_fix_24m DESC;
