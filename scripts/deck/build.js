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

const FOOT = "AI Quality Discovery  |  Data as of 2026-10-22  |  Sources: Jira, Confluence, GitHub";

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
s.addText("Software Quality 2026: What the Data Shows and What Must Change", { placeholder: "title" });
s.addText("Research summary for management  |  QA Architecture  |  22 October 2026", { placeholder: "body" });
s.addNotes("Purpose: share what 9 years of customer-found bug data, our code history and our CI runs show, and agree on the next decisions. All numbers come from read-only queries; detail is in the research repository.");

// ---------- 2. Bottom line
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Situation" });
s.addText("More and worse customer bugs; controls did not keep up", { placeholder: "title" });
const stats = [
  ["+51%", "customer-found bugs", "H1 2026 vs H1 2025", C.accent1],
  ["+72%", "P1/P2 customer-found bugs", "H1 2026 vs H1 2025", C.accent1],
  ["2.4x", "more delivered stories", "2024-Q3 to 2026-Q3", C.text1],
];
stats.forEach(([big, label, sub, col], i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.6, 3.8, 2.6, C.background2, `stat-${i}`);
  tb(s, big, { x: x + 0.3, y: 1.8, w: 3.2, h: 1.1, fontSize: 60, bold: true, color: col, fontFace: THEME.headFontFace });
  tb(s, label, { x: x + 0.3, y: 2.95, w: 3.2, h: 0.5, fontSize: 18, bold: true });
  tb(s, sub, { x: x + 0.3, y: 3.5, w: 3.2, h: 0.4, fontSize: 13, color: C.text2 });
});
const bl = [
  ["Not AI:", " AI-made changes are not riskier per change (ratio 1.03). AI adds volume."],
  ["Real cause:", " change volume grew, but quality controls stayed on paper. No check blocks bad changes."],
  ["Fix:", " add 7 blocking gates, make tests trustworthy, own the hotspot code. Pilot first, review in April 2027."],
];
bl.forEach(([k, v], i) => {
  numCircle(s, 0.6, 4.55 + i * 0.75, i + 1, i === 2 ? C.accent2 : C.text1, 0.45);
  tb(s, [{ text: k, options: { bold: true } }, { text: v }], { x: 1.25, y: 4.55 + i * 0.75, w: 11.4, h: 0.5, fontSize: 16, valign: "middle" });
});
s.addNotes("Bottom line. Five flat years (about 1,300 customer-found bugs per year), then 2026 broke the trend. Severity grew faster than volume. AI is not the per-change cause; the gap is controls that do not scale with volume.");

// ---------- 3. Trend chart
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Situation" });
s.addText("2026 broke a five-year flat line, and severity rose faster", { placeholder: "title" });
const q = ["21Q1","21Q2","21Q3","21Q4","22Q1","22Q2","22Q3","22Q4","23Q1","23Q2","23Q3","23Q4","24Q1","24Q2","24Q3","24Q4","25Q1","25Q2","25Q3","25Q4","26Q1","26Q2","26Q3"];
const cfb = [290,325,305,324,333,337,433,348,401,334,332,297,336,360,354,363,298,276,383,425,332,532,468];
const p12 = [112,138,157,164,153,151,185,172,187,171,179,155,186,178,199,185,174,122,167,242,175,334,316];
s.addChart(pres.charts.BAR, [
  { name: "P1/P2", labels: q, values: p12 },
  { name: "P3/P4", labels: q, values: cfb.map((v, i) => v - p12[i]) },
], {
  x: 0.6, y: 1.45, w: 8.7, h: 5.35, barDir: "col", barGrouping: "stacked", barGapWidthPct: 40,
  chartColors: [H.accent1, H.accent6], showLegend: true, legendPos: "t",
  showTitle: true, title: "Customer-found bugs created per quarter", showValue: false,
  ...chartFrame, ...chartText, catAxisLabelFontSize: 10, objectName: "chart-cfb-trend",
});
card(s, 9.6, 1.45, 3.1, 5.35, C.background2, "trend-notes");
tb(s, "532", { x: 9.85, y: 1.7, w: 2.7, h: 0.8, fontSize: 44, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
tb(s, "record quarter (2026-Q2)", { x: 9.85, y: 2.5, w: 2.7, h: 0.4, fontSize: 14, color: C.text2 });
tb(s, "68%", { x: 9.85, y: 3.15, w: 2.7, h: 0.8, fontSize: 44, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
tb(s, "P1/P2 share in 2026-Q3 (about 50% in 2023-24)", { x: 9.85, y: 3.95, w: 2.7, h: 0.7, fontSize: 14, color: C.text2 });
tb(s, "~1,300", { x: 9.85, y: 4.85, w: 2.7, h: 0.8, fontSize: 44, bold: true, color: C.text1, fontFace: THEME.headFontFace });
tb(s, "per year, flat 2021-2025", { x: 9.85, y: 5.65, w: 2.7, h: 0.4, fontSize: 14, color: C.text2 });
s.addNotes("Source: Jira, issuetype = Bug with a Salesforce case link (11,662 bugs since 2017). Two bulk imports (projects ENG and CGY) were checked and do not affect these counts.");

// ---------- 4. Concentration
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Situation" });
s.addText("Three R&D domains produce 60% of customer-found bugs", { placeholder: "title" });
const vps = ["VMS, Rec, QM & FM", "APQ", "LiveVox & Digital", "AHW", "WFM", "Orchestration Core", "Analytics and Data"];
const vpv = [99, 120, 138, 250, 281, 296, 473];
s.addChart(pres.charts.BAR, [{ name: "CFB", labels: vps, values: vpv }], {
  x: 0.6, y: 1.45, w: 7.4, h: 5.35, barDir: "bar", barGapWidthPct: 35,
  chartColors: [H.accent4], showLegend: false, showValue: true, dataLabelPosition: "outEnd",
  showTitle: true, title: "Customer-found bugs by R&D VP, last 12 months", ...chartFrame, ...chartText,
  valAxisHidden: true, valGridLine: { style: "none" }, catAxisLabelFontSize: 12, objectName: "chart-vp",
});
card(s, 8.4, 1.45, 4.3, 5.35, C.text1, "pilot-card");
tb(s, "Pilot: Orchestration Core", { x: 8.7, y: 1.7, w: 3.8, h: 0.5, fontSize: 20, bold: true, color: C.background1 });
tb(s, "Contact routing and lifecycle flow", { x: 8.7, y: 2.2, w: 3.8, h: 0.4, fontSize: 14, color: C.accent6 });
[["70%", "of its bugs are P1/P2"], ["3.8", "incidents per bug"], ["+34%", "valid bugs in 12 months"]].forEach(([b, l], i) => {
  tb(s, b, { x: 8.7, y: 2.9 + i * 1.25, w: 3.8, h: 0.7, fontSize: 36, bold: true, color: C.accent3, fontFace: THEME.headFontFace });
  tb(s, l, { x: 8.7, y: 3.6 + i * 1.25, w: 3.8, h: 0.4, fontSize: 14, color: C.background1 });
});
s.addNotes("Window: 22 Oct 2025 to 22 Oct 2026, 1,760 bugs (+34% vs the year before). Orchestration Core was chosen as pilot: highest severity and incident load. 51% of its bugs close as invalid (mostly duplicates of the same incident), so we track valid bugs.");

// ---------- 5. Causes
pres.addSection({ title: "Causes" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Causes" });
s.addText("Seven causes, ranked by the strength of the evidence", { placeholder: "title" });
const causes = [
  ["Controls exist on paper only", "9 of ~15 Jira quality fields < 2% filled; no blocking gate"],
  ["The test signal is broken", "Routing E2E passes 1.2% of runs; failures are ignored"],
  ["Real scenarios are not tested", "28-31% of escaped bugs"],
  ["State races, monolith vs new services", "21% of valid pilot bugs; no per-contact version"],
  ["Big changes into hotspot code", "Follow-up fixes 21% (small PRs) to 54% (> 1,000 lines)"],
  ["Knowledge sits with 1-2 people", "Bus factor 1 on the VC-to-VC sync code"],
  ["Production conditions not reproduced", "No performance or chaos test workflow"],
];
causes.forEach(([t, e], i) => {
  const col = i < 4 ? 0 : 1;
  const row = i < 4 ? i : i - 4;
  const x = 0.6 + col * 6.2;
  const y = 1.55 + row * 1.3;
  numCircle(s, x, y + 0.1, i + 1, i < 2 ? C.accent1 : C.text1, 0.55);
  tb(s, t, { x: x + 0.8, y, w: 5.2, h: 0.45, fontSize: 17, bold: true });
  tb(s, e, { x: x + 0.8, y: y + 0.5, w: 5.2, h: 0.6, fontSize: 14, color: C.text2 });
});
card(s, 6.8, 5.45, 5.9, 1.25, C.background2, "ai-note");
tb(s, [{ text: "Not a cause per change: ", options: { bold: true } }, { text: "AI-assisted development. AI changes cause bugs at the same rate (ratio 1.03) and need fewer follow-up fixes (0.67)." }], { x: 7.0, y: 5.6, w: 5.5, h: 1.0, fontSize: 14, valign: "middle" });
s.addNotes("Evidence: 321 classified root-cause analyses (two blind raters agreed 85%), 7,866 commits, 1,663 pull requests and 2,837 CI runs. Causes 1 and 2 explain why the others reach customers.");

// ---------- 6. AI
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Causes" });
s.addText("AI is not riskier per change, but it multiplies change volume", { placeholder: "title" });
const aq = ["25Q1","25Q2","25Q3","25Q4","26Q1","26Q2","26Q3"];
s.addChart(pres.charts.BAR, [{ name: "AI share of resolved stories (%)", labels: aq, values: [0.2, 0.3, 0.4, 2.0, 10.2, 31.3, 22.8] }], {
  x: 0.6, y: 1.45, w: 6.6, h: 5.35, barDir: "col", barGapWidthPct: 45,
  chartColors: [H.accent2], showLegend: false, showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.0\"%\"",
  showTitle: true, title: "AI-implemented share of resolved stories (%)", ...chartFrame, ...chartText,
  valAxisHidden: true, valGridLine: { style: "none" }, objectName: "chart-ai-share",
});
const aiStats = [
  ["1.03", "bug rate ratio, AI vs other changes", "95% CI 0.57-1.86", C.accent2],
  ["0.67", "follow-up fixes after AI PRs vs others", "95% CI 0.47-0.95", C.accent2],
  ["3.7x", "larger AI PRs; review per line not higher", "Risk to watch", C.accent1],
];
aiStats.forEach(([b, l, sub, col], i) => {
  const y = 1.45 + i * 1.83;
  card(s, 7.6, y, 5.1, 1.6, C.background2, `ai-stat-${i}`);
  tb(s, b, { x: 7.85, y: y + 0.2, w: 1.7, h: 1.2, fontSize: 40, bold: true, color: col, valign: "middle", fontFace: THEME.headFontFace });
  tb(s, l, { x: 9.65, y: y + 0.25, w: 2.9, h: 0.75, fontSize: 15, bold: true });
  tb(s, sub, { x: 9.65, y: y + 1.0, w: 2.9, h: 0.4, fontSize: 13, color: C.text2 });
});
s.addNotes("AI pull requests in the pilot repos went from 0-5% in 2025 to 46% in 2026-Q3, and to 51% in the top hotspot code. Confidence on the AI comparison is Low-Medium (few AI-caused bugs so far); re-test with a 90-day window in 2027-Q1.");

// ---------- 7. Size risk
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Causes" });
s.addText("The real risk: big changes into hotspot code, by anyone", { placeholder: "title" });
const sb = ["0-50", "51-150", "151-400", "401-1,000", "> 1,000"];
s.addChart(pres.charts.BAR, [
  { name: "Hotspot code", labels: sb, values: [20.7, 17.3, 27.1, 33.3, 53.8] },
  { name: "Other code", labels: sb, values: [3.7, 3.1, 4.2, 5.1, 5.5] },
], {
  x: 0.6, y: 1.45, w: 8.2, h: 5.35, barDir: "col", barGapWidthPct: 50,
  chartColors: [H.accent1, H.accent6], showLegend: true, legendPos: "t", showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0\"%\"",
  showTitle: true, title: "PRs followed by a customer-bug fix within 30 days, by PR size (lines)", ...chartFrame, ...chartText,
  valAxisHidden: true, valGridLine: { style: "none" }, objectName: "chart-size-risk",
});
card(s, 9.2, 1.45, 3.5, 5.35, C.background2, "size-notes");
tb(s, "54% vs 6%", { x: 9.45, y: 1.7, w: 3.0, h: 0.8, fontSize: 34, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
tb(s, "large PRs in hotspot code vs other code", { x: 9.45, y: 2.5, w: 3.0, h: 0.7, fontSize: 14, color: C.text2 });
tb(s, "39% vs 11%", { x: 9.45, y: 3.45, w: 3.0, h: 0.8, fontSize: 34, bold: true, color: C.text1, fontFace: THEME.headFontFace });
tb(s, "large non-AI vs large AI PRs: rules must cover all PRs", { x: 9.45, y: 4.25, w: 3.0, h: 0.9, fontSize: 14, color: C.text2 });
tb(s, "Review comments per 100 lines fall from 3.3 to 0.03 as PRs grow.", { x: 9.45, y: 5.4, w: 3.0, h: 1.1, fontSize: 14, color: C.text1 });
s.addNotes("Hotspot code = the 10 pilot directories with the most customer-bug fixes (for example the VC-to-VC sync, ACD provider, AFM service). 1,663 merged PRs, 2025-2026.");

// ---------- 8. Controls today
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Causes" });
s.addText("Our controls exist on paper, not in the pipeline", { placeholder: "title" });
const tiles = [
  ["0%", "of Stories have a regression impact analysis"],
  ["9 of 15", "Jira quality fields filled on < 2% of items"],
  ["1.2%", "pass rate of the routing E2E pipeline"],
  ["\"TBD\"", "status on all 26.4 domain Go/No-Go pages"],
  ["None", "code owners file in the monolith"],
  ["2.7%", "of bugs link the change that caused them"],
];
tiles.forEach(([b, l], i) => {
  const x = 0.6 + (i % 3) * 4.1;
  const y = 1.55 + Math.floor(i / 3) * 2.65;
  card(s, x, y, 3.8, 2.35, C.background2, `tile-${i}`);
  tb(s, b, { x: x + 0.3, y: y + 0.25, w: 3.2, h: 0.95, fontSize: 44, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  tb(s, l, { x: x + 0.3, y: y + 1.3, w: 3.2, h: 0.8, fontSize: 15 });
});
s.addNotes("The only blocking automated checks found are opt-in local hooks (Sonar, Aikido). The release gate is a human decision. RCA is filled on 89% of fixed bugs but reviewed on 33%.");

// ---------- 9. Gates
pres.addSection({ title: "Actions" });
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Actions" });
s.addText("Seven gates that block work when a check fails", { placeholder: "title" });
const gates = [
  ["G1", "Design", "State, ordering and toggle section; named owners"],
  ["G2", "Pull request", "Hotspot code: <= 400 lines, owner approval, tests, Jira key"],
  ["G3", "Build", "Unit, contract and ordering tests; Sonar; secret scan"],
  ["G4", "Test health", "A suite blocks only at >= 95% pass over 14 days"],
  ["G5", "Pre-release", "Fault and load stage; data-based Go/No-Go"],
  ["G6", "Deploy", "Toggle, progressive rollout, monitors green"],
  ["G7", "Escape", "A customer bug closes only with a linked test"],
];
const gw = 1.62, gg = 0.13;
gates.forEach(([id, name, chk], i) => {
  const x = 0.6 + i * (gw + gg);
  s.addShape(pres.shapes.CHEVRON, { x, y: 1.6, w: gw, h: 0.85, fill: { color: i < 4 ? H.dk1 : H.accent2 }, line: { color: i < 4 ? H.dk1 : H.accent2 }, objectName: `gate-${id}` });
  tb(s, id, { x: x + 0.25, y: 1.6, w: gw - 0.5, h: 0.85, align: "center", valign: "middle", fontSize: 18, bold: true, color: C.background1 });
  card(s, x, 2.65, gw, 2.45, C.background2, `gate-card-${id}`);
  tb(s, name, { x: x + 0.12, y: 2.8, w: gw - 0.24, h: 0.5, fontSize: 15, bold: true });
  tb(s, chk, { x: x + 0.12, y: 3.35, w: gw - 0.24, h: 1.65, fontSize: 13, color: C.text2 });
});
tb(s, "Code and CI (G1-G4)", { x: 0.6, y: 5.35, w: 6.8, h: 0.35, fontSize: 13, bold: true, color: C.text1 });
tb(s, "Release and production (G5-G7)", { x: 7.6, y: 5.35, w: 5.1, h: 0.35, fontSize: 13, bold: true, color: C.accent2 });
tb(s, "Not now: regression-impact agents (7% of escapes) and mutation testing (3%). Add later only if the measures show the need.", { x: 0.6, y: 6.0, w: 12.1, h: 0.4, fontSize: 14, color: C.text2 });
s.addNotes("A gate is a check that stops the work. A policy without a stop is not a gate. Each gate maps to a cause on slide 5. The monolith cannot roll back, so G6 relies on feature toggles and progressive rollout.");

// ---------- 10. Also needed
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Actions" });
s.addText("Also needed: governance gaps the data revealed", { placeholder: "title" });
const gaps = [
  ["Governance", "Name a sponsor and a quality owner per critical flow; review 7 measures monthly"],
  ["Bug data", "51% of pilot bugs invalid; require cause and incident links; dedupe"],
  ["Detection", "SLOs and alerts per critical flow; record who detected each bug"],
  ["Migrations", "Rollout register; parity checks during dual-run"],
  ["AI governance", "One AI label (14 variants today); AI question in root-cause analysis"],
  ["Knowledge", "Backup owner per hotspot; design notes for the VC core"],
  ["Security", "Secret scanning in Jira and Confluence (credentials found)"],
  ["Data platform", "Monthly automated refresh; add Sonar, CI/CD and incident data"],
];
gaps.forEach(([t, d], i) => {
  const x = 0.6 + (i % 4) * 3.07;
  const y = 1.75 + Math.floor(i / 4) * 2.45;
  card(s, x, y, 2.85, 2.15, C.background2, `gap-${i}`);
  numCircle(s, x + 0.25, y + 0.25, i + 1, C.accent2, 0.45);
  tb(s, t, { x: x + 0.85, y: y + 0.25, w: 1.85, h: 0.45, fontSize: 16, bold: true, valign: "middle" });
  tb(s, d, { x: x + 0.25, y: y + 0.9, w: 2.4, h: 1.1, fontSize: 14, color: C.text2 });
});
s.addNotes("These were not in the original scope but block lasting improvement. The research database built in this initiative is the seed for item 8.");

// ---------- 11. End goal
s = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Actions" });
s.addText("End goal: rare escapes, caught early, never repeated", { placeholder: "title" });
tb(s, "Zero production bugs is not a realistic target. These five measures are, and we already have their baselines.", { x: 0.6, y: 1.45, w: 12.1, h: 0.5, fontSize: 16, color: C.text2 });
const goals = [
  ["Fewer escapes", "8.9", "<= 9", "valid pilot bugs per month (13 since May 2026); then -50% vs 2025"],
  ["No repeats", "38%", ">= 90%", "valid bugs closed with a regression test"],
  ["Caught first", "?", ">= 50%", "bugs found by monitoring before customers (baseline missing)"],
  ["Less impact", "3.8", "<= 2.5", "incidents per pilot bug"],
  ["Trusted tests", "1.2-79%", ">= 95%", "E2E pass rate over 14 days"],
];
goals.forEach(([t, base, target, d], i) => {
  const x = 0.6 + i * 2.46;
  card(s, x, 2.2, 2.25, 4.5, C.background2, `goal-${i}`);
  tb(s, t, { x: x + 0.2, y: 2.4, w: 1.85, h: 0.45, fontSize: 16, bold: true });
  tb(s, "Today", { x: x + 0.2, y: 3.0, w: 1.85, h: 0.3, fontSize: 12, color: C.text2 });
  tb(s, base, { x: x + 0.2, y: 3.3, w: 1.85, h: 0.6, fontSize: 26, bold: true, color: C.accent1, fontFace: THEME.headFontFace });
  tb(s, "Target", { x: x + 0.2, y: 4.0, w: 1.85, h: 0.3, fontSize: 12, color: C.text2 });
  tb(s, target, { x: x + 0.2, y: 4.3, w: 1.85, h: 0.6, fontSize: 26, bold: true, color: C.accent2, fontFace: THEME.headFontFace });
  tb(s, d, { x: x + 0.2, y: 5.05, w: 1.85, h: 1.5, fontSize: 13, color: C.text2 });
});
s.addNotes("Measured monthly from the same queries as the frozen baseline. A change counts only when it holds for two periods. First review April 2027.");

// ---------- 12. Ask
pres.addSection({ title: "Decisions" });
s = pres.addSlide({ masterName: "CLOSE_DARK", sectionTitle: "Decisions" });
s.addText("What we need from management", { placeholder: "title" });
const asks = [
  ["Name a sponsor and an owner per critical flow", "No decision owner exists today"],
  ["Approve the gates for the Orchestration Core pilot", "Start with test health, PR rules, code owners"],
  ["Give access to Sonar, CI/CD and incident data", "Needed to measure detection and to track progress"],
  ["Require a migration rollout register", "No production rollout dates exist for 2026 migrations"],
];
asks.forEach(([t, d], i) => {
  const y = 1.6 + i * 1.15;
  numCircle(s, 0.6, y + 0.05, i + 1, C.accent3, 0.55);
  tb(s, t, { x: 1.4, y, w: 6.4, h: 0.45, fontSize: 18, bold: true, color: C.background1 });
  tb(s, d, { x: 1.4, y: y + 0.48, w: 6.4, h: 0.4, fontSize: 14, color: C.accent6 });
});
card(s, 8.4, 1.6, 4.3, 4.45, H.dk2, "timeline");
tb(s, "Timeline", { x: 8.7, y: 1.8, w: 3.7, h: 0.45, fontSize: 18, bold: true, color: C.background1 });
[["Now", "Pilot gates and measures start"], ["2027-Q1", "Re-test the AI effect (90-day window)"], ["2027-04", "Pilot review against the 5 targets"], ["Then", "Extend to Analytics and Data and WFM"]].forEach(([w, d], i) => {
  tb(s, w, { x: 8.7, y: 2.45 + i * 0.85, w: 1.2, h: 0.7, fontSize: 15, bold: true, color: C.accent3 });
  tb(s, d, { x: 9.95, y: 2.45 + i * 0.85, w: 2.55, h: 0.7, fontSize: 14, color: C.background1 });
});
s.addNotes("The four decisions unblock the pilot. Research outputs (specs, drafts, database) are ready; nothing has been changed in company systems.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
