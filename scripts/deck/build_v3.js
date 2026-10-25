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

const FOOT = "AI Quality Discovery  |  Data as of 2026-10-25  |  Sources: Jira, Confluence, GitHub, ServiceNow";

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


// ---------- 1. Title
pres.addSection({ title: "Situation" });
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Situation" });
s.addText("Product Quality 2026: What the Data Shows and a Quality Model", { placeholder: "title" });
s.addText("Management update v3  |  QA Architecture  |  25 October 2026", { placeholder: "body" });
s.addNotes("Version 2 replaces the 22 October deck. It corrects the headline numbers and replaces the gate proposal with a quality model and small experiments.");

// ---------- 2. Bottom line
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Situation" });
s.addText("Bugs got more severe; customers still find them first", { placeholder: "title" });
const stats = [
  ["+49%", "P1/P2 customer-found bugs", "Jan-Sep 2026 vs Jan-Sep 2025", C.accent1],
  ["+13%", "all customer-found bugs", "same window; MI investigations removed", C.text1],
  ["96%", "of P1 incidents reach us via customer cases", "ServiceNow, since 2025", C.accent1],
];
stats.forEach(([big, label, sub, col], i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 2.6, C.background2, `stat-${i}`);
  tb(s, big, { x: x + 0.3, y: 1.8, w: 3.2, h: 1.1, fontSize: 60, bold: true, color: col, fontFace: THEME.headFontFace });
  tb(s, label, { x: x + 0.3, y: 2.95, w: 3.2, h: 0.6, fontSize: 17, bold: true });
  tb(s, sub, { x: x + 0.3, y: 3.6, w: 3.2, h: 0.45, fontSize: 13, color: C.text2 });
});
const bl = [
  ["Severity, not volume:", " P1/P2 rose sharply; total volume rose a little and fell in Q3."],
  ["Not AI per change:", " matched comparisons show no higher bug rate for AI-made changes."],
  ["Proposal:", " a quality model with a common baseline, risk-based rules, team adaptation, and 5 experiments."],
];
bl.forEach(([k, v], i) => {
  numCircle(s, 0.6, 4.55 + i * 0.75, i + 1, i === 2 ? C.accent2 : C.text1, 0.45);
  tb(s, [{ text: k, options: { bold: true } }, { text: v }], { x: 1.25, y: 4.55 + i * 0.75, w: 11.4, h: 0.5, fontSize: 16, valign: "middle" });
});
s.addNotes("Window Jan-Sep (full quarters). Major-incident investigation tickets, logged as bugs since March 2026, are removed (they are not product defects).");

// ---------- 3. Trend
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Situation" });
s.addText("Severity broke the trend in 2026; volume did not", { placeholder: "title" });
const q = ["21Q1","21Q2","21Q3","21Q4","22Q1","22Q2","22Q3","22Q4","23Q1","23Q2","23Q3","23Q4","24Q1","24Q2","24Q3","24Q4","25Q1","25Q2","25Q3","25Q4","26Q1","26Q2","26Q3"];
const cfb = [290,325,305,324,333,337,433,348,401,334,332,297,336,360,354,363,297,274,383,425,326,410,346];
const p12 = [112,138,157,164,153,151,185,172,187,171,179,155,186,178,199,185,173,120,167,242,170,257,258];
s.addChart(pres.charts.BAR, [
  { name: "P1/P2", labels: q, values: p12 },
  { name: "P3/P4", labels: q, values: cfb.map((v, i) => v - p12[i]) },
], {
  x: 0.6, y: 1.45, w: 8.7, h: 5.35, barDir: "col", barGrouping: "stacked", barGapWidthPct: 40,
  chartColors: [H.accent1, H.accent6], showLegend: true, legendPos: "t",
  showTitle: true, title: "Customer-found bugs per quarter (MI investigations removed)", showValue: false,
  ...chartFrame, ...chartText, catAxisLabelFontSize: 10, objectName: "chart-cfb-trend",
});
card(s, 9.6, 1.45, 3.1, 5.35, C.background2, "trend-notes");
tb(s, "258 vs 167", { x: 9.85, y: 1.7, w: 2.7, h: 0.8, fontSize: 36, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
tb(s, "P1/P2 in Q3 2026 vs Q3 2025", { x: 9.85, y: 2.5, w: 2.7, h: 0.4, fontSize: 14, color: C.text2 });
tb(s, "346 vs 383", { x: 9.85, y: 3.25, w: 2.7, h: 0.8, fontSize: 36, bold: true, color: C.text1, fontFace: THEME.headFontFace });
tb(s, "all bugs in Q3 2026 vs Q3 2025", { x: 9.85, y: 4.05, w: 2.7, h: 0.4, fontSize: 14, color: C.text2 });
tb(s, "75%", { x: 9.85, y: 4.8, w: 2.7, h: 0.8, fontSize: 36, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
tb(s, "P1/P2 share in Q3 2026 (about 50% in 2023-24)", { x: 9.85, y: 5.6, w: 2.7, h: 0.7, fontSize: 14, color: C.text2 });
s.addNotes("Jira bugs with a Salesforce case. 2021-2024 counts had almost no MI investigation tickets. ServiceNow P1 incidents fell in 2026, which is not yet explained.");

// ---------- 4. Correction
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Situation" });
s.addText("Correction: our first headline counted MI investigations as bugs", { placeholder: "title" });
const mm = ["25-01","25-02","25-03","25-04","25-05","25-06","25-07","25-08","25-09","25-10","25-11","25-12","26-01","26-02","26-03","26-04","26-05","26-06","26-07","26-08","26-09","26-10"];
const mv = [0,1,0,0,2,0,0,0,0,0,0,0,0,0,6,49,34,39,48,36,38,17];
s.addChart(pres.charts.BAR, [{ name: "MI tickets", labels: mm, values: mv }], {
  x: 0.6, y: 1.45, w: 7.6, h: 5.35, barDir: "col", barGapWidthPct: 35,
  chartColors: [H.accent4], showLegend: false, showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0;-0;;",
  showTitle: true, title: "MI investigation tickets logged as customer bugs, per month", ...chartFrame, ...chartText,
  valAxisHidden: true, valGridLine: { style: "none" }, catAxisLabelFontSize: 9, objectName: "chart-mi",
});
card(s, 8.6, 1.45, 4.1, 5.35, C.background2, "corr-card");
[["Earlier (H1)", "+51% bugs, +72% P1/P2"], ["Corrected (Jan-Sep)", "+13% bugs, +49% P1/P2"], ["Why", "From March 2026, every major-incident investigation is logged as a bug with a customer case"], ["Lesson", "We now audit what enters a count before we trend it"]].forEach(([k, v], i) => {
  tb(s, k, { x: 8.9, y: 1.7 + i * 1.25, w: 3.5, h: 0.35, fontSize: 14, bold: true, color: i < 2 ? C.accent1 : C.text1 });
  tb(s, v, { x: 8.9, y: 2.05 + i * 1.25, w: 3.5, h: 0.85, fontSize: 14, color: C.text2 });
});
s.addNotes("270 such tickets in 48 projects. They were 44% of the added bugs in H1 2026. Full list of corrections: docs/06-reassessment/why-numbers-changed.md.");

// ---------- 5. What fails
pres.addSection({ title: "Findings" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Findings" });
s.addText("Almost half of valid bugs are business-correctness failures", { placeholder: "title" });
const ft = [["Billing",4,1],["Agent state",18,1],["WFM",33,1],["Security",39,0],["Performance",50,0],["Contact lifecycle",75,1],["Routing",86,1],["Integration",87,0],["Availability",101,0],["Recording / QM",111,1],["UI",208,0],["Other function",354,0],["Report / data",399,1]];
s.addChart(pres.charts.BAR, [
  { name: "Correctness", labels: ft.map(r => r[0]), values: ft.map(r => (r[2] ? r[1] : 0)) },
  { name: "Other", labels: ft.map(r => r[0]), values: ft.map(r => (r[2] ? 0 : r[1])) },
], {
  x: 0.6, y: 1.45, w: 7.6, h: 5.35, barDir: "bar", barGrouping: "stacked", barGapWidthPct: 30,
  chartColors: [H.accent1, H.accent6], showLegend: true, legendPos: "t", showValue: false,
  showTitle: true, title: "Valid customer-found bugs by failure type, 2025-2026", ...chartFrame, ...chartText,
  catAxisLabelFontSize: 11, objectName: "chart-types",
});
card(s, 8.6, 1.45, 4.1, 5.35, C.background2, "types-card");
[["73%", "of routing bugs are P1/P2 (highest)"], ["11", "incidents per agent-state bug"], ["52% -> 70%", "P1/P2 share of correctness bugs, 2025 -> 2026"]].forEach(([b, l], i) => {
  tb(s, b, { x: 8.9, y: 1.7 + i * 1.7, w: 3.5, h: 0.8, fontSize: 34, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  tb(s, l, { x: 8.9, y: 2.5 + i * 1.7, w: 3.5, h: 0.6, fontSize: 14, color: C.text2 });
});
s.addNotes("1,565 valid bugs, 13 types, 93-95% label precision on a sample. About 15% of all reports are expectation or documentation gaps closed as 'works as designed' - not in this chart.");

// ---------- 6. Teams differ
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Findings" });
s.addText("Teams differ too much for one workflow", { placeholder: "title" });
const rng = [["1.1 - 10.4", "incidents per bug"], ["10 - 93%", "P1/P2 share"], ["6 - 79%", "invalid bug share"], ["3 - 31", "days to fix (median)"]];
rng.forEach(([b, l], i) => {
  const x = 0.6 + i * 3.07;
  card(s, x, 1.55, 2.85, 1.9, C.background2, `rng-${i}`);
  tb(s, b, { x: x + 0.25, y: 1.75, w: 2.4, h: 0.8, fontSize: 30, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  tb(s, l, { x: x + 0.25, y: 2.6, w: 2.4, h: 0.5, fontSize: 14, color: C.text2 });
});
tb(s, "Range across 40 teams. The VP explains only 17-46% of this variation; most of it is inside a VP.", { x: 0.6, y: 3.65, w: 12.1, h: 0.4, fontSize: 14, color: C.text2 });
const arch = [["High impact", "9 teams", "Severity and incidents above median"], ["Fast growing", "8 teams", "Valid bugs +50% or more; part is re-homing"], ["High noise", "5 teams", "Half or more of bugs invalid"], ["Stable", "18 teams", "No extra signal"]];
arch.forEach(([t, n, d], i) => {
  const x = 0.6 + i * 3.07;
  card(s, x, 4.3, 2.85, 2.35, C.text1, `arch-${i}`);
  tb(s, t, { x: x + 0.25, y: 4.5, w: 2.4, h: 0.45, fontSize: 17, bold: true, color: C.background1 });
  tb(s, n, { x: x + 0.25, y: 4.95, w: 2.4, h: 0.4, fontSize: 14, bold: true, color: C.accent3 });
  tb(s, d, { x: x + 0.25, y: 5.4, w: 2.4, h: 1.1, fontSize: 14, color: C.accent6 });
});
s.addNotes("40 teams with at least 10 valid bugs in 2025-2026. No maintained team-to-service-to-code map exists; Jira Team Name is the best key today.");

// ---------- 7. AI
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Findings" });
s.addText("AI: what is fact, what is correlation, what is hypothesis", { placeholder: "title" });
const ai = [
  ["FACT", "AI use grew from about 0% to 31-47% of work in 2026", C.text1],
  ["FACT", "AI labels on bugs mark AI-made fixes, not AI-caused bugs", C.text1],
  ["NOT SUPPORTED", "AI changes cause more bugs per change (matched ratio 0.78-0.84)", C.accent2],
  ["NOT SUPPORTED", "AI adoption caused the 2026 rise (adopting teams stayed flat)", C.accent2],
  ["WEAK SIGNAL", "Same author: AI PRs need more follow-up fixes (1.45, CI touches 1)", C.accent3],
  ["MECHANISM", "AI PRs are 3.7x larger and 47% of PRs into hotspot code; review does not grow with size", C.accent1],
];
ai.forEach(([k, v, col], i) => {
  const y = 1.5 + i * 0.86;
  card(s, 0.6, y, 2.6, 0.7, col, `ai-k-${i}`);
  tb(s, k, { x: 0.6, y, w: 2.6, h: 0.7, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle" });
  tb(s, v, { x: 3.45, y, w: 9.2, h: 0.7, fontSize: 16, valign: "middle" });
});
s.addNotes("Low-Medium confidence: few AI-caused bugs so far. Re-test with a 90-day window in 2027-Q1. No company page sets size or review rules for AI-written code.");

// ---------- 8. Dimensions
pres.addSection({ title: "Quality model" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Quality model" });
s.addText("Quality = 8 outcome dimensions, each tied to a decision", { placeholder: "title" });
const dims = [
  ["Business correctness", "Where to invest first", "295 -> 325 valid; P1/P2 52% -> 70%"],
  ["Availability", "Reliability, release risk", "Counts only (access)"],
  ["Performance", "Capacity work", "No SLO data yet"],
  ["Detection", "Monitoring investment", "96% of P1 via customer cases"],
  ["Recovery", "Response capacity", "P1 71% < 4 h; fix median 10 days"],
  ["Change safety", "Review depth for fixes", "1 in 4 causes is a fix; emergency x2.9"],
  ["Non-recurrence", "Do fixes hold", "1-2% return; flat"],
  ["Expectation fit", "Requirements and docs", "~15% of reports are real gaps"],
];
s.addTable([
  [{ text: "Dimension", options: { bold: true, color: H.lt1, fill: { color: H.dk1 } } }, { text: "Decision it supports", options: { bold: true, color: H.lt1, fill: { color: H.dk1 } } }, { text: "2025 -> 2026", options: { bold: true, color: H.lt1, fill: { color: H.dk1 } } }],
  ...dims.map(([a, b, c], i) => [{ text: a, options: { bold: true, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }, { text: b, options: { fill: { color: i % 2 ? H.lt1 : H.lt2 } } }, { text: c, options: { fill: { color: i % 2 ? H.lt1 : H.lt2 } } }]),
], { x: 0.6, y: 1.5, w: 12.1, colW: [3.2, 3.9, 5.0], fontSize: 14, color: H.dk1, rowH: 0.52, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "dims-table" });
tb(s, "Code quality, coverage and tool scores are inputs that may explain these outcomes. They are not quality.", { x: 0.6, y: 6.35, w: 12.1, h: 0.4, fontSize: 14, color: C.text2 });
s.addNotes("Each dimension has a metric, evidence source, baseline, limits and owner in docs/07-quality-model/quality-model-v0.md. No fixed targets yet: each team is compared with its own 2025 baseline.");

// ---------- 9. Three layers
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Quality model" });
s.addText("Common where it adds value, different where risk differs", { placeholder: "title" });
const layers = [
  ["Common baseline", "All teams", ["One intake rule: defect vs MI vs expectation gap", "Each bug: type, detected-by, cause, customers", "RCA for P1/P2 (already uniform)", "Team -> service -> code map"], C.text1],
  ["Risk-based layer", "Any team, by risk", ["High-severity correctness failures", "Hotspot code: review scales with size", "Bug fixes: regression evidence", "Emergency changes: follow-up review"], C.accent1],
  ["Team adaptation", "By archetype", ["High impact: detection and recovery", "Fast growing: check re-homing, then triage", "High noise: expectation gaps first", "Stable: baseline only"], C.accent2],
];
layers.forEach(([t, sub, items, col], i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.55, 3.8, 0.95, col, `layer-h-${i}`);
  tb(s, t, { x: x + 0.25, y: 1.62, w: 3.3, h: 0.45, fontSize: 19, bold: true, color: C.background1 });
  tb(s, sub, { x: x + 0.25, y: 2.05, w: 3.3, h: 0.35, fontSize: 13, color: C.background1 });
  card(s, x, 2.65, 3.8, 2.75, C.background2, `layer-b-${i}`);
  tb(s, items.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < items.length - 1 } })), { x: x + 0.2, y: 2.85, w: 3.4, h: 2.45, fontSize: 15, paraSpaceAfter: 8 });
});
tb(s, "Teams choose how to meet a rule. The model fixes what must be true and how it is measured. Rules apply to all authors, human or AI.", { x: 0.6, y: 5.65, w: 12.1, h: 0.4, fontSize: 14, color: C.text2 });
s.addNotes("Common items make outcomes comparable; the 2026 headline error came from mixed intake. Risk triggers come from data: routing 73% P1/P2, follow-up fixes rise with size only in hotspot code, 1 in 4 known causes is a fix.");

// ---------- 10. Experiments
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Quality model" });
s.addText("Five experiments, redesigned so the data can show a result", { placeholder: "title" });
const hdr = (t) => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk1 } } });
const xs = [
  ["X1 Intake fields", "3 teams (one per type) vs 3 controls", "Bugs with cause and detected-by (15% today)", "1 quarter"],
  ["X2 Detection", "1 high-impact team, shadow mode", "Alerts before a customer case; lead time", "6 weeks + 1 quarter"],
  ["X3 Review by size", "All teams with hotspot PRs, 2-step start", "Follow-up fixes per hotspot PR (about 70%)", "2 quarters"],
  ["X4 Fix safety", "Same pool, bug-fix PRs only", "Follow-up fixes per bug-fix PR", "2 quarters"],
  ["X5 Expectation gaps", "5 high-noise teams + VMS/QM, WFM", "Share of 'works as designed' closures with an action", "1 quarter"],
];
s.addTable([
  [hdr("Experiment"), hdr("Arms"), hdr("Primary measure"), hdr("Duration")],
  ...xs.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
], { x: 0.6, y: 1.5, w: 12.1, colW: [2.6, 3.6, 4.2, 1.7], fontSize: 14, color: H.dk1, rowH: 0.6, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "exp-table" });
card(s, 0.6, 5.35, 12.1, 1.35, C.background2, "power-note");
tb(s, [{ text: "Power check: ", options: { bold: true, color: H.accent1 } }, { text: "bugs are rare per team, so 1 team for 1 quarter cannot show a 30% change for X2-X5 (4 to 33 quarters needed). The new design pools teams and measures events with more volume. Bug counts stay as the slower confirming signal. Each experiment is pre-registered with success and stop rules." }], { x: 0.85, y: 5.45, w: 11.6, h: 1.15, fontSize: 14, valign: "middle" });
s.addNotes("Protocols: docs/07-quality-model/experiment-protocols-v0.md (D-038). Candidates and matched controls come from data (agg_exp_readiness). A practice spreads only when it beats its control.");

// ---------- 11. Keep / Change / Stop / Start
pres.addSection({ title: "Action plan" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Action plan" });
s.addText("What to keep, change, stop and start", { placeholder: "title" });
const kcss = [
  ["Keep", C.accent2, ["RCA for P1/P2 bugs (80-100% today)", "Feature toggles (no monolith rollback)", "AI development, same rules as all changes", "Xray test management"]],
  ["Change", C.accent3, ["Intake: defect vs MI vs expectation gap", "Go/No-Go: from \"TBD\" to data", "E2E: trusted signal before blocking", "Review depth scales with size in hotspots", "QSU: valid, severity-weighted, per team"]],
  ["Stop", C.accent1, ["Raw bug count as the quality number", "One gate set for all teams", "Unused Jira quality fields (9 of 15)", "\"Mandatory\" with no control behind it"]],
  ["Start", C.text1, ["8-dimension quality model", "Team -> service -> code map", "Monitors for routing, lifecycle, data", "Expectation-gap triage; owner backups", "Experiments X1-X5"]],
];
kcss.forEach(([t, col, items], i) => {
  const x = 0.6 + i * 3.07;
  card(s, x, 1.5, 2.85, 0.7, col, `kcss-h-${i}`);
  tb(s, t, { x, y: 1.5, w: 2.85, h: 0.7, fontSize: 20, bold: true, color: C.background1, align: "center", valign: "middle" });
  card(s, x, 2.35, 2.85, 3.4, C.background2, `kcss-b-${i}`);
  tb(s, items.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < items.length - 1 } })), { x: x + 0.15, y: 2.5, w: 2.6, h: 3.15, fontSize: 15, paraSpaceAfter: 8 });
});
s.addNotes("Evidence per line: docs/05-summary/action-plan-v1.md section 2.");

// ---------- 12. Gates and automation
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Action plan" });
s.addText("Our gates and quality automation: means, not goals", { placeholder: "title" });
const gm = [
  ["Gates (G1-G6)", "Few blocking checks where risk is proven: intake fields, hotspot size and review", "Now"],
  ["Go/No-Go", "Data-based: 8 dimensions, open P1-P3, E2E health", "Now"],
  ["E2E automation", "Repair trust first; then block on suites that hold their pass level", "Now -> Q1"],
  ["Sonar, dependency scan", "Keep as build checks", "Keep"],
  ["RIA agents", "Later, aimed at fixes and hotspots (RIA misses = 7%)", "H2 2027"],
  ["Mutation testing", "Later, only if X3/X4 show weak tests (weak tests = 3%)", "H2 2027"],
  ["Agent harness", "Build only for checks that experiments prove", "H2 2027"],
];
const gh = (t) => ({ text: t, options: { bold: true, color: H.lt1, fill: { color: H.dk1 } } });
s.addTable([
  [gh("Means"), gh("Recommendation"), gh("When")],
  ...gm.map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
], { x: 0.6, y: 1.5, w: 12.1, colW: [2.8, 7.6, 1.7], fontSize: 14, color: H.dk1, rowH: 0.6, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "means-table" });
tb(s, "Blocking is justified only where data proves the risk. Everything else waits for the experiment results.", { x: 0.6, y: 6.45, w: 12.1, h: 0.4, fontSize: 14, color: C.text2 });
s.addNotes("This answers how our current gate methodology and quality automation fit: they stay as possible means, applied where the evidence shows risk.");

// ---------- 13. When
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Action plan" });
s.addText("When: measure first, test in a few teams, then spread", { placeholder: "title" });
const ph = [
  ["Now", "Nov 2026", ["Decisions: sponsor, X1-X5, ServiceNow access, team map", "Start X1 intake and X2 detection (shadow)", "QSU: valid, severity-weighted, per team", "Triage 13 failing routing E2E scenarios"]],
  ["Q1 2027", "Jan-Mar", ["X3/X4 step 1 (hotspot and bug-fix PRs)", "X5 with product owners", "Monthly quality review per team", "Re-test the AI effect (90 days)"]],
  ["Q2 2027", "April review", ["X3/X4 step 2", "Results vs controls", "Model v1 with justified targets", "Decide which checks block"]],
  ["H2 2027", "Jul-Dec", ["Spread proven practices to all domains", "Decide RIA agents, mutation, harness from evidence"]],
];
ph.forEach(([t, sub, items], i) => {
  const x = 0.6 + i * 3.07;
  s.addShape(pres.shapes.CHEVRON, { x, y: 1.5, w: 2.95, h: 0.85, fill: { color: i === 0 ? H.accent1 : H.dk1 }, line: { color: i === 0 ? H.accent1 : H.dk1 }, objectName: `phase-${i}` });
  tb(s, t, { x: x + 0.3, y: 1.5, w: 2.35, h: 0.85, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle" });
  tb(s, sub, { x, y: 2.45, w: 2.85, h: 0.35, fontSize: 13, color: C.text2, align: "center" });
  card(s, x, 2.9, 2.85, 3.1, C.background2, `phase-b-${i}`);
  tb(s, items.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < items.length - 1 } })), { x: x + 0.15, y: 3.05, w: 2.6, h: 2.85, fontSize: 15, paraSpaceAfter: 8 });
});
s.addNotes("Success by April 2027: every valid bug records type, detected-by and cause; each team sees its 8 dimensions monthly; one correctness type is detected before customers; X1-X5 have results with confidence intervals.");

// ---------- 11. Asks
pres.addSection({ title: "Decisions" });
s = pres.addSlide({ masterName: "CLOSE_DARK", sectionTitle: "Decisions" });
s.addText("What we need from management", { placeholder: "title" });
const asks = [
  ["Approve experiments X1-X5 in volunteer teams", "1 quarter; no org-wide change yet"],
  ["Grant ServiceNow record-level read for research", "Needed for who was affected and change-to-incident links"],
  ["Name an owner for the team-to-service-to-code map", "No such map exists today"],
  ["Name a sponsor and a monthly quality review", "Each team vs its own baseline, 8 dimensions"],
];
asks.forEach(([t, d], i) => {
  const y = 1.6 + i * 1.15;
  numCircle(s, 0.6, y + 0.05, i + 1, C.accent3, 0.55);
  tb(s, t, { x: 1.4, y, w: 6.6, h: 0.45, fontSize: 18, bold: true, color: C.background1 });
  tb(s, d, { x: 1.4, y: y + 0.48, w: 6.6, h: 0.4, fontSize: 14, color: C.accent6 });
});
card(s, 8.4, 1.6, 4.3, 4.45, H.dk2, "timeline");
tb(s, "Timeline", { x: 8.7, y: 1.8, w: 3.7, h: 0.45, fontSize: 18, bold: true, color: C.background1 });
[["Now", "Start X1-X5"], ["2027-Q1", "Re-test the AI effect (90 days)"], ["2027-04", "Review experiments vs controls"], ["Then", "Spread what worked; model v1"]].forEach(([w, d], i) => {
  tb(s, w, { x: 8.7, y: 2.45 + i * 0.85, w: 1.2, h: 0.7, fontSize: 15, bold: true, color: C.accent3 });
  tb(s, d, { x: 9.95, y: 2.45 + i * 0.85, w: 2.55, h: 0.7, fontSize: 14, color: C.background1 });
});
s.addNotes("Nothing has been changed in company systems. All data, scripts and decisions are in the research repository.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
