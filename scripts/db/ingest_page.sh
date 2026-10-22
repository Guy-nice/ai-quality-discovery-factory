#!/bin/sh
# usage: ingest_page.sh <tool-result-file> <dest-name> <purpose> <jql> [--cfb]
set -e
cd "$(dirname "$0")/../.."
cp "$1" "data/raw/$3/$2.json"
python3 -I scripts/db/load.py dump "data/raw/$3/$2.json" --purpose "$3" --jql "$4" $5
python3 -I -c "import json,sys;d=json.load(open(sys.argv[1]));p=d['issues'].get('pageInfo',{});print('next:',p.get('endCursor') if p.get('hasNextPage') else 'NONE')" "data/raw/$3/$2.json"
