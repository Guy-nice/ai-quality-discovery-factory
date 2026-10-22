# Management deck build

`build.js` makes `docs/05-summary/management-deck.pptx` (pptxgenjs, 12 slides, theme "Quality Signal").

```bash
npm install pptxgenjs@3            # in a scratch dir
NODE_PATH=<scratch>/node_modules node scripts/deck/build.js docs/05-summary/management-deck.pptx
```

Numbers are typed from `docs/05-summary/summary-and-recommendations.md` and `data/aggregates/` (as of 2026-10-22). Update both when data changes.
