/* Let's Practice: solve a worksheet on the site, one task at a time (besides printing it).
   The worksheet HTML marks its answers with data attributes (scripts/generate.py ans_attr, ARCHITECTURE.md):
     data-a="7" (+ data-k="sign" | "word" | "bank" | "shape")  a box to fill; data-a="*" any answer; data-a="?" see data-sum
     data-p="1" | "0" (+ data-look="tick" | "fill")              something to pick: right / wrong
     data-n="4" with data-cell inside                            tap this many cells (draw dots, cross out)
     data-ml / data-mr with the same key                         join with a line
     data-sum="10" on a row of two boxes                          a number bond: the two make 10, every pair once
     data-self                                                    the child checks it (tracing, shading)
   Results go to the child's progress (practice.js). Nothing is sent anywhere. */
"use strict";

const OT = {
  en: { tab: "Solve on screen", task: "Task {n} of {all}", check: "Check", next: "Next task", prev: "Back", listen: "Listen",
    right: "Well done!", almost: "Almost! Look at the boxes with a dot and try again.", shown: "The right answers are shown in grey. Look and go on.",
    selfQ: "Do it on paper or with your finger. Did it work?", yes: "Yes, I did it", notYet: "Not yet", done: "I can do it!", finish: "All tasks done!",
    summary: "First try: {n} of {all}", again: "Solve again", pick: "Tap to choose", word: "Type the word", ok: "OK", help: "Help card",
    keypadNext: "Next box" },
  uk: { tab: "Розв’язати на екрані", task: "Завдання {n} з {all}", check: "Перевірити", next: "Далі", prev: "Назад", listen: "Послухати",
    right: "Молодець!", almost: "Майже! Подивись на клітинки з крапкою і спробуй ще.", shown: "Правильні відповіді показано сірим. Подивись і йди далі.",
    selfQ: "Зроби на папері або пальцем. Вийшло?", yes: "Так, вийшло", notYet: "Ще ні", done: "Я це вмію!", finish: "Усі завдання виконано!",
    summary: "З першого разу: {n} з {all}", again: "Розв’язати ще раз", pick: "Натисни, щоб вибрати", word: "Напиши слово", ok: "OK", help: "Картка-підказка",
    keypadNext: "Наступна клітинка" },
  ru: { tab: "Решать на экране", task: "Задание {n} из {all}", check: "Проверить", next: "Дальше", prev: "Назад", listen: "Послушать",
    right: "Молодец!", almost: "Почти! Посмотри на клетки с точкой и попробуй ещё.", shown: "Правильные ответы показаны серым. Посмотри и иди дальше.",
    selfQ: "Сделай на бумаге или пальцем. Получилось?", yes: "Да, получилось", notYet: "Ещё нет", done: "Я могу!", finish: "Все задания сделаны!",
    summary: "С первого раза: {n} из {all}", again: "Решить ещё раз", pick: "Нажми, чтобы выбрать", word: "Напиши слово", ok: "OK", help: "Карточка-подсказка",
    keypadNext: "Следующая клетка" },
  el: { tab: "Λύσε στην οθόνη", task: "Άσκηση {n} από {all}", check: "Έλεγχος", next: "Επόμενη", prev: "Πίσω", listen: "Άκου",
    right: "Μπράβο!", almost: "Σχεδόν! Δες τα κουτιά με την τελεία και ξαναδοκίμασε.", shown: "Οι σωστές απαντήσεις φαίνονται με γκρι. Δες τες και συνέχισε.",
    selfQ: "Κάν’ το στο χαρτί ή με το δάχτυλο. Τα κατάφερες;", yes: "Ναι, τα κατάφερα", notYet: "Όχι ακόμα", done: "Τα καταφέρνω!", finish: "Όλες οι ασκήσεις έγιναν!",
    summary: "Με την πρώτη: {n} από {all}", again: "Λύσε ξανά", pick: "Πάτησε για να διαλέξεις", word: "Γράψε τη λέξη", ok: "OK", help: "Κάρτα βοήθειας",
    keypadNext: "Επόμενο κουτί" },
  de: { tab: "Am Bildschirm lösen", task: "Aufgabe {n} von {all}", check: "Prüfen", next: "Weiter", prev: "Zurück", listen: "Anhören",
    right: "Super!", almost: "Fast! Schau auf die Kästchen mit Punkt und versuch es noch mal.", shown: "Die richtigen Antworten stehen grau da. Schau sie an und mach weiter.",
    selfQ: "Mach es auf Papier oder mit dem Finger. Hat es geklappt?", yes: "Ja, geschafft", notYet: "Noch nicht", done: "Ich kann das!", finish: "Alle Aufgaben fertig!",
    summary: "Beim ersten Mal: {n} von {all}", again: "Noch einmal lösen", pick: "Tippe zum Auswählen", word: "Schreib das Wort", ok: "OK", help: "Hilfekarte",
    keypadNext: "Nächstes Kästchen" },
  fr: { tab: "Résoudre à l’écran", task: "Exercice {n} sur {all}", check: "Vérifier", next: "Suivant", prev: "Retour", listen: "Écouter",
    right: "Bravo !", almost: "Presque ! Regarde les cases avec un point et réessaie.", shown: "Les bonnes réponses sont en gris. Regarde-les et continue.",
    selfQ: "Fais-le sur papier ou avec le doigt. Ça a marché ?", yes: "Oui, j’ai réussi", notYet: "Pas encore", done: "Je sais le faire !", finish: "Tous les exercices sont faits !",
    summary: "Du premier coup : {n} sur {all}", again: "Recommencer", pick: "Touche pour choisir", word: "Écris le mot", ok: "OK", help: "Carte d’aide",
    keypadNext: "Case suivante" },
  es: { tab: "Resolver en pantalla", task: "Ejercicio {n} de {all}", check: "Comprobar", next: "Siguiente", prev: "Atrás", listen: "Escuchar",
    right: "¡Muy bien!", almost: "¡Casi! Mira las casillas con un punto y prueba otra vez.", shown: "Las respuestas correctas están en gris. Míralas y sigue.",
    selfQ: "Hazlo en papel o con el dedo. ¿Te salió?", yes: "Sí, me salió", notYet: "Todavía no", done: "¡Yo puedo!", finish: "¡Todos los ejercicios hechos!",
    summary: "A la primera: {n} de {all}", again: "Resolver otra vez", pick: "Toca para elegir", word: "Escribe la palabra", ok: "OK", help: "Tarjeta de ayuda",
    keypadNext: "Siguiente casilla" },
};
const ot = (k, o) => fmt(OT[state.ui][k], o || {});
const GREY = "#e9e9e9";
const OLW = 724;  // a task is 714 px wide on the A4 page; on screen it is scaled to the width

/* ---------------------------------------------------------------- the online state of a sheet */
let ol = null;  // {key, secs:[{html, tid, n, st}], i}
function sheetKey() { return `${state.level}|${state.seed}|${state.lang}`; }
function loadSheet() {
  if (ol && ol.key === sheetKey()) return ol;
  const map = (catalog() && catalog().stage_ids) || {}, secs = [];
  for (const body of state.sheet.pages) {
    const d = new DOMParser().parseFromString(body, "text/html");
    d.querySelectorAll("section[data-task]").forEach((s) => {
      s.classList.remove("stretch"); s.removeAttribute("style");
      secs.push({ html: s.outerHTML, tid: map[s.dataset.task] || s.dataset.task, n: s.querySelector(".n")?.textContent.trim() || "",
        title: s.querySelector(".qt, .it")?.textContent.trim() || "", st: newState() });
    });
  }
  ol = { key: sheetKey(), secs, i: 0 };
  return ol;
}
function newState() { return { vals: {}, sel: new Set(), cells: {}, pairs: {}, cur: 0, tries: 0, done: false, first: null, result: null, self: null, wrong: new Set() }; }

/* ---------------------------------------------------------------- markup of the online tab */
function ensureTab() {
  if ($("tab-online")) { $("tab-online").textContent = ot("tab"); return; }
  const b = Object.assign(document.createElement("button"), { className: "chip", id: "tab-online", type: "button", textContent: ot("tab") });
  b.dataset.tab = "online"; b.setAttribute("aria-pressed", "false");
  $("tabs").appendChild(b);
}
const olStyle = document.createElement("style");
olStyle.textContent = `
  .ol { display:flex; flex-direction:column; gap:12px; max-width:860px; }
  .ol-top { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
  .ol-top b { font-size:20px; font-weight:900; margin-right:auto; }
  .ol-dots { display:flex; gap:4px; flex-wrap:wrap; }
  .ol-dots button { width:30px; height:30px; border-radius:50%; border:2px solid var(--ink); background:#fff; font-weight:900; font-size:13px; padding:0; }
  .ol-dots button.on { outline:3px solid var(--ink); outline-offset:2px; }
  .ol-dots button.ok { background:var(--ink); color:#fff; }
  .ol-frame { position:relative; background:#fff; border:var(--b); border-radius:var(--r); overflow:hidden; }
  .ol-frame iframe { position:absolute; left:0; top:0; width:${OLW}px; border:0; transform-origin:0 0; }
  .ol-pad { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; }
  .ol-pad button { min-width:58px; min-height:58px; font-size:26px; font-weight:900; border:var(--b); border-radius:14px; background:#fff; padding:0 12px; }
  .ol-pad button:active { background:var(--soft); }
  .ol-pad .wide2 { font-size:17px; }
  .ol-pad input { height:58px; font-size:22px; font-weight:800; border:var(--b); border-radius:14px; padding:0 12px; min-width:0; flex:1; max-width:340px; }
  .ol-act { display:flex; gap:8px; flex-wrap:wrap; justify-content:center; }
  .ol-act .btn { min-height:54px; font-size:18px; font-weight:900; border-radius:14px; padding:0 22px; }
  .ol-msg { min-height:0; text-align:center; font-size:20px; font-weight:900; }
  .ol-end { text-align:center; display:flex; flex-direction:column; gap:12px; align-items:center; border:var(--b); border-radius:var(--r); background:#fff; padding:26px; }
  .ol-end .stars { font-size:44px; letter-spacing:6px; }
  .ol-end .big { display:inline-block; background:var(--ink); color:#fff; border-radius:40px; padding:8px 26px; font-size:28px; font-weight:900; }
`;
document.head.appendChild(olStyle);

// inside the task frame: how picked, filled, wrong and current things look
const FRAME_CSS = `
  body{margin:0;background:#fff} .olwrap{width:${OLW}px;box-sizing:border-box;padding:10px 5px}
  [data-a],[data-p],[data-cell],[data-ml],[data-mr]{cursor:pointer}
  .ol-cur{outline:4px solid #111 !important;outline-offset:3px;border-radius:10px}
  .ol-sel{outline:3.5px solid #111;outline-offset:5px;border-radius:999px}
  .ol-fill{display:inline-flex !important;align-items:center;justify-content:center;font-size:24px;font-weight:800;font-family:inherit}
  .ol-wrong{background:#fff !important;outline:3px dashed #111 !important;outline-offset:3px}
  .ol-shown{background:${GREY} !important}
`;

/* ---------------------------------------------------------------- render the tab */
const olScaler = new ResizeObserver(() => fitFrame());
function render() {
  ensureTab();
  const s = loadSheet();
  if (!s.secs.length) { $("view").innerHTML = ""; return; }
  if (s.i >= s.secs.length) return renderEnd();
  const sec = s.secs[s.i];
  $("view").innerHTML = `<div class="ol">
      <div class="ol-top"><b>${ot("task", { n: s.i + 1, all: s.secs.length })}</b><div class="ol-dots" id="ol-dots"></div></div>
      <div class="ol-frame" id="ol-frame"><iframe id="ol-if" title="${esc(sec.title)}"></iframe></div>
      <div class="ol-msg" id="ol-msg" role="status"></div>
      <div class="ol-pad" id="ol-pad"></div>
      <div class="ol-act" id="ol-act"></div></div>`;
  $("ol-dots").innerHTML = s.secs.map((x, i) =>
    `<button type="button" data-ol-go="${i}" class="${i === s.i ? "on" : ""} ${x.st.done ? "ok" : ""}" aria-label="${ot("task", { n: i + 1, all: s.secs.length })}">${x.st.done ? "★" : i + 1}</button>`).join("");
  const fr = $("ol-if");
  fr.addEventListener("load", () => { setupFrame(fr, sec); fitFrame(); });
  fr.srcdoc = doc([`<div class="olwrap">${sec.html}</div>`], state.sheet.css + FRAME_CSS, sec.title, state.lang);
  olScaler.disconnect(); olScaler.observe($("ol-frame"));
}
function fitFrame() {
  const fr = $("ol-if"), box = $("ol-frame"); if (!fr || !box) return;
  let h = 300;
  try { h = fr.contentDocument.querySelector(".olwrap").scrollHeight; } catch { /* loading */ }
  const k = box.clientWidth / OLW;
  fr.style.height = h + "px"; fr.style.transform = `scale(${k})`;
  box.style.height = Math.ceil(h * k) + "px";
}
function renderEnd() {
  const s = ol, first = s.secs.filter((x) => x.st.first === 1).length;
  const stars = "★".repeat(Math.max(1, Math.round(3 * first / s.secs.length)));
  $("view").innerHTML = `<div class="ol-end"><div class="stars">${stars}</div><span class="big">${ot("done")}</span>
    <b style="font-size:20px">${ot("finish")}</b><span>${ot("summary", { n: first, all: s.secs.length })}</span>
    <div class="ol-act"><button class="btn" type="button" data-ol-again>${ot("again")}</button>
    <button class="btn dark" type="button" data-ol-today>${PT[state.ui].today}</button></div></div>`;
}

/* ---------------------------------------------------------------- inside the frame */
const EL = {};  // the current task's elements: slots, picks, groups, left/right ends, sums, self
function setupFrame(fr, sec) {
  const d = fr.contentDocument, root = d.querySelector(".olwrap");
  EL.d = d; EL.sec = sec;
  EL.slots = [...root.querySelectorAll("[data-a]")];
  EL.picks = [...root.querySelectorAll("[data-p]")];
  EL.groups = [...root.querySelectorAll("[data-n]")].map((g) => ({ g, cells: [...g.querySelectorAll("[data-cell]")] }));
  EL.left = [...root.querySelectorAll("[data-ml]")]; EL.right = [...root.querySelectorAll("[data-mr]")];
  EL.self = !!root.querySelector("[data-self]") && !EL.slots.length && !EL.picks.length;
  EL.bank = [...root.querySelectorAll(".pill")].map((p) => p.textContent.replace(/­/g, "").trim());
  EL.shapes = {};
  root.querySelectorAll("[data-shape]").forEach((s) => { EL.shapes[s.dataset.shape] = s.outerHTML.replace(/data-shape="[^"]*"/, ""); });
  EL.orig = EL.slots.map((s) => s.innerHTML);
  root.addEventListener("click", onFrameClick);
  paint();
  renderPad();
  renderActions(sec);
}
const isSvg = (el) => el instanceof EL.d.defaultView.SVGElement && el.tagName.toLowerCase() !== "svg";
function overlay(el, make) {  // draw something on top of an SVG element, in its own SVG
  const svg = el.ownerSVGElement, b = el.getBBox(), m = el.getCTM && el.getCTM(), sm = svg.getCTM && svg.getCTM();
  let x = b.x, y = b.y, w = b.width, h = b.height;
  if (m && sm) {  // element coordinates -> svg user coordinates (elements may be translated or scaled)
    const p = svg.createSVGPoint(), inv = sm.inverse();
    const pts = [[b.x, b.y], [b.x + b.width, b.y + b.height]].map(([px, py]) => { p.x = px; p.y = py; return p.matrixTransform(m).matrixTransform(inv); });
    x = Math.min(pts[0].x, pts[1].x); y = Math.min(pts[0].y, pts[1].y); w = Math.abs(pts[1].x - pts[0].x); h = Math.abs(pts[1].y - pts[0].y);
  }
  const g = EL.d.createElementNS("http://www.w3.org/2000/svg", "g");
  g.setAttribute("class", "ol-x"); g.setAttribute("pointer-events", "none");
  g.innerHTML = make(x, y, w, h);
  svg.appendChild(g);
}
const center = (el) => { const r = el.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; };

function paint() {
  const st = EL.sec.st, d = EL.d;
  d.querySelectorAll(".ol-x").forEach((x) => x.remove());
  d.querySelectorAll(".ol-cur,.ol-sel,.ol-wrong,.ol-shown").forEach((x) => x.classList.remove("ol-cur", "ol-sel", "ol-wrong", "ol-shown"));
  // boxes
  EL.slots.forEach((s, i) => {
    const v = st.vals[i] ?? "", shown = st.done && st.shown && st.shown[i] !== undefined;
    const text = shown ? st.shown[i] : v, k = s.dataset.k;
    if (isSvg(s)) {
      if (text !== "") overlay(s, (x, y, w, h) => `<text x="${x + w / 2}" y="${y + h / 2 + 9}" text-anchor="middle" font-size="26" font-weight="800" fill="#111">${esc(text)}</text>`);
      if (i === st.cur && !st.done) overlay(s, (x, y, w, h) => `<rect x="${x - 4}" y="${y - 4}" width="${w + 8}" height="${h + 8}" rx="10" fill="none" stroke="#111" stroke-width="4"/>`);
      if (st.wrong.has(i)) overlay(s, (x, y, w, h) => `<circle cx="${x + w - 4}" cy="${y + 4}" r="6" fill="#111"/>`);
      if (shown) s.setAttribute("fill", GREY);
    } else {
      s.innerHTML = k === "shape" && text ? (EL.shapes[text] || text) : (text === "" ? EL.orig[i] : esc(k === "sign" ? text : text));
      s.classList.toggle("ol-fill", text !== "" && k !== "word" && k !== "bank");
      if (text !== "" && (k === "word" || k === "bank")) { s.style.fontSize = "22px"; s.style.fontWeight = "800"; s.style.textAlign = "center"; }
      if (i === st.cur && !st.done) s.classList.add("ol-cur");
      if (st.wrong.has(i)) s.classList.add("ol-wrong");
      if (shown) s.classList.add("ol-shown");
    }
  });
  // picks
  EL.picks.forEach((p, i) => {
    const on = st.done && st.shown ? p.dataset.p === "1" : st.sel.has(i), look = p.dataset.look;
    if (!on) return;
    if (look === "tick") {
      if (p.tagName.toLowerCase() === "svg") overlayRoot(p, `<path d="M9 22 L17 30 L33 11" fill="none" stroke="#111" stroke-width="4" stroke-linecap="round"/>`);
      else { p.textContent = "✓"; p.classList.add("ol-fill"); }
    } else if (look === "fill") {
      p.setAttribute("fill", "#bdbdbd");  // the shape group itself gets coloured
    } else if (isSvg(p)) overlay(p, (x, y, w, h) => `<ellipse cx="${x + w / 2}" cy="${y + h / 2}" rx="${w / 2 + 10}" ry="${h / 2 + 10}" fill="none" stroke="#111" stroke-width="3.5"/>`);
    else p.classList.add("ol-sel");
  });
  EL.picks.forEach((p, i) => {  // un-picked: back to how it was
    const on = st.done && st.shown ? p.dataset.p === "1" : st.sel.has(i);
    if (on) return;
    if (p.dataset.look === "tick" && p.tagName.toLowerCase() !== "svg") { p.textContent = ""; p.classList.remove("ol-fill"); }
    if (p.dataset.look === "fill") p.setAttribute("fill", "#fff");
    if (p.dataset.look === "tick" && p.tagName.toLowerCase() === "svg") p.querySelectorAll(".ol-x").forEach((x) => x.remove());
  });
  // cells: dots in a ten frame, crosses on objects
  EL.groups.forEach(({ cells }, gi) => {
    const on = st.cells[gi] || new Set();
    cells.forEach((c, ci) => {
      if (!on.has(ci)) return;
      if (c.tagName.toLowerCase() === "rect") overlay(c, (x, y, w, h) => `<circle cx="${x + w / 2}" cy="${y + h / 2}" r="${w * 0.32}" fill="#111"/>`);
      else overlay(c, (x, y, w, h) => `<path d="M${x} ${y} L${x + w} ${y + h} M${x + w} ${y} L${x} ${y + h}" stroke="#111" stroke-width="3.5" fill="none"/>`);
    });
  });
  // lines between matched ends
  Object.entries(st.pairs).forEach(([li, ri]) => joinLine(EL.left[+li], EL.right[+ri]));
  if (st.pick !== undefined && EL.left[st.pick]) overlay(EL.left[st.pick], (x, y, w, h) => `<rect x="${x - 4}" y="${y - 4}" width="${w + 8}" height="${h + 8}" rx="10" fill="none" stroke="#111" stroke-width="3" stroke-dasharray="6 5"/>`);
  if (st.done && st.shown) EL.left.forEach((l) => { const r = EL.right.find((x) => x.dataset.mr === l.dataset.ml); if (r && !Object.entries(st.pairs).some(([li, ri]) => EL.left[+li] === l && EL.right[+ri] === r)) joinLine(l, r, true); });
  fitFrame();
}
function overlayRoot(svg, inner) {
  const g = EL.d.createElementNS("http://www.w3.org/2000/svg", "g");
  g.setAttribute("class", "ol-x"); g.innerHTML = inner; svg.appendChild(g);
}
function joinLine(l, r, grey) {  // from the dot on the right of the left end to the dot on the left of the right end
  const svg = l.ownerSVGElement, inv = svg.getScreenCTM().inverse(), p = svg.createSVGPoint();
  const at = (el, side) => { const b = el.getBoundingClientRect(); p.x = side ? b.right : b.left; p.y = b.top + b.height / 2; return p.matrixTransform(inv); };
  const dotL = l.querySelector("circle[r='5']"), dotR = r.querySelector("circle[r='5']");
  const a = dotL ? at(dotL, 1) : at(l, 1), b = dotR ? at(dotR, 0) : at(r, 0);
  const g = EL.d.createElementNS("http://www.w3.org/2000/svg", "g");
  g.setAttribute("class", "ol-x"); g.setAttribute("pointer-events", "none");
  const mx = (a.x + b.x) / 2;
  g.innerHTML = `<path d="M${a.x} ${a.y} C${mx} ${a.y} ${mx} ${b.y} ${b.x} ${b.y}" fill="none" stroke="${grey ? "#9a9a9a" : "#111"}" stroke-width="3" stroke-linecap="round"/>`;
  svg.appendChild(g);
}

function onFrameClick(e) {
  const st = EL.sec.st; if (st.done) return;
  const t = e.target;
  const slot = t.closest("[data-a]"), pick = t.closest("[data-p]"), cell = t.closest("[data-cell]"), l = t.closest("[data-ml]"), r = t.closest("[data-mr]");
  if (slot) { st.cur = EL.slots.indexOf(slot); paint(); renderPad(); return; }
  if (pick) { const i = EL.picks.indexOf(pick); st.sel.has(i) ? st.sel.delete(i) : st.sel.add(i); st.wrong.clear(); paint(); msg(""); return; }
  if (cell) {
    const gi = EL.groups.findIndex((g) => g.cells.includes(cell)), ci = EL.groups[gi].cells.indexOf(cell);
    const set = st.cells[gi] || (st.cells[gi] = new Set());
    set.has(ci) ? set.delete(ci) : set.add(ci); paint(); msg(""); return;
  }
  if (l) {
    const li = EL.left.indexOf(l);
    if (st.pairs[li] !== undefined) { delete st.pairs[li]; st.pick = undefined; } else st.pick = li;
    paint(); return;
  }
  if (r && st.pick !== undefined) {
    const ri = EL.right.indexOf(r);
    for (const k of Object.keys(st.pairs)) if (st.pairs[k] === ri) delete st.pairs[k];
    st.pairs[st.pick] = ri; st.pick = undefined; paint(); msg("");
  }
}

/* ---------------------------------------------------------------- keypad */
function renderPad() {
  const st = EL.sec.st, s = EL.slots[st.cur], pad = $("ol-pad");
  if (!pad) return;
  if (st.done) { pad.innerHTML = ""; return; }
  if (!s) { pad.innerHTML = EL.picks.length || EL.groups.length || EL.left.length ? `<span class="hint">${ot("pick")}</span>` : ""; return; }
  const k = s.dataset.k;
  const nextKey = `<button type="button" class="wide2" data-key="next">${ot("keypadNext")} →</button>`;
  if (k === "word") {
    pad.innerHTML = `<input id="ol-word" autocomplete="off" autocapitalize="none" spellcheck="false" placeholder="${ot("word")}" value="${esc(st.vals[st.cur] || "")}">
      <button type="button" class="wide2" data-key="word">${ot("ok")}</button>`;
    return;
  }
  if (k === "bank") { pad.innerHTML = EL.bank.map((w) => `<button type="button" class="wide2" data-put="${esc(w)}">${esc(w)}</button>`).join("") + nextKey; return; }
  if (k === "shape") {
    pad.innerHTML = Object.entries(EL.shapes).map(([name, svg]) => `<button type="button" data-put="${name}" aria-label="${name}">${svg}</button>`).join("") + nextKey;
    return;
  }
  const keys = k === "sign" ? ["<", ">", "="] : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"];
  pad.innerHTML = keys.map((x) => `<button type="button" data-key="${esc(x)}">${esc(x)}</button>`).join("") +
    `<button type="button" data-key="back" aria-label="⌫">⌫</button>` + nextKey;
}
function put(v, replace) {
  const st = EL.sec.st, s = EL.slots[st.cur]; if (!s || st.done) return;
  const old = st.vals[st.cur] || "";
  st.vals[st.cur] = replace ? v : (old + v).slice(0, 3);
  st.wrong.delete(st.cur);
  const want = s.dataset.a;
  // a number of the expected length, a sign, a word from the bank or a shape is complete: go to the next empty box
  const complete = replace || (/^\d+$/.test(want) && st.vals[st.cur].length >= want.length);
  if (complete) nextSlot();
  paint(); renderPad(); msg("");
}
function nextSlot() {
  const st = EL.sec.st, n = EL.slots.length;
  for (let j = 1; j <= n; j++) { const i = (st.cur + j) % n; if (!st.vals[i]) { st.cur = i; return; } }
  st.cur = Math.min(st.cur + 1, n - 1);
}
document.addEventListener("click", (e) => {
  const key = e.target.closest("#ol-pad [data-key]"), putB = e.target.closest("#ol-pad [data-put]");
  if (putB) return put(putB.dataset.put, true);
  if (key) {
    const k = key.dataset.key, st = EL.sec.st;
    if (k === "back") { st.vals[st.cur] = (st.vals[st.cur] || "").slice(0, -1); paint(); return; }
    if (k === "next") { nextSlot(); paint(); renderPad(); return; }
    if (k === "word") return put($("ol-word").value.trim(), true);
    const sign = { "<": "<", ">": ">", "=": "=" }[k];
    return put(sign || k, !!sign);
  }
  const go = e.target.closest("[data-ol-go]");
  if (go) { ol.i = +go.dataset.olGo; return render(); }
  if (e.target.closest("[data-ol-again]")) { ol.secs.forEach((x) => { x.st = newState(); }); ol.i = 0; return render(); }
  if (e.target.closest("[data-ol-today]")) return $("today").click();
});
document.addEventListener("keydown", (e) => {
  if (state.tab !== "online" || !EL.sec || e.target.closest?.("input,select,textarea")) return;
  if (/^[0-9]$/.test(e.key)) put(e.key);
  else if (["<", ">", "="].includes(e.key)) put(e.key, true);
  else if (e.key === "Backspace") { const st = EL.sec.st; st.vals[st.cur] = (st.vals[st.cur] || "").slice(0, -1); paint(); }
  else if (e.key === "Enter") check();
});
document.addEventListener("keydown", (e) => { if (e.key === "Enter" && e.target.id === "ol-word") put(e.target.value.trim(), true); });

/* ---------------------------------------------------------------- checking */
const norm = (s) => String(s).toLowerCase().replace(/­/g, "").replace(/ё/g, "е").replace(/[‐-―-]/g, " ").replace(/\s+/g, " ").trim()
  .normalize("NFD").replace(/[̀-ͯ]/g, "");
function slotRight(s, v) {
  const a = s.dataset.a, k = s.dataset.k;
  if (a === "*") return v !== "";
  if (a === "?") return v !== "";  // number bonds: checked as rows below
  if (k === "word") return norm(v) === norm(a);
  if (k === "bank") return norm(v) === norm(a.replace(/&shy;/g, ""));
  return String(v) === String(a);
}
function score() {  // [right, total, wrong slot indexes]
  const st = EL.sec.st, wrong = new Set();
  let right = 0, total = 0;
  EL.slots.forEach((s, i) => { total++; if (slotRight(s, st.vals[i] ?? "")) right++; else wrong.add(i); });
  // number bonds: each row makes the sum, every pair only once, and not the worked example (0 + n)
  const seen = new Set();
  EL.d.querySelectorAll("[data-sum]").forEach((row) => {
    const n = +row.dataset.sum, [a, b] = [...row.querySelectorAll("[data-a]")].map((s) => EL.slots.indexOf(s));
    const x = +(st.vals[a] ?? NaN), y = +(st.vals[b] ?? NaN), key = `${x}+${y}`;
    const ok = st.vals[a] !== undefined && st.vals[b] !== undefined && x + y === n && !seen.has(key) && !(x === 0 && y === n);
    seen.add(key);
    if (!ok) { if (!wrong.has(a)) { wrong.add(a); right--; } if (!wrong.has(b)) { wrong.add(b); right--; } }
  });
  EL.picks.forEach((p, i) => { total++; if ((p.dataset.p === "1") === st.sel.has(i)) right++; });
  EL.groups.forEach(({ g }, gi) => { total++; if ((st.cells[gi] || new Set()).size === +g.dataset.n) right++; });
  EL.left.forEach((l, li) => { total++; const ri = st.pairs[li]; if (ri !== undefined && EL.right[ri].dataset.mr === l.dataset.ml) right++; });
  return [Math.max(0, right), total, wrong];
}
function msg(text) { if ($("ol-msg")) $("ol-msg").textContent = text; }
function finish(sec, result) {
  const st = sec.st;
  st.done = true; st.result = result;
  if (window.LP && sec.tid) LP.mark(sec.tid, result, "online");
}
function check() {
  const sec = EL.sec, st = sec.st; if (st.done) return;
  const [right, total, wrong] = score();
  if (st.first === null) st.first = total ? right / total : 1;
  st.tries++;
  if (right === total) {
    finish(sec, st.tries === 1 ? "easy" : st.first >= 0.5 ? "ok" : "hard");
    st.wrong.clear(); paint(); msg("★ " + ot("right"));
  } else if (st.tries < 2) {
    st.wrong = wrong; paint(); msg(ot("almost"));
  } else {  // second miss: show the right answers in grey, like the worked example
    st.shown = {};
    EL.slots.forEach((s, i) => { if (wrong.has(i) && s.dataset.a !== "?" && s.dataset.a !== "*") st.shown[i] = s.dataset.k === "shape" ? s.dataset.a : s.dataset.a.replace(/&shy;/g, ""); });
    st.wrong.clear();
    finish(sec, st.first >= 0.5 ? "ok" : "hard"); paint(); msg(ot("shown"));
  }
  renderActions(sec); renderDots();
}
function renderDots() {
  document.querySelectorAll("[data-ol-go]").forEach((b, i) => {
    const x = ol.secs[i]; b.classList.toggle("ok", x.st.done); b.textContent = x.st.done ? "★" : i + 1;
  });
}
function renderActions(sec) {
  const st = sec.st, last = ol.i >= ol.secs.length - 1, act = $("ol-act"); if (!act) return;
  const listen = hasSpeech ? `<button class="btn" type="button" data-ol-say>${SPEAKER.replace("<svg ", '<svg width="20" height="20" ')} ${ot("listen")}</button>` : "";
  const back = ol.i > 0 ? `<button class="btn" type="button" data-ol-prev>← ${ot("prev")}</button>` : "";
  if (st.self === null && EL.self && !st.done) {
    act.innerHTML = `${back}${listen}<button class="btn" type="button" data-ol-self="0">${ot("notYet")}</button>
      <button class="btn dark" type="button" data-ol-self="1">${ot("yes")}</button>`;
    msg(ot("selfQ")); return;
  }
  act.innerHTML = back + listen + (st.done
    ? `<button class="btn dark" type="button" data-ol-next>${last ? ot("done") : ot("next")} →</button>`
    : `<button class="btn dark" type="button" data-ol-check>${ot("check")}</button>`);
}
document.addEventListener("click", (e) => {
  if (!e.target.closest("#ol-act")) return;
  if (e.target.closest("[data-ol-check]")) return check();
  if (e.target.closest("[data-ol-next]")) { ol.i++; return render(); }
  if (e.target.closest("[data-ol-prev]")) { ol.i--; return render(); }
  if (e.target.closest("[data-ol-say]")) return speak(EL.sec.title, state.lang);
  const self = e.target.closest("[data-ol-self]");
  if (self) {
    const sec = EL.sec;
    if (self.dataset.olSelf === "1") { sec.st.first = 1; finish(sec, "easy"); msg("★ " + ot("right")); }
    else { sec.st.first = 0; finish(sec, "hard"); msg(""); }
    sec.st.self = self.dataset.olSelf; renderActions(sec); renderDots();
  }
});

window.LO = { render, ensureTab, reset() { ol = null; } };
ensureTab();
