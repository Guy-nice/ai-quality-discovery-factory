#!/bin/sh
# R8 denominator counts (JQL count results recorded 2026-10-22). Re-run: python3 -I scripts/db/load.py count ...
cd "$(dirname "$0")/../.."
c() { python3 -I scripts/db/load.py count --purpose R8 --label "$1" --jql "$2" --count "$3"; }
Q="2025-Q1:2025-01-01:2025-04-01 2025-Q2:2025-04-01:2025-07-01 2025-Q3:2025-07-01:2025-10-01 2025-Q4:2025-10-01:2026-01-01 2026-Q1:2026-01-01:2026-04-01 2026-Q2:2026-04-01:2026-07-01 2026-Q3:2026-07-01:2026-10-01"
rec() { # type ai quarter count
  for q in $Q; do n=${q%%:*}; r=${q#*:}; a=${r%%:*}; b=${r#*:}
    if [ "$n" = "$3" ]; then
      case $2 in all) f="";; yes) f=" and cf[15229] = Yes";; notempty) f=" and cf[15229] is not EMPTY";; no) f=" and cf[15229] = No";; esac
      c "$1|$2|$3" "issuetype = $1 and resolved >= \"$a\" and resolved < \"$b\"$f and project not in (CGY, ENG)" "$4"; fi; done; }
rec Story all 2025-Q1 19320; rec Story all 2025-Q2 22046; rec Story all 2025-Q3 22953; rec Story all 2025-Q4 22295; rec Story all 2026-Q1 24828; rec Story all 2026-Q2 30857; rec Story all 2026-Q3 33231
rec Story yes 2025-Q1 43; rec Story yes 2025-Q2 51; rec Story yes 2025-Q3 71; rec Story yes 2025-Q4 358; rec Story yes 2026-Q1 2381; rec Story yes 2026-Q2 8907; rec Story yes 2026-Q3 8265
rec Story no 2026-Q2 10132
rec Bug all 2025-Q1 5200; rec Bug all 2025-Q2 5678; rec Bug all 2025-Q3 5922; rec Bug all 2025-Q4 5538; rec Bug all 2026-Q1 6368; rec Bug all 2026-Q2 8509; rec Bug all 2026-Q3 12791
rec Bug yes 2025-Q4 31; rec Bug yes 2026-Q1 438; rec Bug yes 2026-Q2 1134; rec Bug yes 2026-Q3 1747
c "Bug|yes|2025-Q1..Q3" 'issuetype = Bug and resolved >= "2025-01-01" and resolved < "2025-10-01" and cf[15229] = Yes and project not in (CGY, ENG)' 7
rec Story notempty 2026-Q1 3353; rec Story notempty 2026-Q2 19039; rec Story notempty 2026-Q3 16617
rec Bug notempty 2026-Q1 1181; rec Bug notempty 2026-Q2 5704; rec Bug notempty 2026-Q3 5117
v() { c "VP|$1|$2|2026-Q1..Q3" "issuetype in (Story, Bug) and resolved >= \"2026-01-01\" and resolved < \"2026-10-01\" and \"R&D VP[Dropdown]\" = \"$1\"$( [ "$2" = yes ] && echo ' and cf[15229] = Yes') and project not in (CGY, ENG)" "$3"; }
v "Analytics and Data" all 11102; v "Analytics and Data" yes 2002
v "Orchestration Core" all 8266; v "Orchestration Core" yes 2327
v "WFM" all 16808; v "WFM" yes 5694
v "AHW" all 9535; v "AHW" yes 3172
v "APQ" all 17019; v "APQ" yes 6472
c "Epic|all|2026-Q1..Q3" 'issuetype = Epic and resolved >= "2026-01-01" and resolved < "2026-10-01" and project not in (CGY, ENG)' 19752
c "Epic|yes|2026-Q1..Q3" 'issuetype = Epic and resolved >= "2026-01-01" and resolved < "2026-10-01" and cf[15229] = Yes and project not in (CGY, ENG)' 6275
c "Epic|no|2026-Q1..Q3" 'issuetype = Epic and resolved >= "2026-01-01" and resolved < "2026-10-01" and cf[15229] = No and project not in (CGY, ENG)' 4980
