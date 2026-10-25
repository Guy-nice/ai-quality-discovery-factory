const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/Users/Guy.Guterman/.claude/skills/synced/ad2d1967-9b78-4a06-aa14-a45eb2824fc3_67ef7a44-32fc-4fe8-bd93-940173b50190/pptx/scripts/apply_theme.js");

const OUT = process.argv[2] || "/tmp/deck/management-deck.pptx";

const THEME = {
  name: "Quality Signal",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1B2A41", lt1: "FFFFFF", dk2: "4A5A72", lt2: "EEF2F6",
    accent1: "C8443D", accent2: "2A8C82", accent3: "E0A030", accent4: "8796AB",
    accent5: "1B2A41", accent6: "C9D3DF", hlink: "2A8C82", folHlink: "4A5A72",
  },
};
const H = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "Software Quality 2026 - Research Summary";
pres.author = "QA Architecture";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const FOOT = "Quality DoD v2  |  Evidence as of 2026-10-25  |  Revises Confluence 4048715783";

pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.2, w: 11.7, h: 1.9, fontSize: 40, bold: true, color: C.background1, valign: "bottom", align: "left", margin: 0 }, text: "Title" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.35, w: 11.7, h: 1.0, fontSize: 18, color: C.accent6, valign: "top", margin: 0 }, text: "Subtitle" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  margin: [0.5, 0.6, 0.6, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.95, fontSize: 30, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "Title" } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.0, w: 10.5, h: 0.3, fontSize: 10, color: C.text2, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.text2, align: "right" },
});
pres.defineSlideMaster({
  title: "CLOSE_DARK",
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.95, fontSize: 30, bold: true, color: C.background1, valign: "middle", align: "left", margin: 0 }, text: "Title" } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.0, w: 10.5, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});

const tb = (slide, text, o) => slide.addText(text, { isTextBox: true, margin: 0, fontSize: 14, color: C.text1, valign: "top", ...o });

function card(slide, x, y, w, h, fill, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill }, objectName: name,
  });
}

function numCircle(slide, x, y, n, fill, d = 0.5) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: `num-${n}` });
  tb(slide, String(n), { x, y, w: d, h: d, align: "center", valign: "middle", bold: true, fontSize: 16, color: C.background1 });
}

const chartText = { catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt", titleFontFace: "+mn-lt" };
const chartFrame = {
  catAxisLabelColor: H.dk2, valAxisLabelColor: H.dk2, catAxisLabelFontSize: 11, valAxisLabelFontSize: 11,
  valGridLine: { color: "DDE3EA", size: 0.75 }, catGridLine: { style: "none" },
  catAxisLineShow: false, valAxisLineShow: false, dataLabelFontSize: 11, dataLabelColor: H.dk1,
  titleColor: H.dk1, titleFontSize: 14, legendFontSize: 12, legendColor: H.dk1,
};



const th = (t) => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk1 } } });
const VC = { "Keep": H.accent2, "Strengthen": H.accent2, "Change": H.accent3, "Later": H.accent4, "Add": H.accent1 };
function verdictTable(slide, rows, name, first = "WIP DoD item") {
  slide.addTable([
    [th(first), th("v2 verdict"), th("Enforcement"), th("Evidence")],
    ...rows.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j < 2, color: j === 1 ? (VC[c.split(":")[0]] || H.dk1) : H.dk1, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
  ], { x: 0.6, y: 1.45, w: 12.1, colW: [3.3, 2.6, 2.4, 3.8], fontSize: 12, color: H.dk1, rowH: 0.5, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: name });
}

// 1 Title
pres.addSection({ title: "DoD v2" });
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "DoD v2" });
s.addText("Quality Definition of Done v2: What the Evidence Keeps, Changes and Adds", { placeholder: "title" });
s.addText("Revises the WIP Quality DoD (Confluence 4048715783)  |  QA Architecture  |  25 October 2026", { placeholder: "body" });

// 2 Why
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "DoD v2" });
s.addText("Why the DoD must change", { placeholder: "title" });
[["+49%", "P1/P2 customer-found bugs", C.accent1], ["96%", "of P1 incidents found by customers", C.accent1], ["Few", "DoD items block today; most are policy", C.text1], ["1.1-10.4", "incidents per bug across teams", C.text1]].forEach(([b, l, col], i) => {
  const x = 0.6 + i * 3.07;
  card(s, x, 1.55, 2.85, 2.3, C.background2, `why-${i}`);
  tb(s, b, { x: x + 0.25, y: 1.75, w: 2.4, h: 0.9, fontSize: 38, bold: true, color: col, fontFace: THEME.headFontFace });
  tb(s, l, { x: x + 0.25, y: 2.75, w: 2.4, h: 0.9, fontSize: 14, color: C.text2 });
});
card(s, 0.6, 4.25, 12.1, 2.4, C.text1, "principle");
tb(s, "Principle", { x: 0.9, y: 4.45, w: 11.5, h: 0.45, fontSize: 18, bold: true, color: C.accent3 });
tb(s, [
  { text: "A gate blocks only where data proves the risk.", options: { bold: true, breakLine: true } },
  { text: "Everything else is policy or a suggested means, measured and reviewed.", options: { breakLine: true } },
  { text: "Tiers come from evidence (impact, failure type, hotspot code), not from product names." },
], { x: 0.9, y: 4.95, w: 11.5, h: 1.55, fontSize: 17, color: C.background1, paraSpaceAfter: 6 });

// 3 Gate map
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "DoD v2" });
s.addText("Gate map v2: where each check sits and whether it blocks", { placeholder: "title" });
const gates = [
  ["Design", "Epic review; state / toggle section for risky Epics", "Policy + audit"],
  ["Pull request", "Hotspot size limit, code-owner review, tests, Jira key", "Blocks (hotspot)"],
  ["Build", "Unit tests, Sonar, secret and dependency scan", "Blocks"],
  ["Test health", "Suite blocks only while it holds its pass level", "Blocks when healthy"],
  ["Release", "Perf / chaos for high risk; data-based Go/No-Go", "Human + checks"],
  ["Deploy", "Toggle, progressive rollout, invariant monitors", "Release check"],
  ["Escape", "Bug fields + linked test before close", "Jira validator"],
];
const gw = 1.62, gg = 0.13;
gates.forEach(([name, chk, en], i) => {
  const x = 0.6 + i * (gw + gg);
  const blocks = en.startsWith("Blocks");
  s.addShape(pres.shapes.CHEVRON, { x, y: 1.6, w: gw, h: 0.8, fill: { color: blocks ? H.accent1 : H.dk1 }, line: { color: blocks ? H.accent1 : H.dk1 }, objectName: `gm-${i}` });
  tb(s, name, { x: x + 0.32, y: 1.6, w: gw - 0.5, h: 0.8, align: "center", valign: "middle", fontSize: 12, bold: true, color: C.background1 });
  card(s, x, 2.6, gw, 2.6, C.background2, `gmc-${i}`);
  tb(s, chk, { x: x + 0.1, y: 2.75, w: gw - 0.2, h: 1.7, fontSize: 13 });
  tb(s, en, { x: x + 0.1, y: 4.6, w: gw - 0.2, h: 0.5, fontSize: 12, bold: true, color: blocks ? C.accent1 : C.text2 });
});
tb(s, "Red = blocks. Agents (test plan, Playwright, RIA, exploratory, mutation) feed these checks; they are not gates by themselves.", { x: 0.6, y: 5.5, w: 12.1, h: 0.6, fontSize: 14, color: C.text2 });

// 4 Epic level
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "DoD v2" });
s.addText("Epic level: your WIP items, verdict by evidence", { placeholder: "title" });
verdictTable(s, [
  ["PRD / Epic review, acceptance criteria", "Strengthen: risky Epics", "Jira flow + audit", "Causing stories link a spec 6.8% vs 31.8%"],
  ["RIA phase 1 / phase 2", "Change: fixes + hotspots", "Policy; phase 2 later", "RIA miss 7-15%; half had RIA done"],
  ["Test plan / Playwright generator", "Keep: as means", "Suggested", "No escape evidence yet"],
  ["SonarQube gate", "Keep: block everywhere", "Required CI check", "Required in 1 of 5 pilot repos"],
  ["Mutation >= 80% (blocking)", "Change: visible first", "Block per scope later", "Weak tests 3%; 2 of 4 fails false"],
  ["ReportPortal; pipeline stable", "Change: test health", "Blocks when healthy", "Routing E2E 1.2% pass"],
  ["Performance test, Chaos Runner", "Keep: high risk only", "Release check", "Race / scale escapes 13-23%"],
  ["All tests in Xray, linked", "Change: escape + risky", "Policy + audit", "Links 18-25% today"],
  ["Plan reviewed with PM / Architect, PO", "Keep: high-impact teams", "Policy", "Teams differ strongly"],
], "epic-table");

// 5 Release level
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "DoD v2" });
s.addText("Release level: your WIP items, verdict by evidence", { placeholder: "title" });
verdictTable(s, [
  ["Feature toggle registered, owner, removal", "Keep: mandatory", "Release check", "Monolith cannot roll back"],
  ["Toggle verified on and off", "Keep: high risk", "Release check", "Same"],
  ["Deploy and rollback verified", "Change: toggle-off + progressive", "Release check", "Rollback not possible on monolith"],
  ["Post-deploy sanity by toggle", "Keep", "Release check", "-"],
  ["Synthetic monitor for changed paths", "Strengthen: correctness monitors", "Release check (high risk)", "96% of P1 found by customers"],
  ["No open P1-P3", "Keep", "Go/No-Go", "-"],
  ["Go/No-Go sign-off", "Change: data-based", "Human + data", "26.4 pages mostly TBD"],
], "release-table");

// 6 New items
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "DoD v2" });
s.addText("New items the evidence adds", { placeholder: "title" });
verdictTable(s, [
  ["Intake: defect vs MI vs expectation gap", "Add", "Jira required field", "MI tickets inflated the 2026 rise"],
  ["Bug fields: type, detected-by, cause", "Add", "Jira required (X1)", "Cause known for ~25% only"],
  ["Escape-to-test before close", "Add", "Jira validator", "38% of RCAs add a test today"],
  ["Hotspot PR rules: size, owner, tests", "Add", "Blocks on hotspot paths", "Follow-up fixes 21% -> 54% by size"],
  ["CODEOWNERS for hotspot code", "Add", "Required review", "Monolith has none; bus factor 1"],
  ["Bug-fix review, correctness types", "Add", "Policy -> block if X4", "1 in 4 known causes is a fix"],
  ["Emergency-change follow-up review", "Add", "Policy", "Emergency changes x2.9 since June"],
], "new-table", "New item");

// 7 Tiering
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "DoD v2" });
s.addText("Tiers by evidence, not by product name", { placeholder: "title" });
[["High risk", C.accent1, ["High-impact team type", "Correctness-critical failure types (routing, contact lifecycle, report data, agent state)", "Hotspot code"], ["All blocking checks", "Perf and chaos stage", "Invariant monitors", "Plan review with PM / Architect"]],
 ["Standard", C.text1, ["All other teams and code"], ["Common baseline (intake, fields, RCA)", "Sonar + test health", "Feature toggles"]]].forEach(([t, col, by, gets], i) => {
  const x = 0.6 + i * 6.15;
  card(s, x, 1.55, 5.95, 0.75, col, `tier-h-${i}`);
  tb(s, t, { x: x + 0.3, y: 1.55, w: 5.4, h: 0.75, fontSize: 20, bold: true, color: C.background1, valign: "middle" });
  card(s, x, 2.45, 5.95, 4.2, C.background2, `tier-b-${i}`);
  tb(s, "Assigned by", { x: x + 0.3, y: 2.6, w: 5.4, h: 0.4, fontSize: 15, bold: true });
  tb(s, by.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < by.length - 1 } })), { x: x + 0.3, y: 3.0, w: 5.4, h: 1.5, fontSize: 14, paraSpaceAfter: 4 });
  tb(s, "Gets", { x: x + 0.3, y: 4.55, w: 5.4, h: 0.4, fontSize: 15, bold: true });
  tb(s, gets.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < gets.length - 1 } })), { x: x + 0.3, y: 4.95, w: 5.4, h: 1.6, fontSize: 14, paraSpaceAfter: 4 });
});

// 8 When
s = pres.addSlide({ masterName: "CLOSE_DARK", sectionTitle: "DoD v2" });
s.addText("When the DoD v2 takes effect", { placeholder: "title" });
[["Now", ["Bug intake rule and fields", "Sonar required in every repo", "Mutation score visible in Sonar", "Go/No-Go with data", "Triage routing E2E failures"]],
 ["Q1 2027", ["Hotspot PR rules (X3)", "Bug-fix review (X4)", "Correctness monitors in shadow (X2)", "CODEOWNERS for hotspots"]],
 ["April 2027", ["Results vs control teams", "Decide which checks block, per tier", "Mutation blocking per scope, if proven", "Harness only for proven checks"]]].forEach(([t, items], i) => {
  const x = 0.6 + i * 4.1;
  tb(s, t, { x, y: 1.6, w: 3.8, h: 0.55, fontSize: 22, bold: true, color: C.accent3 });
  tb(s, items.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < items.length - 1 } })), { x, y: 2.3, w: 3.8, h: 3.8, fontSize: 16, color: C.background1, paraSpaceAfter: 8 });
});
(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
