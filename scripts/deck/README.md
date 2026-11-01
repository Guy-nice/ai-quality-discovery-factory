# Deck builds

All decks are built with pptxgenjs and the theme "Quality Signal" (Cambria headings, Calibri body).

| Script | Output | Status |
|---|---|---|
| `build_offsite.js` | `docs/05-summary/offsite-deck.pptx` (17 slides) | **Current** |
| `build_dod.js` | `docs/05-summary/dod-v2-deck.pptx` (8 slides) | Current |
| `build_v3.js` | `docs/05-summary/management-deck-v3.pptx` (15 slides) | Current (2026-10-25 decision deck) |
| `build_v2.js`, `build.js` | `docs/05-summary/archive/management-deck-v2.pptx`, `-v1-superseded.pptx` | Archived |

```bash
npm install pptxgenjs@3            # in a scratch dir
NODE_PATH=<scratch>/node_modules node scripts/deck/build_offsite.js docs/05-summary/offsite-deck.pptx
```

`build_*.js` require `apply_theme.js` from the local pptx skill path set at the top of each script. Change that path on a new machine.

**Numbers:** typed from `docs/05-summary/management-report.md` (canonical, D-035) and `data/aggregates/`. When data changes, update the report first, then the decks.

**Checks after a build:** run the pptx skill `validate.py`, then open the deck in PowerPoint. LibreOffice is not installed on the build machine, so a visual check is manual.
