/* Let's Practice: progress of a child, kept only on this device (localStorage), and "Today's sheet".
   Nothing is sent anywhere. Progress can be saved to a file and loaded on another device.
   Loaded after the main script of index.html and uses its globals (state, catalog, update, ...). */
"use strict";

const PT = {
  en: {
    title: "Progress", hint: "Kept only on this device. Nothing is sent anywhere.", child: "Child", add: "+ Child",
    namePh: "Name or nickname", nameOk: "Add", today: "Today’s sheet",
    todayHint: "Topics for {year}: what was hard, then new ones, and one to keep fresh.",
    rate: "How did it go?", rateBtn: "Mark how it went", rateHint: "Tap for each topic. You can skip any.",
    easy: "Easy", ok: "So-so", hard: "Hard", close: "Done", saved: "Saved. Thank you!",
    map: "Topic map", legend: "★ easy · ✓ so-so · ↺ practise more · – not yet", none: "No marks yet. Print a sheet and mark how it went.",
    save: "Save to a file", load: "Load from a file", loaded: "Progress loaded.", bad: "This file is not Let’s Practice progress.",
    warn: "If the browser data is cleared, progress is lost. Save it to a file now and then.",
    noTopics: "Choose a sheet first.", kid: "Child {n}",
  },
  uk: {
    title: "Прогрес", hint: "Зберігається лише на цьому пристрої. Нікуди не надсилається.", child: "Дитина", add: "+ Дитина",
    namePh: "Ім’я або прізвисько", nameOk: "Додати", today: "Аркуш на сьогодні",
    todayHint: "Теми для {year}: що було важко, потім нові й одна, щоб не забути.",
    rate: "Як пройшло?", rateBtn: "Позначити, як пройшло", rateHint: "Натисніть для кожної теми. Можна пропустити.",
    easy: "Легко", ok: "Так собі", hard: "Важко", close: "Готово", saved: "Збережено. Дякуємо!",
    map: "Карта тем", legend: "★ легко · ✓ так собі · ↺ ще потренуватися · – ще не було", none: "Ще немає позначок. Надрукуйте аркуш і позначте, як пройшло.",
    save: "Зберегти у файл", load: "Завантажити з файлу", loaded: "Прогрес завантажено.", bad: "Це не файл прогресу Let’s Practice.",
    warn: "Якщо очистити дані браузера, прогрес зникне. Іноді зберігайте його у файл.",
    noTopics: "Спершу оберіть аркуш.", kid: "Дитина {n}",
  },
  ru: {
    title: "Прогресс", hint: "Хранится только на этом устройстве. Никуда не отправляется.", child: "Ребёнок", add: "+ Ребёнок",
    namePh: "Имя или прозвище", nameOk: "Добавить", today: "Лист на сегодня",
    todayHint: "Темы для {year}: что было трудно, потом новые и одна, чтобы не забыть.",
    rate: "Как прошло?", rateBtn: "Отметить, как прошло", rateHint: "Нажмите для каждой темы. Можно пропустить.",
    easy: "Легко", ok: "Так себе", hard: "Трудно", close: "Готово", saved: "Сохранено. Спасибо!",
    map: "Карта тем", legend: "★ легко · ✓ так себе · ↺ ещё потренироваться · – ещё не было", none: "Отметок пока нет. Распечатайте лист и отметьте, как прошло.",
    save: "Сохранить в файл", load: "Загрузить из файла", loaded: "Прогресс загружен.", bad: "Это не файл прогресса Let’s Practice.",
    warn: "Если очистить данные браузера, прогресс пропадёт. Иногда сохраняйте его в файл.",
    noTopics: "Сначала выберите лист.", kid: "Ребёнок {n}",
  },
  el: {
    title: "Πρόοδος", hint: "Μένει μόνο σε αυτή τη συσκευή. Δεν στέλνεται πουθενά.", child: "Παιδί", add: "+ Παιδί",
    namePh: "Όνομα ή παρατσούκλι", nameOk: "Προσθήκη", today: "Φύλλο της ημέρας",
    todayHint: "Θέματα για {year}: ό,τι ήταν δύσκολο, μετά νέα και ένα για να μην ξεχαστεί.",
    rate: "Πώς πήγε;", rateBtn: "Σημείωσε πώς πήγε", rateHint: "Πάτησε για κάθε θέμα. Μπορείς να παραλείψεις.",
    easy: "Εύκολο", ok: "Έτσι κι έτσι", hard: "Δύσκολο", close: "Έτοιμο", saved: "Αποθηκεύτηκε. Ευχαριστούμε!",
    map: "Χάρτης θεμάτων", legend: "★ εύκολο · ✓ έτσι κι έτσι · ↺ κι άλλη εξάσκηση · – όχι ακόμα", none: "Δεν υπάρχουν σημειώσεις. Τύπωσε ένα φύλλο και σημείωσε πώς πήγε.",
    save: "Αποθήκευση σε αρχείο", load: "Φόρτωση από αρχείο", loaded: "Η πρόοδος φορτώθηκε.", bad: "Αυτό δεν είναι αρχείο προόδου Let’s Practice.",
    warn: "Αν σβηστούν τα δεδομένα του browser, η πρόοδος χάνεται. Αποθήκευέ τη σε αρχείο πού και πού.",
    noTopics: "Διάλεξε πρώτα ένα φύλλο.", kid: "Παιδί {n}",
  },
  de: {
    title: "Fortschritt", hint: "Nur auf diesem Gerät gespeichert. Nichts wird gesendet.", child: "Kind", add: "+ Kind",
    namePh: "Name oder Spitzname", nameOk: "Hinzufügen", today: "Blatt für heute",
    todayHint: "Themen für {year}: was schwer war, dann neue und eins zum Wiederholen.",
    rate: "Wie war es?", rateBtn: "Markieren, wie es war", rateHint: "Für jedes Thema tippen. Überspringen geht auch.",
    easy: "Leicht", ok: "Geht so", hard: "Schwer", close: "Fertig", saved: "Gespeichert. Danke!",
    map: "Themenkarte", legend: "★ leicht · ✓ geht so · ↺ mehr üben · – noch nicht", none: "Noch keine Markierungen. Drucke ein Blatt und markiere, wie es war.",
    save: "In Datei speichern", load: "Aus Datei laden", loaded: "Fortschritt geladen.", bad: "Diese Datei ist kein Let’s-Practice-Fortschritt.",
    warn: "Werden die Browserdaten gelöscht, ist der Fortschritt weg. Speichere ihn ab und zu in eine Datei.",
    noTopics: "Wähle zuerst ein Blatt.", kid: "Kind {n}",
  },
  fr: {
    title: "Progrès", hint: "Gardé seulement sur cet appareil. Rien n’est envoyé.", child: "Enfant", add: "+ Enfant",
    namePh: "Prénom ou surnom", nameOk: "Ajouter", today: "Fiche du jour",
    todayHint: "Thèmes pour {year} : ce qui était difficile, puis des nouveaux et un à revoir.",
    rate: "Comment ça s’est passé ?", rateBtn: "Noter comment ça s’est passé", rateHint: "Touchez pour chaque thème. Vous pouvez passer.",
    easy: "Facile", ok: "Moyen", hard: "Difficile", close: "Terminé", saved: "Enregistré. Merci !",
    map: "Carte des thèmes", legend: "★ facile · ✓ moyen · ↺ à retravailler · – pas encore", none: "Pas encore de notes. Imprimez une fiche et notez comment ça s’est passé.",
    save: "Enregistrer dans un fichier", load: "Charger un fichier", loaded: "Progrès chargés.", bad: "Ce fichier n’est pas un fichier de progrès Let’s Practice.",
    warn: "Si les données du navigateur sont effacées, les progrès sont perdus. Enregistrez-les de temps en temps.",
    noTopics: "Choisissez d’abord une fiche.", kid: "Enfant {n}",
  },
  es: {
    title: "Progreso", hint: "Se guarda solo en este dispositivo. No se envía nada.", child: "Niño/a", add: "+ Niño/a",
    namePh: "Nombre o apodo", nameOk: "Añadir", today: "Ficha de hoy",
    todayHint: "Temas para {year}: lo que fue difícil, luego nuevos y uno para repasar.",
    rate: "¿Qué tal fue?", rateBtn: "Marcar qué tal fue", rateHint: "Toque en cada tema. Puede saltar alguno.",
    easy: "Fácil", ok: "Regular", hard: "Difícil", close: "Listo", saved: "Guardado. ¡Gracias!",
    map: "Mapa de temas", legend: "★ fácil · ✓ regular · ↺ practicar más · – todavía no", none: "Aún no hay marcas. Imprima una ficha y marque qué tal fue.",
    save: "Guardar en un archivo", load: "Cargar de un archivo", loaded: "Progreso cargado.", bad: "Este archivo no es un progreso de Let’s Practice.",
    warn: "Si se borran los datos del navegador, el progreso se pierde. Guárdelo en un archivo de vez en cuando.",
    noTopics: "Elija primero una ficha.", kid: "Niño/a {n}",
  },
};
const pt = (k, o) => fmt(PT[state.ui][k], o || {});
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

/* ---------------------------------------------------------------- storage */
const STORE = "lp-progress";
const RESULTS = ["easy", "ok", "hard"];
function emptyProgress() { return { app: "lets-practice", v: 1, cur: "k1", kids: [{ id: "k1", name: "" }], topics: { k1: {} } }; }
function validProgress(p) {
  return p && p.app === "lets-practice" && p.v === 1 && Array.isArray(p.kids) && p.kids.length && p.topics && typeof p.topics === "object";
}
let progress = (() => {
  try { const p = JSON.parse(localStorage.getItem(STORE)); if (validProgress(p)) return p; } catch { /* blocked or broken */ }
  return emptyProgress();
})();
function saveProgress() { try { localStorage.setItem(STORE, JSON.stringify(progress)); } catch { /* storage blocked: keep in memory */ } }
const kidTopics = () => progress.topics[progress.cur] || (progress.topics[progress.cur] = {});
const today = () => new Date().toISOString().slice(0, 10);
// marks of a topic: [[date, "easy" | "ok" | "hard", "paper" | "online"], ...], newest last
function mark(tid, result, how) {
  const t = kidTopics(), m = t[tid] || (t[tid] = []);
  m.push([today(), result, how]);
  if (m.length > 30) m.splice(0, m.length - 30);
  saveProgress();
}
const lastMark = (tid) => { const m = kidTopics()[tid]; return m && m.length ? m[m.length - 1] : null; };

/* ---------------------------------------------------------------- topics of the catalogue */
function topicInfo() {  // variant id -> {row, title, label, year, index}
  const c = catalog(), out = {};
  if (!c) return out;
  c.rows.forEach((r, ri) => r.variants.forEach((v, vi) => {
    out[v.id] = { row: r, title: r.title, label: v.label, year: r.year, ri, vi };
  }));
  return out;
}
function sheetTopicIds() {  // topic ids of the sheet on screen, in order
  if (!state.sheet) return [];
  if (isTopics(state.level)) return state.level.slice(2).split("_");
  const map = (catalog() && catalog().stage_ids) || {}, ids = [];
  for (const body of state.sheet.pages) {
    for (const m of body.matchAll(/data-task="([\w]+)"/g)) if (map[m[1]] && !ids.includes(map[m[1]])) ids.push(map[m[1]]);
  }
  return ids;
}

/* ---------------------------------------------------------------- "How did it go?" */
function showRate() {
  const ids = sheetTopicIds(), info = topicInfo();
  if (!ids.length) return toast(pt("noTopics"));
  const sym = { easy: "★", ok: "✓", hard: "↺" };
  $("rate").innerHTML = `<div class="rate-head"><b>${pt("rate")}</b><span>${pt("rateHint")}</span>
      <button class="btn dark" type="button" data-rate-close>${pt("close")}</button></div>` +
    ids.map((id, i) => {
      const x = info[id] || { title: id, label: "" };
      return `<div class="rate-row" data-rate-topic="${id}"><span class="n">${i + 1}</span>
        <span class="rate-name">${x.title}${x.label ? ` <small>· ${x.label}</small>` : ""}</span>
        <span class="rate-btns">${RESULTS.map((r) => `<button class="chip" type="button" data-rate="${r}" aria-pressed="false">${sym[r]} ${pt(r)}</button>`).join("")}</span></div>`;
    }).join("");
  $("rate").hidden = false;
  $("rate").scrollIntoView({ behavior: "smooth", block: "nearest" });
}
$("rate").addEventListener("click", (e) => {
  if (e.target.closest("[data-rate-close]")) {
    const rows = [...$("rate").querySelectorAll("[data-rate-topic]")];
    let n = 0;
    for (const row of rows) {
      const on = row.querySelector('[data-rate][aria-pressed="true"]');
      if (on) { mark(row.dataset.rateTopic, on.dataset.rate, "paper"); n++; }
    }
    $("rate").hidden = true;
    if (n) toast(pt("saved"));
    renderProgress();
    return;
  }
  const b = e.target.closest("[data-rate]"); if (!b) return;
  b.parentElement.querySelectorAll("[data-rate]").forEach((x) => x.setAttribute("aria-pressed", x === b));
});

/* ---------------------------------------------------------------- today's sheet */
// The variant to practise in a row: the last one practised; up after 2 "easy" in a row, down after 2 "hard".
function rowVariant(r) {
  let best = null;
  r.variants.forEach((v, i) => { const m = lastMark(v.id); if (m && (!best || m[0] >= best.date)) best = { i, date: m[0] }; });
  if (!best) return { i: 0, date: null, last: null };
  const marks = kidTopics()[r.variants[best.i].id], two = marks.slice(-2).map((m) => m[1]);
  const last = marks[marks.length - 1][1];
  let i = best.i;
  if (two.length === 2 && two.every((x) => x === "easy") && i < r.variants.length - 1) i++;
  if (two.length === 2 && two.every((x) => x === "hard") && i > 0) i--;
  return { i, date: best.date, last };
}
function todayTopics(year) {
  const c = catalog(); if (!c) return [];
  const rows = c.rows.filter((r) => r.year === year && (r.subject || "maths") === state.subject);
  const n = { R: 4, Y1: 6, Y2: 6 }[year] || 6;
  const st = rows.map((r, order) => ({ r, order, ...rowVariant(r) }));
  const hard = st.filter((x) => x.last === "hard").sort((a, b) => (a.date < b.date ? 1 : -1));
  const fresh = st.filter((x) => !x.last);
  const known = st.filter((x) => x.last && x.last !== "hard").sort((a, b) => (a.date < b.date ? -1 : 1));  // oldest first
  const picked = [];
  const take = (list, k) => { for (const x of list) { if (picked.length >= k) break; if (!picked.includes(x)) picked.push(x); } };
  take(hard, Math.ceil(n / 2));
  take(fresh, n - 1);
  take(known, n);
  take(fresh, n); take(hard, n);
  return picked.sort((a, b) => a.order - b.order).map((x) => x.r.variants[x.i].id);
}
function makeToday() {
  const ids = todayTopics(state.year);
  if (!ids.length) return toast(catalog() ? catalog().soon_year : pt("noTopics"));
  state.level = `T:${ids.join("_")}`;
  syncFromLevel(); renderPanel();
  setSeed(randomSeed());
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* ---------------------------------------------------------------- the progress block */
const SYM = { easy: "★", ok: "✓", hard: "↺" };
function kidName(k, i) { return k.name || pt("kid", { n: i + 1 }); }
function renderProgress() {
  if (!$("progress-block")) return;
  $("kids").innerHTML = progress.kids.map((k, i) =>
    `<button class="chip" type="button" data-kid="${k.id}" aria-pressed="${k.id === progress.cur}">${esc(kidName(k, i))}</button>`).join("") +
    `<button class="chip" type="button" id="kid-add">${pt("add")}</button>`;
  $("today-hint").textContent = pt("todayHint", { year: yearName(state.year) });
  $("today").disabled = !subjectReady();
  renderMap();
}
function renderMap() {
  const c = catalog();
  $("map-legend").textContent = pt("legend");
  if (!c) { $("map").innerHTML = ""; return; }
  const rows = c.rows.filter((r) => r.year === state.year && (r.subject || "maths") === state.subject);
  const any = rows.some((r) => r.variants.some((v) => lastMark(v.id)));
  if (!any) { $("map").innerHTML = `<p class="hint" style="margin:0">${pt("none")}</p>`; return; }
  let html = "", strand = null;
  for (const r of rows) {
    if (r.strand !== strand) { strand = r.strand; html += `<p class="strand">${c.strands[strand]}</p>`; }
    const marks = r.variants.map((v) => { const m = lastMark(v.id); return `<span title="${esc(v.label || r.title)}">${m ? SYM[m[1]] : "–"}</span>`; }).join("");
    html += `<div class="maprow"><span>${r.title}</span><span class="marks">${marks}</span></div>`;
  }
  $("map").innerHTML = html;
}
$("kids").addEventListener("click", (e) => {
  if (e.target.closest("#kid-add")) { $("kid-form").hidden = false; $("kid-name").focus(); return; }
  const b = e.target.closest("[data-kid]"); if (!b) return;
  progress.cur = b.dataset.kid; saveProgress(); renderProgress();
});
$("kid-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const name = $("kid-name").value.trim().slice(0, 30);
  const id = "k" + (Math.max(0, ...progress.kids.map((k) => +k.id.slice(1) || 0)) + 1);
  progress.kids.push({ id, name }); progress.topics[id] = {}; progress.cur = id;
  $("kid-name").value = ""; $("kid-form").hidden = true;
  saveProgress(); renderProgress();
});
$("today").addEventListener("click", makeToday);
$("rate-open").addEventListener("click", showRate);
$("prog-save").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(progress, null, 1)], { type: "application/json" });
  const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `lets-practice-progress-${today()}.json` });
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
});
$("prog-load").addEventListener("click", () => $("prog-file").click());
$("prog-file").addEventListener("change", async () => {
  const f = $("prog-file").files[0]; $("prog-file").value = "";
  if (!f) return;
  try {
    const p = JSON.parse(await f.text());
    if (!validProgress(p)) throw new Error("bad");
    if (!p.kids.some((k) => k.id === p.cur)) p.cur = p.kids[0].id;
    progress = p; saveProgress(); renderProgress(); toast(pt("loaded"));
  } catch { toast(pt("bad")); }
});
// after printing the worksheet: ask how it went (it can be skipped)
$("print-sheet").addEventListener("click", () => setTimeout(showRate, 800));

window.LP = {
  render() { if (!$("progress-block")) return; document.querySelectorAll("[data-pt]").forEach((el) => { el.textContent = pt(el.dataset.pt); });
    $("kid-name").placeholder = pt("namePh"); renderProgress(); },
  onSheet() { $("rate").hidden = true; renderProgress(); },
  mark, sheetTopicIds,
};
LP.render();
