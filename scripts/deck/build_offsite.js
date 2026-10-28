const pptxgen = require("pptxgenjs");
const { applyTheme } = require("/Users/Guy.Guterman/.claude/skills/synced/ad2d1967-9b78-4a06-aa14-a45eb2824fc3_67ef7a44-32fc-4fe8-bd93-940173b50190/pptx/scripts/apply_theme.js");

const OUT = process.argv[2] || "/tmp/deck/offsite-deck.pptx";

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
pres.title = "Quality gates for pods and AI - Offsite kickoff";
pres.author = "QA Architecture";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const FOOT = "Quality gates for pods and AI  |  Evidence as of 2026-10-28";

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

const bullets = (arr) => arr.map((it, j) => ({ text: it, options: { bullet: true, breakLine: j < arr.length - 1 } }));
const content = (title, notes) => {
  const sl = pres.addSlide({ masterName: "CONTENT", sectionTitle: "Offsite" });
  sl.addText(title, { placeholder: "title" });
  if (notes) sl.addNotes(notes);
  return sl;
};

pres.addSection({ title: "Offsite" });

// 1 Title
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Offsite" });
s.addText("Quality gates for pods and AI: one contract, free means", { placeholder: "title" });
s.addText("What 2025-2026 taught us, and the gate model we propose  |  QA & RM  |  Offsite kickoff", { placeholder: "body" });
s.addNotes("Goal of this talk: agree on a gate model that works for hundreds of pods that each choose their own way of working. Evidence: 40 teams studied, Jan 2025 - Oct 2026.");

// 2 What happened
s = content("What happened in 2025-2026", "P1/P2 and all-bug counts: Jan-Sep 2026 vs 2025, MI investigation tickets removed. 96% = P1 incidents that entered through customer cases (intake channel is a proxy for first detection).");
[["+49%", "P1/P2 customer-found bugs", C.accent1], ["+13%", "all customer-found bugs", C.text1], ["96%", "of P1 incidents enter through customer cases", C.accent1], ["46%", "of valid bugs are business-correctness failures", C.text1]].forEach(([b, l, col], i) => {
  const x = 0.6 + i * 3.07;
  card(s, x, 1.55, 2.85, 2.5, C.background2, `stat-${i}`);
  tb(s, b, { x: x + 0.25, y: 1.75, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: col, fontFace: THEME.headFontFace });
  tb(s, l, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.1, fontSize: 15, color: C.text2 });
});
card(s, 0.6, 4.4, 12.1, 2.2, C.text1, "so-what");
tb(s, "So what", { x: 0.9, y: 4.6, w: 11.5, h: 0.45, fontSize: 18, bold: true, color: C.accent3 });
tb(s, [
  { text: "Quality fell in severity, not in volume.", options: { bold: true, breakLine: true } },
  { text: "Customers find our worst problems before we do." },
], { x: 0.9, y: 5.1, w: 11.5, h: 1.3, fontSize: 20, color: C.background1, paraSpaceAfter: 8 });

// 3 Risk is concentrated
s = content("Risk follows change size in hotspot code, not AI use", "Hotspot = top code directories by customer-bug-fix density. Follow-up fix = a later fix PR on the same files within 90 days. AI matched risk ratio 0.78-0.84, not significant. AI PRs in hotspots: 5% to 47%.");
s.addChart(pres.charts.BAR, [{ name: "Follow-up fix rate", labels: ["Small PR", "Large PR"], values: [21, 54] }], {
  x: 0.6, y: 1.5, w: 6.3, h: 5.1, barDir: "col", chartColors: [H.accent4, H.accent1], showTitle: true, title: "Follow-up fix within 90 days, hotspot code (%)",
  showValue: true, dataLabelPosition: "outEnd", showLegend: false, valAxisMaxVal: 70, valAxisHidden: true, barGapWidthPct: 60, ...chartText, ...chartFrame,
});
[["AI is not riskier per change", "Matched risk ratio 0.78-0.84 vs non-AI changes"],
 ["AI adds volume and size", "AI PRs in hotspot code: 5% to 47%"],
 ["Teams differ strongly", "Incidents per bug: 1.1 to 10.4 between teams"]].forEach(([t, d], i) => {
  const y = 1.55 + i * 1.7;
  card(s, 7.3, y, 5.4, 1.5, C.background2, `ins-${i}`);
  tb(s, t, { x: 7.55, y: y + 0.2, w: 4.9, h: 0.45, fontSize: 18, bold: true });
  tb(s, d, { x: 7.55, y: y + 0.75, w: 4.9, h: 0.6, fontSize: 14, color: C.text2 });
});

// 3b Outside research
s = content("Outside research 2024-2026 points the same way", "Trust: DORA = large survey (medium). METR = small RCT (high). Faros = vendor telemetry (low). Some numbers are from secondary write-ups; verify before quoting. Detail: docs/08-pod-quality/external-research-2024-2026.md");
s.addTable([
  [th("Finding"), th("Source"), th("So we")],
  ...[
    ["AI is an amplifier. Small batches and platform quality decide the payoff.", "DORA 2025", "Fix the contract; build a good paved road"],
    ["More AI adoption links to lower delivery stability.", "DORA 2024", "Gate on change size and risk, not author"],
    ["Experienced developers were 19% slower with AI, but felt faster.", "METR 2025", "Judge AI by outcomes, not opinion"],
    ["About 40-45% of AI code samples had security flaws.", "Pearce; Veracode", "Keep the security scan blocking"],
    ["Agent-made tests work when tools filter them first.", "Meta TestGen-LLM", "Agent output is untrusted until checked"],
    ["No study shows blocking gates beat advisory gates in autonomous teams.", "Gap", "Prove before we block"],
  ].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
], { x: 0.6, y: 1.5, w: 12.1, colW: [6.0, 2.2, 3.9], fontSize: 14, color: H.dk1, rowH: 0.72, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "outside-table" });

// 4 Why gates fail today
s = content("Why today's gates do not protect us", "Source: current-gates check 2026-10-25 (Confluence + GitHub, read-only). Nothing in the agent set blocks a change; agents run locally by choice.");
s.addTable([
  [th("What we see today"), th("Evidence")],
  ...[
    ["Almost no gate blocks a change", "Only Aikido and PR / Jira-ID checks block; Sonar required in 1 of 5 pilot repos"],
    ["Go/No-Go is a form, not data", "All 26.4 domain pages show TBD"],
    ["The E2E signal is not trusted", "Routing pipeline passed 1.2% of runs; failures ignored"],
    ["Quality fields are unused", "9 of ~15 Jira quality fields filled < 2%"],
    ["One gate set for every team", "Teams differ 10x in incidents per bug"],
  ].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
], { x: 0.6, y: 1.5, w: 12.1, colW: [4.6, 7.5], fontSize: 15, color: H.dk1, rowH: 0.78, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "today-table" });
tb(s, "Policy on paper does not change outcomes.", { x: 0.6, y: 6.4, w: 12.1, h: 0.5, fontSize: 18, bold: true, color: C.accent1 });

// 5 The model
s = content("The model: fixed outcomes, risk-based floor, free means", "Core idea: leadership fixes WHAT must be true and HOW it is measured. Pods choose HOW to get there. Gates check evidence, not tools.");
[["1", "Contract", "Same for every pod", "Intake rule, bug fields, 8 metrics, owner map", C.text1],
 ["2", "Risk floor", "Blocks only where data proves risk", "Hotspot PR rules, Sonar, toggles, escape-to-test, data-based Go/No-Go", C.accent1],
 ["3", "Free means", "Each pod chooses", "Structure, process, agents, test tools, RIA", C.accent2]].forEach(([n, t, sub, d, col], i) => {
  const y = 1.55 + i * 1.75;
  card(s, 0.6, y, 12.1, 1.55, C.background2, `layer-${i}`);
  numCircle(s, 0.9, y + 0.5, n, col, 0.55);
  tb(s, t, { x: 1.8, y: y + 0.2, w: 3.0, h: 0.5, fontSize: 24, bold: true, fontFace: THEME.headFontFace });
  tb(s, sub, { x: 1.8, y: y + 0.8, w: 3.2, h: 0.6, fontSize: 14, color: C.text2 });
  tb(s, d, { x: 5.2, y: y + 0.2, w: 7.2, h: 1.2, fontSize: 17, valign: "middle" });
});

// 6 Contract
s = content("Layer 1: the contract every pod keeps", "These are common because they make outcomes measurable and comparable, not because one way of working is better. RCA for P1/P2 is already 80-100% in every team.");
[["Intake rule", "Defect, MI investigation and expectation gap are separate types"],
 ["Bug fields", "Failure type, detected-by, causing change, affected customers"],
 ["RCA", "Every valid P1/P2 bug gets a root cause (already 80-100%)"],
 ["Owner map", "Pod -> service -> repo, with owners and backups"],
 ["Monthly view", "8 metrics per pod against its own baseline"],
 ["Same bar for all authors", "Human or AI: the same checks apply"]].forEach(([t, d], i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = 0.6 + col * 4.1, y = 1.6 + row * 2.6;
  card(s, x, y, 3.9, 2.3, C.background2, `ct-${i}`);
  tb(s, t, { x: x + 0.25, y: y + 0.25, w: 3.4, h: 0.5, fontSize: 20, bold: true, color: C.accent2 });
  tb(s, d, { x: x + 0.25, y: y + 0.9, w: 3.4, h: 1.2, fontSize: 15 });
});

// 6b What a pod must have
s = content("What every pod must have (roles, not job titles)", "One person can hold more than one role. Detail: pod quality playbook section 3.");
[["Quality owner", "Owns the contract, metric review, exception log"],
 ["Release owner", "Brings data to Go/No-Go"],
 ["Code owners", "Service map entry; 2+ owners per hotspot path"],
 ["Test strategy", "1 page: levels, tools, escaped bug to test"],
 ["AI agreement", "Which agents, who reviews, how AI use is labeled"],
 ["Production link", "Alerts reach the pod; detected-by recorded"],
 ["Test-signal care", "Each failing suite has an owner and a triage date"],
 ["Self-assessment", "25 questions each quarter, sent to QA&RM"]].forEach(([t, d], i) => {
  const col = i % 4, row = Math.floor(i / 4);
  const x = 0.6 + col * 3.07, y = 1.55 + row * 2.55;
  card(s, x, y, 2.85, 2.3, C.background2, `cap-${i}`);
  numCircle(s, x + 0.2, y + 0.2, i + 1, i < 7 ? C.accent2 : C.text2, 0.45);
  tb(s, t, { x: x + 0.8, y: y + 0.2, w: 1.95, h: 0.45, fontSize: 17, bold: true, valign: "middle" });
  tb(s, d, { x: x + 0.2, y: y + 0.9, w: 2.45, h: 1.2, fontSize: 14 });
});

// 6c QA&RM role
s = content("QA&RM role: enable, provide the road, govern", "Based on Team Topologies (enabling and platform teams) and DORA 2025 (platform quality decides AI payoff). The paved road is a product: if pods avoid it, QA&RM fixes it.");
[["Enabling", C.accent2, ["Coach test strategy, risk and hotspot work", "Short help, then step back"], "Not: own a pod's tests"],
 ["Paved road", C.accent3, ["Agents, pipeline templates, dashboards", "Gate checks ready to use"], "Not: force pods to use them"],
 ["Governance", C.accent1, ["Contract, gate catalog, metrics", "Experiments and Go/No-Go data"], "Not: approve every release by hand"]].forEach(([t, col, does, not], i) => {
  const x = 0.6 + i * 4.1;
  card(s, x, 1.55, 3.9, 0.8, col, `role-h-${i}`);
  tb(s, t, { x: x + 0.3, y: 1.55, w: 3.4, h: 0.8, fontSize: 22, bold: true, color: C.background1, valign: "middle" });
  card(s, x, 2.5, 3.9, 3.4, C.background2, `role-b-${i}`);
  tb(s, bullets(does), { x: x + 0.3, y: 2.7, w: 3.4, h: 2.2, fontSize: 16, paraSpaceAfter: 8 });
  tb(s, not, { x: x + 0.3, y: 5.0, w: 3.4, h: 0.7, fontSize: 14, bold: true, color: C.text2 });
});
tb(s, "A pod that leaves the paved road keeps the same gates and must still leave the evidence.", { x: 0.6, y: 6.2, w: 12.1, h: 0.5, fontSize: 16, bold: true, color: C.accent2 });

// 7 Gates along SDLC (S0-S8)
s = content("Layer 2: gates along the SDLC (target mode)", "Target mode shown. Most gates start Visible and block only after evidence. Full list with 29 gates, mode today and evidence: docs/08-pod-quality/gate-catalog.md.");
s.addTable([
  [th("Stage"), th("What must be true"), th("Blocks: all pods"), th("Blocks: T1 or hotspot")],
  ...[
    ["S0 Intake", "Report type; bug fields", "Report type", "-"],
    ["S1 Plan", "Spec link; state and toggle design", "-", "- (audit)"],
    ["S2 Build", "Tests with the change; AI use labeled", "-", "-"],
    ["S3 Review", "Jira key; hotspot size, owner, test", "Jira key", "Size, owner, test"],
    ["S4 CI", "Build, Sonar, security scan; healthy E2E", "Build, Sonar, scan, E2E when healthy", "-"],
    ["S5 Release", "Go/No-Go with data; toggle", "Go/No-Go with data; toggle", "Perf and chaos"],
    ["S6 Deploy", "Progressive rollout; sanity", "Post-deploy sanity", "Toggle-off verified"],
    ["S7 Operate", "Correctness monitors; SLOs", "-", "Monitors (after X2)"],
    ["S8 Learn", "RCA; escaped bug gets a test", "Test link or reason", "-"],
  ].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, color: (j > 1 && c !== "-" && !c.startsWith("-")) ? H.accent1 : H.dk1, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
], { x: 0.6, y: 1.45, w: 12.1, colW: [1.8, 4.3, 3.3, 2.7], fontSize: 14, color: H.dk1, rowH: 0.52, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "sdlc-table" });

// 7b Gate lifecycle
s = content("Every gate earns its place: prove before we block", "Proposed starting levels: 1 quarter Visible, false blocks under 5%, retire after 2 quarters with no value. Experiments and the Visible stage set final values.");
const life = [["Proposed", "Owner, metric, exception path defined", H.dk2], ["Visible", "Measured 1 quarter; does not stop work", H.dk1], ["Block per scope", "Beats control; false blocks < 5%", H.accent1], ["Review", "Each quarter: value, false blocks, exceptions", H.dk1], ["Retire", "No catch or no outcome change for 2 quarters", H.accent4]];
const lw = 2.3, lg = 0.15;
life.forEach(([n, d, col], i) => {
  const x = 0.6 + i * (lw + lg);
  s.addShape(pres.shapes.CHEVRON, { x, y: 1.7, w: lw, h: 0.9, fill: { color: col }, line: { color: col }, objectName: `life-${i}` });
  tb(s, n, { x: x + 0.35, y: 1.7, w: lw - 0.6, h: 0.9, align: "center", valign: "middle", fontSize: 15, bold: true, color: C.background1 });
  card(s, x, 2.85, lw, 1.9, C.background2, `lifec-${i}`);
  tb(s, d, { x: x + 0.15, y: 3.0, w: lw - 0.3, h: 1.6, fontSize: 15 });
});
card(s, 0.6, 5.1, 12.1, 1.5, C.text1, "modes");
tb(s, [
  { text: "Modes:  ", options: { bold: true, color: C.accent3 } },
  { text: "Advice (a means, not checked)  |  Visible (on the dashboard)  |  Audit (sample check)  |  Block (required check, exceptions logged)", options: { color: C.background1 } },
], { x: 0.9, y: 5.25, w: 11.5, h: 1.2, fontSize: 16, valign: "middle" });

// 8 AI
s = content("AI and pods: one rule set for every author", "Agents we provide (test cases, automation, RIA, mutation) are suggested means. A pod that proves the same outcome another way passes the same gate.");
card(s, 0.6, 1.55, 5.9, 5.05, C.text1, "ai-left");
tb(s, "We do", { x: 0.9, y: 1.75, w: 5.3, h: 0.5, fontSize: 20, bold: true, color: C.accent3 });
tb(s, bullets(["Keep AI-assisted development", "Apply the same gates to every author", "Scale review by change size and code area", "Offer agents as a paved road, not a duty"]), { x: 0.9, y: 2.35, w: 5.3, h: 4.0, fontSize: 18, color: C.background1, paraSpaceAfter: 10 });
card(s, 6.8, 1.55, 5.9, 5.05, C.background2, "ai-right");
tb(s, "We do not", { x: 7.1, y: 1.75, w: 5.3, h: 0.5, fontSize: 20, bold: true, color: C.accent1 });
tb(s, bullets(["Add an AI-only gate", "Require a specific tool or agent", "Block on a score before we prove it works", "Use raw bug counts as the quality number"]), { x: 7.1, y: 2.35, w: 5.3, h: 4.0, fontSize: 18, paraSpaceAfter: 10 });

// 9 Pods
s = content("Pods differ: the floor is common, the depth follows risk", "40 teams studied, 4 archetypes, re-assessed quarterly. Teams choose how to meet a requirement; the model fixes what must be true.");
s.addTable([
  [th("Pod type"), th("Pods"), th("What changes"), th("Why")],
  ...[
    ["A. High impact", "9", "More depth on detection and recovery", "Incidents per bug and P1/P2 share above median"],
    ["B. Fast growing", "8", "Check re-homing first, then triage and capacity", "Part of growth is renames and splits"],
    ["C. High noise", "5", "Intake and expectation gaps before defects", "50%+ of reports invalid"],
    ["D. Stable", "18", "Contract and common floor only", "No signal that more control helps"],
  ].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j < 2, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
], { x: 0.6, y: 1.5, w: 12.1, colW: [2.6, 1.0, 4.6, 3.9], fontSize: 15, color: H.dk1, rowH: 0.85, border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "pods-table" });
tb(s, "Each pod is compared with its own 2025 baseline and with similar pods, never with one shared target.", { x: 0.6, y: 5.95, w: 12.1, h: 0.6, fontSize: 17, bold: true, color: C.accent2 });

// 10 Metrics (2 slides, table form)
const metricRows = [
  ["D1 Business correctness", "Valid bugs where the product does the wrong thing. Data, routing, contact lifecycle. Weighted by severity.", "Bugs: 295 to 325 (+10%). P1/P2 share: 52% to 70%.", "Customer reports only. Billing is rarely reported.", "Where to invest first"],
  ["D2 Availability", "P1 incidents per quarter. Customers affected.", "P1 by customer channel: about 150 to 76 per quarter.", "ServiceNow access pending. Reason for the fall is unknown.", "Reliability work and release risk"],
  ["D3 Performance", "Slow-system bugs. SLO breaches.", "50 performance bugs in total.", "No SLO data yet.", "Capacity work"],
  ["D4 Detection", "Share of impact that we find before customers.", "96% of P1 incidents come through customer cases.", "Intake channel is only a proxy for first detection.", "Monitoring investment and Go/No-Go"],
  ["D5 Recovery", "Time to restore service. Time to fix a bug.", "71% of P1 under 4 hours. Bug fix median 10 days, both years.", "Resolve time is not restore time.", "Response capacity"],
  ["D6 Change safety", "Bugs caused by fixes. Emergency changes. Recent changes.", "Fix-caused: 23.5% to 27.1%. Emergency changes x2.9 since June 2026.", "Cause is known for 25% of bugs only.", "Review depth for fixes"],
  ["D7 Non-recurrence", "Do fixes hold? Repeat bugs and reopens.", "Repeat: 3.9% to 1.2-1.6%. Reopen: 5.2% to 5.6%.", "Similarity model. One rater.", "Whether fixes work"],
  ["D8 Expectation fit", "Reports closed as works as designed that are real gaps.", "25% of reports closed this way. 42.5% of those are real gaps.", "Sample of 40 only.", "Requirement and documentation work"],
];
[[0, "Eight metrics every pod sees (1 of 2)"], [4, "Eight metrics every pod sees (2 of 2)"]].forEach(([from, title]) => {
  s = content(title, "Baseline: 2025 vs 2026, MI investigation tickets removed. Each pod compares with its own baseline. D2, D4, D5 per pod need ServiceNow read access (request REQ0120210 pending).");
  s.addTable([
    [th("Metric"), th("What it measures"), th("Today (2025 to 2026)"), th("Data limit"), th("Decision it supports")],
    ...metricRows.slice(from, from + 4).map((r, i) => r.map((c, j) => ({ text: c, options: { bold: j === 0, fill: { color: i % 2 ? H.lt1 : H.lt2 } } }))),
  ], { x: 0.6, y: 1.5, w: 12.1, colW: [1.9, 3.1, 2.7, 2.3, 2.1], fontSize: 14, color: H.dk1, rowH: [0.5, 1.05, 1.05, 1.05, 1.05], border: { type: "solid", pt: 0.5, color: "DDE3EA" }, fontFace: THEME.bodyFontFace, valign: "middle", objectName: "metrics-table" });
  if (from === 4) tb(s, "Rule: a pod outside its own range for 2 months gets an investigation, not a punishment.", { x: 0.6, y: 6.5, w: 12.1, h: 0.4, fontSize: 14, color: C.text2 });
});

// 11 Prove before block
s = pres.addSlide({ masterName: "CLOSE_DARK", sectionTitle: "Offsite" });
s.addText("Prove before we block: timeline", { placeholder: "title" });
s.addNotes("Limits: team-to-service map missing (U-26/U-27 open), no SME validation yet, ServiceNow P1 fall unexplained (C-08). Blocking gates are tested in X3/X4 before rollout.");
[["Now (Nov 2026)", ["Intake rule and bug fields (X1)", "Sonar required everywhere", "Mutation score visible, not blocking", "Go/No-Go with data", "Correctness monitor in shadow (X2)"]],
 ["Q1 2027", ["Hotspot PR rules (X3)", "Bug-fix review (X4)", "Expectation-gap triage (X5)", "Monthly pod review"]],
 ["April 2027 and after", ["Results vs control pods", "Decide what blocks, per tier", "Spread proven practices to all pods", "Decide on RIA, mutation, harness"]]].forEach(([t, items], i) => {
  const x = 0.6 + i * 4.1;
  tb(s, t, { x, y: 1.6, w: 3.8, h: 0.55, fontSize: 22, bold: true, color: C.accent3 });
  tb(s, bullets(items), { x, y: 2.3, w: 3.8, h: 3.6, fontSize: 16, color: C.background1, paraSpaceAfter: 8 });
});
tb(s, "Open limits: owner map missing, no SME validation yet, ServiceNow data pending.", { x: 0.6, y: 6.3, w: 12.1, h: 0.5, fontSize: 14, color: C.accent6 });

// 12 Asks
s = pres.addSlide({ masterName: "CLOSE_DARK", sectionTitle: "Offsite" });
s.addText("What we ask from you today", { placeholder: "title" });
[["Agree the model", "One contract, a small blocking floor, free means"],
 ["Name a quality owner per pod", "Owner map, bug fields, quarterly self-assessment"],
 ["Volunteer pods", "For the experiments X1-X5, with control pods"],
 ["Decide the Dec 15 mutation gate", "Visible in Sonar first; block per scope after evidence"]].forEach(([t, d], i) => {
  const y = 1.6 + i * 1.3;
  numCircle(s, 0.6, y + 0.1, i + 1, C.accent3, 0.6);
  tb(s, t, { x: 1.5, y, w: 5.2, h: 0.9, fontSize: 22, bold: true, color: C.background1, valign: "middle" });
  tb(s, d, { x: 6.9, y, w: 5.8, h: 0.9, fontSize: 17, color: C.accent6, valign: "middle" });
});
s.addNotes("Ask for explicit yes/no on each of the four. Discussion prompt: what is the one gate your pod would never accept, and why?");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
