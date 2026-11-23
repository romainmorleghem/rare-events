import { C, Plot, logPmf, logTail, logBellTail, rate, LN10, sci, rng, binomialSampler } from "../assets/plot.js";

const $ = id => document.getElementById(id);
const segValue = (seg, attr) => seg.querySelector("button.on").dataset[attr];
function wireSeg(seg, cb) {
  seg.querySelectorAll("button").forEach(b => b.onclick = () => {
    seg.querySelectorAll("button").forEach(x => x.classList.toggle("on", x === b)); cb();
  });
}

// ---------------------------------------------------------------- 1. three lenses
const nOf = v => Math.round(10 ** (1 + 2.5 * v / 100));          // slider 0..100 -> n = 10 .. ~3162
const lensPlot = new Plot($("lens"), { x: [0, 1], y: [0, 1] });
function drawLens() {
  const L = +segValue($("lens-seg"), "l"), n = nOf(+$("n").value), thr = +$("thr").value;
  $("n-o").textContent = n; $("thr-o").textContent = `${Math.round(thr * 100)}%`;
  const P = lensPlot, ks = [...Array(n + 1).keys()], lp = ks.map(k => logPmf(n, k));
  const r = Math.sqrt(n), sd = 0.5;
  let pts, bellPts = null, bowlPts = null;
  if (L === 1) {
    const ymax = Math.exp(Math.max(...lp)) * n * 1.1;
    P.x = [0, 1]; P.y = [0, ymax];
    pts = ks.flatMap((k, i) => [[(k - 0.5) / n, Math.exp(lp[i]) * n], [(k + 0.5) / n, Math.exp(lp[i]) * n]]);
  } else if (L === 2) {
    P.x = [-1.8, 1.8]; P.y = [0, 0.95];
    pts = ks.flatMap((k, i) => [[r * ((k - 0.5) / n - 0.5), Math.exp(lp[i]) * r], [r * ((k + 0.5) / n - 0.5), Math.exp(lp[i]) * r]]);
    bellPts = [...Array(301).keys()].map(i => { const z = -1.8 + 3.6 * i / 300; return [z, Math.exp(-z * z / (2 * sd * sd)) / (sd * Math.sqrt(2 * Math.PI))]; });
  } else {
    P.x = [0, 1]; P.y = [0, 0.75];
    pts = ks.map((k, i) => [k / n, -lp[i] / n]);
    bellPts = [...Array(201).keys()].map(i => { const x = i / 200; return [x, 2 * (x - 0.5) ** 2]; });
    bowlPts = [...Array(401).keys()].map(i => { const x = i / 400; return [x, rate(x)]; });
  }
  P.clear();
  P.axes({ xl: L === 2 ? "√n (proportion − ½)" : "proportion of heads", yl: L === 3 ? "−(1/n) ln P" : "how likely",
           yt: L === 3 ? 3 : 0 });
  if (L === 3) {
    if ($("bowl").checked) P.line(bowlPts, C.ldp, 4);
    P.line(pts, C.heads, 2);
    if ($("bell").checked) P.line(bellPts, C.clt, 2);
    P.vline(thr, C.truth, [4, 4]);
  } else {
    P.fill(pts, C.heads, 0.6);
    P.line(pts, C.heads, 1.2);
    if (bellPts && $("bell").checked) P.line(bellPts, C.clt, 2.5);
    if (L === 1) P.vline(thr, C.truth, [4, 4]);
  }
  // tail table
  const k = Math.ceil(thr * n - 1e-9), ex = logTail(n, k) / LN10, be = logBellTail(n, k) / LN10,
        ld = -n * rate(k / n) / LN10;
  const ratio = be - ex;
  $("tail").innerHTML = `<tr><th>P(at least ${k} heads out of ${n})</th><th>exact</th><th>bell curve</th><th>e<sup>−nI</sup></th><th>bell / exact</th></tr>
    <tr><td></td><td>${sci(ex)}</td><td style="color:var(--clt)">${sci(be)}</td><td style="color:var(--ldp)">${sci(ld)}</td>
    <td class="${Math.abs(ratio) > 1 ? "bad" : "ok"}">${ratio >= 0 ? "×" : "÷"} ${sci(Math.abs(ratio), 1).replace(/^1\.0 × /, "")}</td></tr>`;
}
wireSeg($("lens-seg"), drawLens);
["n", "thr", "bell", "bowl"].forEach(id => $(id).oninput = drawLens);
lensPlot.onresize = drawLens;
drawLens();

// ---------------------------------------------------------------- 2. rigged coin
const rigPlot = new Plot($("rig"), { x: [0, 1], y: [0, 1], aspect: 0.45 });
let last = null;
const keep = (n, k) => (last && last.n === n && last.k === k) ? last : (last = { n, k, fair: "", rig: "" });
function rigParams() {
  const n = +$("rn").value, k = Math.ceil(+$("rk").value * n - 1e-9), q = +$("rq").value;
  $("rn-o").textContent = n; $("rk-o").textContent = k; $("rq-o").textContent = q.toFixed(2);
  return { n, k, q };
}
function drawRig() {
  const { n, k, q } = rigParams(), P = rigPlot;
  P.x = [Math.max(0, Math.floor(0.3 * n)), n]; P.y = [0, 1];
  P.clear(); P.axes({ xl: "number of heads", yl: "", yt: 0 });
  const fair = [], rigd = [];
  for (let j = P.x[0]; j <= n; j++) { fair.push([j, Math.exp(logPmf(n, j, 0.5))]); rigd.push([j, Math.exp(logPmf(n, j, q))]); }
  const mx = Math.max(...fair.map(p => p[1]), ...rigd.map(p => p[1]));
  P.y = [0, mx * 1.15];
  P.fill(fair, C.heads, 0.55); P.line(fair, C.heads, 1.2);
  P.fill(rigd, C.rigged, 0.45); P.line(rigd, C.rigged, 1.2);
  P.vline(k, C.truth, [4, 4], `${k}`);
  const ex = logTail(n, k) / LN10;
  let html = `Exact $P(\\ge ${k})$ = <b>${sci(ex)}</b>.`;
  if (last && last.n === n && last.k === k) html += [last.fair, last.rig].filter(Boolean).map(h => `<br>${h}`).join("");
  $("rig-read").innerHTML = html.replace(/\$[^$]*\$/g, s => s.slice(1, -1).replace("\\ge", "≥"));
}
function runFair() {
  const { n, k } = rigParams(), rand = rng(7), S = binomialSampler(n, 0.5, rand);
  let hits = 0, best = 0; const M = 100000;
  for (let i = 0; i < M; i++) { const h = S(); if (h >= k) hits++; if (h > best) best = h; }
  keep(n, k).fair = (`Fair coin, ${M.toLocaleString("en")} experiments: <b>${hits}</b> hits (record ${best} heads)` +
    (hits ? `, estimate ${sci(Math.log10(hits / M))}.` : ". The event is invisible."));
  drawRig();
}
function runRig() {
  const { n, k, q } = rigParams(), rand = rng(11), S = binomialSampler(n, q, rand), M = 10000;
  const lh = Math.log(0.5 / q), lt = Math.log(0.5 / (1 - q)), lw = [];
  let hits = 0;
  for (let i = 0; i < M; i++) { const h = S(); if (h >= k) { hits++; lw.push(h * lh + (n - h) * lt); } }
  if (!hits) { keep(n, k).rig = `Rigged coin (q = ${q.toFixed(2)}): 0 hits. Rig harder!`; drawRig(); return; }
  const m = Math.max(...lw), w = lw.map(v => Math.exp(v - m));
  const s1 = w.reduce((a, b) => a + b, 0), s2 = w.reduce((a, b) => a + b * b, 0);
  const mean = s1 / M, varr = s2 / M - mean * mean, rel = Math.sqrt(Math.max(varr, 0) / M) / mean;
  const est = (Math.log(mean) + m) / LN10, ex = logTail(n, k) / LN10;
  keep(n, k).rig = (`Rigged coin (q = ${q.toFixed(2)}), ${M.toLocaleString("en")} experiments: ${hits} hits,
    weighted estimate <b style="color:var(--rigged)">${sci(est)}</b> ± ${(100 * rel).toFixed(0)}%
    (${Math.abs(est - ex) < 0.1 ? '<span class="ok">matches</span>' : '<span class="bad">off: try q closer to k/n</span>'}).`);
  drawRig();
}
["rn", "rk", "rq"].forEach(id => $(id).oninput = () => { last = null; drawRig(); });
$("run-fair").onclick = runFair; $("run-rig").onclick = runRig;
$("best-q").onclick = () => { $("rq").value = Math.min(0.99, +$("rk").value).toFixed(2); last = null; drawRig(); };
rigPlot.onresize = drawRig;
drawRig();

// ---------------------------------------------------------------- 3. conspiracy or culprit
const ccPlot = new Plot($("cc"), { x: [0, 100], y: [0, 12], aspect: 0.42 });
let sample = null, seed = 1;
function drawSample() {
  const kind = segValue($("kind-seg"), "k"), c = +$("c").value, a = +$("alpha").value, T = 100 * c;
  $("c-o").textContent = c.toFixed(1); $("alpha-o").textContent = a.toFixed(1);
  $("alpha").disabled = kind === "light";
  const rand = rng(seed++);
  let xs, tries = 0;
  if (kind === "light") {
    const e = Array.from({ length: 100 }, () => -Math.log(1 - rand())), s = e.reduce((p, v) => p + v, 0);
    xs = e.map(v => v * T / s);
  } else {
    const xm = (a - 1) / a;
    for (tries = 1; tries <= 3e6; tries++) {
      const b = Array.from({ length: 100 }, () => xm * Math.pow(1 - rand(), -1 / a));
      if (b.reduce((p, v) => p + v, 0) >= T) { xs = b; break; }
    }
  }
  sample = { kind, xs, tries, T };
  drawCC();
}
function drawCC() {
  const P = ccPlot; P.clear(); P.axes({ xl: "100 amounts", yl: "", xt: 0, yt: 3 });
  if (!sample || !sample.xs) { $("cc-read").textContent = "No sample found within the time budget: lower c or raise α."; return; }
  const xs = sample.xs, col = sample.kind === "light" ? C.tails : C.clt;
  P.bars(xs.map((_, i) => i + 0.5), xs.map(v => Math.min(v, 11.8)), 0.8, col);
  P.line([[0, 1], [100, 1]], C.fg, 1, 0.6, [3, 4]);
  const big = Math.max(...xs), i = xs.indexOf(big), sorted = [...xs].sort((p, q) => p - q);
  const med = sorted[49], c = P.ctx;
  if (big > 11.8) { c.fillStyle = C.clt; c.font = "13px system-ui, sans-serif"; c.textAlign = "left";
    c.fillText(`↑ ${big.toFixed(0)}`, P.px(i + 1.2), P.py(11.2)); }
  const tot = xs.reduce((p, v) => p + v, 0);
  $("cc-read").innerHTML = `Total ${tot.toFixed(0)}. Largest amount <b>${big.toFixed(1)}</b>
    (${(100 * big / tot).toFixed(0)}% of the total); median amount <b>${med.toFixed(2)}</b> (usual median:
    ${sample.kind === "light" ? "0.69" : (((+$("alpha").value - 1) / +$("alpha").value) * 2 ** (1 / +$("alpha").value)).toFixed(2)}).
    ${sample.kind === "heavy" ? ` Found after ${sample.tries.toLocaleString("en")} batches.` : ""}
    ${sample.kind === "light" ? "A conspiracy." : big / tot > 0.3 ? "A culprit." : ""}`;
}
wireSeg($("kind-seg"), drawSample);
["c", "alpha"].forEach(id => $(id).onchange = drawSample);
["c", "alpha"].forEach(id => $(id).oninput = () => { $("c-o").textContent = (+$("c").value).toFixed(1);
  $("alpha-o").textContent = (+$("alpha").value).toFixed(1); });
$("draw").onclick = drawSample;
ccPlot.onresize = drawCC;
drawSample();

// ---------------------------------------------------------------- 4. facts table
fetch("../data/ep1.json").then(r => r.json()).then(F => {
  const t = F.tails, rows = [
    ["P(≥ 600 heads of 1000)", sci(t["600"].exact), sci(t["600"].bell)],
    ["P(≥ 700 heads of 1000)", sci(t["700"].exact), sci(t["700"].bell)],
    ["P(≥ 900 heads of 1000)", sci(t["900"].exact), sci(t["900"].bell)],
  ];
  const imp = F.importance;
  $("facts").innerHTML = `<tr><th></th><th>exact</th><th>bell curve</th></tr>` +
    rows.map(r => `<tr><td style="text-align:left">${r[0]}</td><td>${r[1]}</td><td style="color:var(--clt)">${r[2]}</td></tr>`).join("") +
    `<tr><td style="text-align:left">1 000 000 fair experiments: record</td><td colspan="2">${F.naive.max_heads} heads, 0 hits at 700</td></tr>
     <tr><td style="text-align:left">10 000 rigged experiments (q = 0.7)</td><td colspan="2" style="color:var(--rigged)">${sci(imp["700"].estimate_log10)} ± ${(100 * imp["700"].rel_error).toFixed(0)}%</td></tr>
     <tr><td style="text-align:left">10 000 rigged experiments (q = 0.9)</td><td colspan="2" style="color:var(--rigged)">${sci(imp["900"].estimate_log10)} ± ${(100 * imp["900"].rel_error).toFixed(0)}%</td></tr>
     <tr><td style="text-align:left">Given 700 heads: longest streak (mean)</td><td colspan="2">${F.conspiracy.longest_run_mean.toFixed(1)} (fair coin: ${F.conspiracy.longest_run_fair_mean.toFixed(1)})</td></tr>
     <tr><td style="text-align:left">100 amounts, total ≥ 200: probability</td><td colspan="2">ordinary ${sci(F.tails_kind.light.prob_log10)}, wild ${sci(Math.log10(F.tails_kind.heavy.prob))}</td></tr>
     <tr><td style="text-align:left">… largest amount (typical)</td><td colspan="2">ordinary ${F.tails_kind.light.largest_mean.toFixed(1)}, wild ${F.tails_kind.heavy.largest_median.toFixed(0)}</td></tr>`;
});
