const state = {
  stages: [],
  topicMap: new Map(),
  user: null,
  completed: new Set(),
  notes: {},
  quizResults: {},
  totalXp: 0,
  streakDays: 0,
  filter: "all",
  search: "",
  authMode: "login",
  collapsedStages: new Set(),
  activeLessonId: null,
  activeLessonTab: "theory",
  flashcardIndex: 0,
  flashcards: [],
  pomodoroSeconds: 25 * 60,
  pomodoroRunning: false,
  pomodoroTimerId: null,
};

const el = {
  authArea: document.getElementById("authArea"),
  guestBanner: document.getElementById("guestBanner"),
  bannerRegisterBtn: document.getElementById("bannerRegisterBtn"),
  bannerLoginBtn: document.getElementById("bannerLoginBtn"),
  themeToggleBtn: document.getElementById("themeToggleBtn"),
  overallPercent: document.getElementById("overallPercent"),
  overallBar: document.getElementById("overallBar"),
  progressSubtitle: document.getElementById("progressSubtitle"),
  completedCountText: document.getElementById("completedCountText"),
  activeStageHint: document.getElementById("activeStageHint"),
  xpValue: document.getElementById("xpValue"),
  streakValue: document.getElementById("streakValue"),
  quizzesValue: document.getElementById("quizzesValue"),
  searchInput: document.getElementById("searchInput"),
  filterPills: document.getElementById("filterPills"),
  stageNav: document.getElementById("stageNav"),
  stagesContainer: document.getElementById("stagesContainer"),
  // Auth
  authModal: document.getElementById("authModal"),
  closeModalBtn: document.getElementById("closeModalBtn"),
  tabLogin: document.getElementById("tabLogin"),
  tabRegister: document.getElementById("tabRegister"),
  authModalTitle: document.getElementById("authModalTitle"),
  authModalDesc: document.getElementById("authModalDesc"),
  authForm: document.getElementById("authForm"),
  usernameInput: document.getElementById("usernameInput"),
  displayNameField: document.getElementById("displayNameField"),
  displayNameInput: document.getElementById("displayNameInput"),
  passwordInput: document.getElementById("passwordInput"),
  authError: document.getElementById("authError"),
  authSubmitBtn: document.getElementById("authSubmitBtn"),
  // Lesson
  lessonModal: document.getElementById("lessonModal"),
  closeLessonBtn: document.getElementById("closeLessonBtn"),
  lessonDoneCloseBtn: document.getElementById("lessonDoneCloseBtn"),
  lessonStageBadge: document.getElementById("lessonStageBadge"),
  lessonTitle: document.getElementById("lessonTitle"),
  lessonTabs: document.getElementById("lessonTabs"),
  lessonBody: document.getElementById("lessonBody"),
  lessonCompleteCheckbox: document.getElementById("lessonCompleteCheckbox"),
  // Playground
  openPlaygroundBtn: document.getElementById("openPlaygroundBtn"),
  playgroundModal: document.getElementById("playgroundModal"),
  closePlaygroundBtn: document.getElementById("closePlaygroundBtn"),
  playgroundCode: document.getElementById("playgroundCode"),
  runCodeBtn: document.getElementById("runCodeBtn"),
  clearOutputBtn: document.getElementById("clearOutputBtn"),
  playgroundOutput: document.getElementById("playgroundOutput"),
  // Flashcards
  openFlashcardsBtn: document.getElementById("openFlashcardsBtn"),
  flashcardsModal: document.getElementById("flashcardsModal"),
  closeFlashcardsBtn: document.getElementById("closeFlashcardsBtn"),
  flashcardMeta: document.getElementById("flashcardMeta"),
  flashcardTopic: document.getElementById("flashcardTopic"),
  flashcardQ: document.getElementById("flashcardQ"),
  flashcardA: document.getElementById("flashcardA"),
  flashcardToggleAnswerBtn: document.getElementById("flashcardToggleAnswerBtn"),
  flashcardNextBtn: document.getElementById("flashcardNextBtn"),
  // Pomodoro
  pomodoroTime: document.getElementById("pomodoroTime"),
  pomodoroToggleBtn: document.getElementById("pomodoroToggleBtn"),
  pomodoroResetBtn: document.getElementById("pomodoroResetBtn"),
  toastContainer: document.getElementById("toastContainer"),
};

function refreshIcons() {
  if (window.lucide) window.lucide.createIcons();
}

function showModal(modalEl) {
  modalEl.classList.remove("hidden");
}

function hideModal(modalEl) {
  modalEl.classList.add("hidden");
}

function showToast(message) {
  const node = document.createElement("div");
  node.className =
    "px-4 py-2.5 rounded-xl text-xs font-medium bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 shadow-lg border border-zinc-800 dark:border-zinc-200";
  node.textContent = message;
  el.toastContainer.appendChild(node);
  setTimeout(() => node.remove(), 3200);
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function api(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    credentials: "same-origin",
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Сталася помилка запиту");
  return data;
}

/* ---------- Theme ---------- */
function applyTheme(theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
  localStorage.setItem("pypath_theme", theme);
  el.themeToggleBtn.innerHTML =
    theme === "dark"
      ? `<i data-lucide="sun" class="w-4 h-4"></i>`
      : `<i data-lucide="moon" class="w-4 h-4"></i>`;
  refreshIcons();
}

function toggleTheme() {
  const isDark = document.documentElement.classList.contains("dark");
  applyTheme(isDark ? "light" : "dark");
}

/* ---------- Pomodoro ---------- */
function renderPomodoro() {
  const m = String(Math.floor(state.pomodoroSeconds / 60)).padStart(2, "0");
  const s = String(state.pomodoroSeconds % 60).padStart(2, "0");
  el.pomodoroTime.textContent = `${m}:${s}`;
  el.pomodoroToggleBtn.innerHTML = state.pomodoroRunning
    ? `<i data-lucide="pause" class="w-3 h-3"></i>`
    : `<i data-lucide="play" class="w-3 h-3"></i>`;
  refreshIcons();
}

function togglePomodoro() {
  if (state.pomodoroRunning) {
    clearInterval(state.pomodoroTimerId);
    state.pomodoroRunning = false;
  } else {
    state.pomodoroRunning = true;
    state.pomodoroTimerId = setInterval(() => {
      if (state.pomodoroSeconds > 0) {
        state.pomodoroSeconds--;
        renderPomodoro();
      } else {
        clearInterval(state.pomodoroTimerId);
        state.pomodoroRunning = false;
        renderPomodoro();
        showToast("Час фокусу завершено! Зроби 5 хвилин перерви.");
      }
    }, 1000);
  }
  renderPomodoro();
}

function resetPomodoro() {
  clearInterval(state.pomodoroTimerId);
  state.pomodoroRunning = false;
  state.pomodoroSeconds = 25 * 60;
  renderPomodoro();
}

/* ---------- Auth ---------- */
function openAuthModal(mode = "login") {
  state.authMode = mode;
  const isReg = mode === "register";

  const activeCls = "py-1.5 rounded-md text-xs font-medium bg-white dark:bg-zinc-950 text-zinc-900 dark:text-white shadow-2xs transition cursor-pointer";
  const idleCls = "py-1.5 rounded-md text-xs font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-white transition cursor-pointer";
  el.tabLogin.className = isReg ? idleCls : activeCls;
  el.tabRegister.className = isReg ? activeCls : idleCls;

  el.displayNameField.classList.toggle("hidden", !isReg);
  el.authModalTitle.textContent = isReg ? "Створити акаунт" : "Увійти в акаунт";
  el.authModalDesc.textContent = isReg
    ? "Зареєструйся, щоб твій прогрес, XP, тести та нотатки зберігалися на сервері."
    : "Твій прогрес та нотатки завантажаться автоматично.";
  el.authSubmitBtn.textContent = isReg ? "Зареєструватися" : "Увійти";
  el.authError.classList.add("hidden");
  showModal(el.authModal);
  el.usernameInput.focus();
}

function closeAuthModal() {
  hideModal(el.authModal);
  el.authForm.reset();
  el.authError.classList.add("hidden");
}

function renderAuthArea() {
  if (state.user) {
    el.guestBanner.classList.add("hidden");
    el.authArea.innerHTML = `
      <div class="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900 text-xs">
        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
        <span class="font-medium">${escapeHtml(state.user.display_name)}</span>
      </div>
      <button id="logoutBtn" class="px-2.5 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition cursor-pointer">
        Вийти
      </button>
    `;
    document.getElementById("logoutBtn").addEventListener("click", handleLogout);
  } else {
    el.guestBanner.classList.remove("hidden");
    el.authArea.innerHTML = `
      <button id="loginBtn" class="px-2.5 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition cursor-pointer">
        Увійти
      </button>
      <button id="registerBtn" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 hover:opacity-90 transition cursor-pointer">
        Реєстрація
      </button>
    `;
    document.getElementById("loginBtn").addEventListener("click", () => openAuthModal("login"));
    document.getElementById("registerBtn").addEventListener("click", () => openAuthModal("register"));
  }
}

/* ---------- Stats & Render ---------- */
function computeStats() {
  let totalTopics = 0;
  let completedTopics = 0;
  let totalQuizzes = 0;
  let passedQuizzes = 0;
  let nextStageTitle = "Усі етапи завершено";
  let foundNext = false;

  for (const stage of state.stages) {
    let stageDone = 0;
    for (const topic of stage.topics) {
      totalTopics++;
      if (state.completed.has(topic.id)) {
        completedTopics++;
        stageDone++;
      }
      if (topic.quiz && topic.quiz.length > 0) {
        totalQuizzes++;
        const qr = state.quizResults[topic.id];
        if (qr && qr.score === qr.total) passedQuizzes++;
      }
    }
    if (!foundNext && stageDone < stage.topics.length) {
      nextStageTitle = `Поточний фокус: Етап ${stage.number}`;
      foundNext = true;
    }
  }

  const pct = totalTopics ? Math.round((completedTopics / totalTopics) * 100) : 0;
  el.overallPercent.textContent = `${pct}%`;
  el.overallBar.style.width = `${pct}%`;
  el.completedCountText.textContent = `${completedTopics} з ${totalTopics} тем виконано`;
  el.activeStageHint.textContent = nextStageTitle;
  el.progressSubtitle.textContent = state.user
    ? `Акаунт ${state.user.display_name} · прогрес синхронізується автоматично`
    : "Створи акаунт, щоб зберегти свій шлях навчання";

  el.xpValue.textContent = `${state.totalXp} XP`;
  el.streakValue.textContent = `${state.streakDays} дн.`;
  el.quizzesValue.textContent = `${passedQuizzes} / ${totalQuizzes}`;
}

function renderStageNav() {
  el.stageNav.innerHTML = state.stages
    .map((stage) => {
      const done = stage.topics.filter((t) => state.completed.has(t.id)).length;
      const total = stage.topics.length;
      const isDone = done === total && total > 0;
      const badgeCls = isDone
        ? "bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-900"
        : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500 dark:text-zinc-400 border-zinc-200 dark:border-zinc-700";

      return `
        <a href="#${stage.id}" class="flex items-center justify-between gap-2 px-2.5 py-2 rounded-lg text-xs hover:bg-zinc-100 dark:hover:bg-zinc-800/70 transition">
          <span class="truncate text-zinc-700 dark:text-zinc-300">
            <span class="font-semibold text-zinc-900 dark:text-white">${stage.number}.</span> ${escapeHtml(stage.title.replace(/^ЕТАП \d+:\s*/, ""))}
          </span>
          <span class="px-1.5 py-0.5 rounded text-[11px] font-mono border shrink-0 ${badgeCls}">${done}/${total}</span>
        </a>
      `;
    })
    .join("");
}

function topicMatchesFilter(topic) {
  const isDone = state.completed.has(topic.id);
  if (state.filter === "done" && !isDone) return false;
  if (state.filter === "todo" && isDone) return false;
  const q = state.search.trim().toLowerCase();
  if (!q) return true;
  const hay = `${topic.title} ${topic.summary} ${topic.practice} ${topic.tags.join(" ")}`.toLowerCase();
  return hay.includes(q);
}

function renderStages() {
  const htmlParts = [];
  for (const stage of state.stages) {
    const visibleTopics = stage.topics.filter(topicMatchesFilter);
    if (visibleTopics.length === 0) continue;

    const total = stage.topics.length;
    const done = stage.topics.filter((t) => state.completed.has(t.id)).length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    const collapsed = state.collapsedStages.has(stage.id);

    const topicsHtml = collapsed
      ? ""
      : `<div class="divide-y divide-zinc-200/80 dark:divide-zinc-800/80 border-t border-zinc-200/80 dark:border-zinc-800/80">
          ${visibleTopics
            .map((topic) => {
              const checked = state.completed.has(topic.id);
              const qr = state.quizResults[topic.id];
              const quizBadge =
                qr && qr.score === qr.total
                  ? `<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-900">Тест ${qr.score}/${qr.total}</span>`
                  : "";
              const hasNote = Boolean((state.notes[topic.id] || "").trim());

              return `
                <div class="p-4 sm:p-5 transition ${checked ? "bg-emerald-50/30 dark:bg-emerald-950/10" : "hover:bg-zinc-50/70 dark:hover:bg-zinc-800/25"}">
                  <div class="flex items-start gap-3.5">
                    <input
                      type="checkbox"
                      data-action="toggle"
                      data-topic-id="${topic.id}"
                      ${checked ? "checked" : ""}
                      aria-label="Позначити тему виконаною"
                      class="mt-1 w-4 h-4 rounded border-zinc-300 dark:border-zinc-700 accent-zinc-900 dark:accent-white cursor-pointer shrink-0"
                    />
                    <div class="flex-1 min-w-0">
                      <div class="flex flex-wrap items-center justify-between gap-2 mb-1">
                        <h3 class="text-sm sm:text-base font-semibold tracking-tight ${checked ? "line-through text-zinc-400 dark:text-zinc-500" : ""}">
                          ${escapeHtml(topic.title)}
                        </h3>
                        <div class="flex items-center gap-1.5">
                          ${quizBadge}
                          ${hasNote ? '<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium bg-amber-50 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-900">Нотатка</span>' : ""}
                        </div>
                      </div>

                      <p class="text-xs sm:text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed mb-2.5">${escapeHtml(topic.summary)}</p>

                      <div class="flex flex-wrap gap-1.5 mb-3">
                        ${topic.tags.map((t) => `<span class="px-2 py-0.5 rounded-md text-[11px] font-mono bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300 border border-zinc-200/70 dark:border-zinc-700/70">${escapeHtml(t)}</span>`).join("")}
                      </div>

                      <div class="rounded-lg border border-zinc-200/80 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950/60 px-3 py-2 text-xs text-zinc-600 dark:text-zinc-300 mb-3">
                        <span class="font-semibold text-zinc-900 dark:text-zinc-100">Практика:</span> ${escapeHtml(topic.practice)}
                      </div>

                      <div class="flex flex-wrap items-center gap-2">
                        <button data-action="open-lesson" data-topic-id="${topic.id}" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 hover:opacity-90 transition cursor-pointer">
                          <i data-lucide="book-open" class="w-3.5 h-3.5"></i> Відкрити урок
                        </button>
                        <button data-action="open-lesson-quiz" data-topic-id="${topic.id}" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition cursor-pointer">
                          <i data-lucide="check-circle" class="w-3.5 h-3.5 text-zinc-500"></i> Міні-тест
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              `;
            })
            .join("")}
        </div>`;

    htmlParts.push(`
      <section id="${stage.id}" class="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 shadow-xs overflow-hidden">
        <div data-action="toggle-stage" data-stage-id="${stage.id}" class="p-5 cursor-pointer hover:bg-zinc-50/60 dark:hover:bg-zinc-800/20 transition">
          <div class="flex items-start justify-between gap-4">
            <div>
              <span class="inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-medium bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-300 border border-zinc-200 dark:border-zinc-700 mb-2">
                ${escapeHtml(stage.duration)}
              </span>
              <h2 class="text-base sm:text-lg font-semibold tracking-tight">${escapeHtml(stage.title)}</h2>
              <p class="text-xs sm:text-sm text-zinc-500 dark:text-zinc-400 mt-1">${escapeHtml(stage.goal)}</p>
            </div>
            <span class="text-xs text-zinc-400 shrink-0">${collapsed ? "Розгорнути ▾" : "Згорнути ▴"}</span>
          </div>
          <div class="flex items-center gap-3 mt-4">
            <div class="flex-1 h-1.5 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
              <div class="h-full rounded-full bg-zinc-900 dark:bg-white transition-all duration-300" style="width: ${pct}%"></div>
            </div>
            <span class="text-xs font-mono text-zinc-500 dark:text-zinc-400 tabular-nums">${done}/${total} (${pct}%)</span>
          </div>
        </div>
        ${topicsHtml}
      </section>
    `);
  }

  el.stagesContainer.innerHTML =
    htmlParts.join("") ||
    `<div class="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-10 text-center text-sm text-zinc-500">За вашим запитом тем не знайдено.</div>`;
  refreshIcons();
}

function renderAll() {
  renderAuthArea();
  computeStats();
  renderStageNav();
  renderStages();
}

/* ---------- Lesson Modal ---------- */
function openLessonModal(topicId, tab = "theory") {
  const entry = state.topicMap.get(topicId);
  if (!entry) return;
  state.activeLessonId = topicId;
  state.activeLessonTab = tab;

  el.lessonStageBadge.textContent = `Етап ${entry.stage.number}`;
  el.lessonTitle.textContent = entry.topic.title;
  el.lessonCompleteCheckbox.checked = state.completed.has(topicId);
  renderLessonTab();
  showModal(el.lessonModal);
}

function closeLessonModal() {
  hideModal(el.lessonModal);
  state.activeLessonId = null;
}

function renderLessonTab() {
  const entry = state.topicMap.get(state.activeLessonId);
  if (!entry) return;
  const { topic } = entry;

  const activeCls = "pb-2.5 border-b-2 border-zinc-900 dark:border-white font-medium text-zinc-900 dark:text-white cursor-pointer whitespace-nowrap";
  const idleCls = "pb-2.5 border-b-2 border-transparent font-medium text-zinc-500 hover:text-zinc-900 dark:hover:text-white cursor-pointer whitespace-nowrap";
  for (const btn of el.lessonTabs.querySelectorAll("button[data-ltab]")) {
    btn.className = btn.dataset.ltab === state.activeLessonTab ? activeCls : idleCls;
  }

  if (state.activeLessonTab === "theory") {
    const theoryHtml = (topic.theory || [topic.summary])
      .map((p) => `<p class="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed">${escapeHtml(p)}</p>`)
      .join("");
    const codeHtml = topic.code
      ? `<div class="rounded-xl border border-zinc-200 dark:border-zinc-800 overflow-hidden bg-zinc-950">
           <div class="px-4 py-2 border-b border-zinc-800 flex items-center justify-between bg-zinc-900/60">
             <span class="text-xs font-mono text-zinc-400">example.py</span>
             <div class="flex items-center gap-2">
               <button id="copyLessonCodeBtn" class="px-2.5 py-1 rounded-md text-xs font-medium text-zinc-300 hover:bg-zinc-800 transition cursor-pointer">Копіювати</button>
               <button id="runInPlaygroundBtn" class="px-2.5 py-1 rounded-md text-xs font-medium bg-white text-zinc-900 hover:opacity-90 transition cursor-pointer">Запустити</button>
             </div>
           </div>
           <pre class="p-4 text-xs sm:text-sm font-mono text-zinc-100 overflow-x-auto leading-relaxed">${escapeHtml(topic.code)}</pre>
         </div>`
      : "";
    const docsHtml = (topic.docs || []).length
      ? `<div class="flex flex-wrap gap-2">
           ${topic.docs
             .map(
               (d) =>
                 `<a class="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition" href="${escapeHtml(d.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(d.label)} ↗</a>`
             )
             .join("")}
         </div>`
      : "";

    el.lessonBody.innerHTML = `
      <div class="space-y-3">${theoryHtml}</div>
      <div class="rounded-lg border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 p-3.5 text-xs sm:text-sm">
        <span class="font-semibold">Практичне завдання:</span> ${escapeHtml(topic.practice)}
      </div>
      ${codeHtml}
      ${docsHtml}
    `;

    const copyBtn = document.getElementById("copyLessonCodeBtn");
    if (copyBtn) {
      copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(topic.code);
        showToast("Код скопійовано");
      });
    }
    const runBtn = document.getElementById("runInPlaygroundBtn");
    if (runBtn) {
      runBtn.addEventListener("click", () => openPlayground(topic.code));
    }
  } else if (state.activeLessonTab === "quiz") {
    const quiz = topic.quiz || [];
    if (!quiz.length) {
      el.lessonBody.innerHTML = `<p class="text-sm text-zinc-500">Для цієї теми тест поки відсутній.</p>`;
      return;
    }
    el.lessonBody.innerHTML = `
      <form id="lessonQuizForm" class="space-y-4">
        ${quiz
          .map(
            (q, qi) => `
          <div class="rounded-xl border border-zinc-200 dark:border-zinc-800 p-4 quiz-item" data-qi="${qi}">
            <div class="text-sm font-semibold mb-3">${qi + 1}. ${escapeHtml(q.q)}</div>
            <div class="space-y-2">
              ${q.options
                .map(
                  (opt, oi) => `
                <label class="flex items-center gap-2.5 p-2.5 rounded-lg border border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-800/40 cursor-pointer quiz-opt transition">
                  <input type="radio" name="q_${qi}" value="${oi}" required class="accent-zinc-900 dark:accent-white" />
                  <span class="text-xs sm:text-sm">${escapeHtml(opt)}</span>
                </label>`
                )
                .join("")}
            </div>
          </div>`
          )
          .join("")}
        <button type="submit" class="px-4 py-2 rounded-lg text-xs font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 hover:opacity-90 transition cursor-pointer">
          Перевірити відповіді
        </button>
      </form>
      <div id="quizResultBox" class="hidden"></div>
    `;

    document.getElementById("lessonQuizForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const answers = quiz.map((_, qi) => {
        const checked = e.target.querySelector(`input[name="q_${qi}"]:checked`);
        return checked ? Number(checked.value) : -1;
      });
      try {
        const res = await api(`/api/quiz/${topic.id}`, {
          method: "POST",
          body: JSON.stringify({ answers }),
        });
        res.correct_indices.forEach((correctIdx, qi) => {
          const item = el.lessonBody.querySelector(`.quiz-item[data-qi="${qi}"]`);
          const opts = item.querySelectorAll(".quiz-opt");
          opts.forEach((optEl, oi) => {
            optEl.classList.remove("correct", "wrong");
            if (oi === correctIdx) optEl.classList.add("correct");
            else if (answers[qi] === oi) optEl.classList.add("wrong");
          });
        });

        const box = document.getElementById("quizResultBox");
        box.classList.remove("hidden");
        box.innerHTML = res.passed
          ? `<div class="rounded-lg border border-emerald-200 dark:border-emerald-900 bg-emerald-50 dark:bg-emerald-950/40 p-3 text-xs sm:text-sm text-emerald-800 dark:text-emerald-300"><strong>Чудово!</strong> ${res.score}/${res.total} правильних. ${res.xp_earned ? `+${res.xp_earned} XP!` : ""}</div>`
          : `<div class="rounded-lg border border-red-200 dark:border-red-900 bg-red-50 dark:bg-red-950/40 p-3 text-xs sm:text-sm text-red-700 dark:text-red-300">Результат: ${res.score}/${res.total}. Спробуйте ще раз!</div>`;

        if (state.user) {
          state.quizResults[topic.id] = { score: res.score, total: res.total };
          state.totalXp = res.total_xp;
          state.streakDays = res.streak_days;
          renderAll();
        }
      } catch (err) {
        showToast(err.message);
      }
    });
  } else if (state.activeLessonTab === "interview") {
    const iv = topic.interview;
    if (!iv) {
      el.lessonBody.innerHTML = `<p class="text-sm text-zinc-500">Питання зі співбесіди для цієї теми відсутнє.</p>`;
      return;
    }
    el.lessonBody.innerHTML = `
      <div class="rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 p-5">
        <div class="text-xs font-medium text-zinc-500 mb-2">Питання зі співбесіди</div>
        <div class="text-base font-semibold mb-3">${escapeHtml(iv.q)}</div>
        <div id="lessonInterviewAns" class="hidden pt-3 border-t border-zinc-200 dark:border-zinc-800 text-sm text-zinc-600 dark:text-zinc-300 leading-relaxed">${escapeHtml(iv.a)}</div>
      </div>
      <button id="toggleLessonIvBtn" class="px-3.5 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-zinc-700 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition cursor-pointer">
        Показати еталонну відповідь
      </button>
    `;
    document.getElementById("toggleLessonIvBtn").addEventListener("click", () => {
      document.getElementById("lessonInterviewAns").classList.toggle("hidden");
    });
  } else if (state.activeLessonTab === "notes") {
    const currentNote = state.notes[topic.id] || "";
    el.lessonBody.innerHTML = `
      <textarea id="lessonNoteInput" rows="6" placeholder="Запиши сюди свій конспект, посилання або складні моменти..." class="w-full rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-950 p-3 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/15 dark:focus:ring-white/15">${escapeHtml(currentNote)}</textarea>
      <div class="flex justify-end">
        <button id="saveLessonNoteBtn" class="px-4 py-2 rounded-lg text-xs font-medium bg-zinc-900 text-white dark:bg-white dark:text-zinc-900 hover:opacity-90 transition cursor-pointer">
          Зберегти нотатку
        </button>
      </div>
    `;
    document.getElementById("saveLessonNoteBtn").addEventListener("click", async () => {
      const val = document.getElementById("lessonNoteInput").value;
      await saveNote(topic.id, val);
    });
  }
}

/* ---------- Playground (Pyodide in-browser + API fallback) ---------- */
let pyodideInstance = null;
let pyodideLoadingPromise = null;

async function ensurePyodide() {
  if (pyodideInstance) return pyodideInstance;
  if (!pyodideLoadingPromise) {
    pyodideLoadingPromise = (async () => {
      if (!window.loadPyodide) {
        await new Promise((resolve, reject) => {
          const s = document.createElement("script");
          s.src = "https://cdn.jsdelivr.net/pyodide/v0.27.8/full/pyodide.js";
          s.onload = resolve;
          s.onerror = reject;
          document.head.appendChild(s);
        });
      }
      pyodideInstance = await window.loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.8/full/",
      });
      return pyodideInstance;
    })();
  }
  return pyodideLoadingPromise;
}

function openPlayground(initialCode = null) {
  if (initialCode !== null) {
    el.playgroundCode.value = initialCode;
  } else if (!el.playgroundCode.value.trim()) {
    el.playgroundCode.value = "print('Привіт, Python!')\nfor i in range(1, 6):\n    print(f'{i}^2 = {i**2}')";
  }
  showModal(el.playgroundModal);
}

async function runPlaygroundCode() {
  const code = el.playgroundCode.value;
  if (!code.trim()) return;
  el.playgroundOutput.textContent = "Запуск Python у браузері (Pyodide)...";
  try {
    const pyodide = await ensurePyodide();
    const outLines = [];
    pyodide.setStdout({ batched: (msg) => outLines.push(msg) });
    pyodide.setStderr({ batched: (msg) => outLines.push(msg) });
    await pyodide.runPythonAsync(code);
    el.playgroundOutput.textContent = outLines.join("\n") || "(Програма завершилась без виводу)";
  } catch (pyErr) {
    if (String(pyErr).includes("loadPyodide") || String(pyErr).includes("Failed to fetch")) {
      try {
        const res = await api("/api/playground/run", {
          method: "POST",
          body: JSON.stringify({ code }),
        });
        const out = [res.stdout, res.stderr].filter(Boolean).join("\n");
        el.playgroundOutput.textContent = out || "(Програма завершилась без виводу)";
      } catch (err) {
        el.playgroundOutput.textContent = `Помилка: ${err.message}`;
      }
    } else {
      el.playgroundOutput.textContent = String(pyErr);
    }
  }
}

/* ---------- Flashcards ---------- */
function openFlashcards() {
  state.flashcards = [];
  for (const stage of state.stages) {
    for (const topic of stage.topics) {
      if (topic.interview) {
        state.flashcards.push({
          stageNum: stage.number,
          topicTitle: topic.title,
          q: topic.interview.q,
          a: topic.interview.a,
        });
      }
    }
  }
  state.flashcardIndex = 0;
  renderFlashcard();
  showModal(el.flashcardsModal);
}

function renderFlashcard() {
  if (!state.flashcards.length) return;
  const card = state.flashcards[state.flashcardIndex];
  el.flashcardMeta.textContent = `Картка ${state.flashcardIndex + 1} з ${state.flashcards.length}`;
  el.flashcardTopic.textContent = `Етап ${card.stageNum} · ${card.topicTitle}`;
  el.flashcardQ.textContent = card.q;
  el.flashcardA.textContent = card.a;
  el.flashcardA.classList.add("hidden");
}

/* ---------- Progress Actions ---------- */
async function handleToggleTopic(topicId, checked) {
  if (checked) state.completed.add(topicId);
  else state.completed.delete(topicId);
  renderAll();

  if (!state.user) {
    showToast("Позначено локально. Створи акаунт, щоб зберегти прогрес!");
    return;
  }
  try {
    const res = await api(`/api/progress/${topicId}`, {
      method: "PUT",
      body: JSON.stringify({ completed: checked }),
    });
    state.totalXp = res.total_xp;
    state.streakDays = res.streak_days;
    computeStats();
  } catch (err) {
    showToast(err.message);
  }
}

async function saveNote(topicId, notes) {
  state.notes[topicId] = notes;
  if (!state.user) {
    openAuthModal("register");
    showToast("Створи акаунт або увійди, щоб зберігати нотатки.");
    return;
  }
  try {
    const res = await api(`/api/progress/${topicId}`, {
      method: "PUT",
      body: JSON.stringify({ notes }),
    });
    state.totalXp = res.total_xp;
    state.streakDays = res.streak_days;
    computeStats();
    renderStages();
    showToast("Нотатку збережено");
  } catch (err) {
    showToast(err.message);
  }
}

async function loadUserProgress() {
  if (!state.user) {
    state.completed = new Set();
    state.notes = {};
    state.quizResults = {};
    state.totalXp = 0;
    state.streakDays = 0;
    return;
  }
  const data = await api("/api/progress");
  state.completed = new Set(data.completed || []);
  state.notes = data.notes || {};
  state.quizResults = data.quiz_results || {};
  state.totalXp = data.total_xp || 0;
  state.streakDays = data.streak_days || 0;
}

async function handleAuthSubmit(e) {
  e.preventDefault();
  el.authError.classList.add("hidden");
  const username = el.usernameInput.value.trim();
  const password = el.passwordInput.value;
  const displayName = el.displayNameInput.value.trim();
  const guestCompleted = Array.from(state.completed);

  try {
    const endpoint = state.authMode === "register" ? "/api/auth/register" : "/api/auth/login";
    const body =
      state.authMode === "register"
        ? { username, display_name: displayName, password }
        : { username, password };

    const data = await api(endpoint, { method: "POST", body: JSON.stringify(body) });
    state.user = data.user;

    if (state.authMode === "register" && guestCompleted.length > 0) {
      await api("/api/progress/bulk", {
        method: "POST",
        body: JSON.stringify({ completed_ids: guestCompleted }),
      });
    }

    await loadUserProgress();
    closeAuthModal();
    renderAll();
    showToast(
      state.authMode === "register"
        ? "Акаунт створено! Прогрес тепер зберігається."
        : `Вітаємо з поверненням, ${state.user.display_name}!`
    );
  } catch (err) {
    el.authError.textContent = err.message;
    el.authError.classList.remove("hidden");
  }
}

async function handleLogout() {
  await api("/api/auth/logout", { method: "POST" });
  state.user = null;
  await loadUserProgress();
  renderAll();
  showToast("Ви вийшли з акаунту");
}

function bindEvents() {
  el.themeToggleBtn.addEventListener("click", toggleTheme);
  el.bannerRegisterBtn.addEventListener("click", () => openAuthModal("register"));
  el.bannerLoginBtn.addEventListener("click", () => openAuthModal("login"));
  el.closeModalBtn.addEventListener("click", closeAuthModal);
  el.authModal.addEventListener("click", (e) => { if (e.target === el.authModal) closeAuthModal(); });
  el.tabLogin.addEventListener("click", () => openAuthModal("login"));
  el.tabRegister.addEventListener("click", () => openAuthModal("register"));
  el.authForm.addEventListener("submit", handleAuthSubmit);

  el.closeLessonBtn.addEventListener("click", closeLessonModal);
  el.lessonDoneCloseBtn.addEventListener("click", closeLessonModal);
  el.lessonModal.addEventListener("click", (e) => { if (e.target === el.lessonModal) closeLessonModal(); });
  el.lessonTabs.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-ltab]");
    if (!btn) return;
    state.activeLessonTab = btn.dataset.ltab;
    renderLessonTab();
  });
  el.lessonCompleteCheckbox.addEventListener("change", (e) => {
    if (state.activeLessonId) handleToggleTopic(state.activeLessonId, e.target.checked);
  });

  el.openPlaygroundBtn.addEventListener("click", () => openPlayground());
  el.closePlaygroundBtn.addEventListener("click", () => hideModal(el.playgroundModal));
  el.playgroundModal.addEventListener("click", (e) => { if (e.target === el.playgroundModal) hideModal(el.playgroundModal); });
  el.runCodeBtn.addEventListener("click", runPlaygroundCode);
  el.clearOutputBtn.addEventListener("click", () => { el.playgroundOutput.textContent = ""; });
  el.playgroundCode.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.key === "Enter") {
      e.preventDefault();
      runPlaygroundCode();
    } else if (e.key === "Tab") {
      e.preventDefault();
      const start = el.playgroundCode.selectionStart;
      const end = el.playgroundCode.selectionEnd;
      el.playgroundCode.value =
        el.playgroundCode.value.substring(0, start) + "    " + el.playgroundCode.value.substring(end);
      el.playgroundCode.selectionStart = el.playgroundCode.selectionEnd = start + 4;
    }
  });

  el.openFlashcardsBtn.addEventListener("click", openFlashcards);
  el.closeFlashcardsBtn.addEventListener("click", () => hideModal(el.flashcardsModal));
  el.flashcardsModal.addEventListener("click", (e) => { if (e.target === el.flashcardsModal) hideModal(el.flashcardsModal); });
  el.flashcardToggleAnswerBtn.addEventListener("click", () => el.flashcardA.classList.toggle("hidden"));
  el.flashcardNextBtn.addEventListener("click", () => {
    state.flashcardIndex = (state.flashcardIndex + 1) % state.flashcards.length;
    renderFlashcard();
  });

  el.pomodoroToggleBtn.addEventListener("click", togglePomodoro);
  el.pomodoroResetBtn.addEventListener("click", resetPomodoro);

  el.searchInput.addEventListener("input", (e) => {
    state.search = e.target.value;
    renderStages();
  });
  el.filterPills.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-filter]");
    if (!btn) return;
    state.filter = btn.dataset.filter;
    const activeCls = "px-3 py-1 rounded-md text-xs font-medium bg-white dark:bg-zinc-950 text-zinc-900 dark:text-white shadow-2xs transition cursor-pointer";
    const idleCls = "px-3 py-1 rounded-md text-xs font-medium text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-white transition cursor-pointer";
    for (const p of el.filterPills.querySelectorAll("button[data-filter]")) {
      p.className = p === btn ? activeCls : idleCls;
    }
    renderStages();
  });
  el.stagesContainer.addEventListener("click", (e) => {
    const stageHeader = e.target.closest('[data-action="toggle-stage"]');
    if (stageHeader) {
      const sid = stageHeader.dataset.stageId;
      if (state.collapsedStages.has(sid)) state.collapsedStages.delete(sid);
      else state.collapsedStages.add(sid);
      renderStages();
      return;
    }
    const openBtn = e.target.closest('[data-action="open-lesson"]');
    if (openBtn) {
      openLessonModal(openBtn.dataset.topicId, "theory");
      return;
    }
    const quizBtn = e.target.closest('[data-action="open-lesson-quiz"]');
    if (quizBtn) {
      openLessonModal(quizBtn.dataset.topicId, "quiz");
    }
  });
  el.stagesContainer.addEventListener("change", (e) => {
    const cb = e.target.closest('[data-action="toggle"]');
    if (!cb) return;
    handleToggleTopic(cb.dataset.topicId, cb.checked);
  });
}

async function init() {
  applyTheme(localStorage.getItem("pypath_theme") || "light");
  bindEvents();
  renderPomodoro();
  const [currData, meData] = await Promise.all([api("/api/curriculum"), api("/api/auth/me")]);
  state.stages = currData.stages || [];
  for (const stage of state.stages) {
    for (const topic of stage.topics) {
      state.topicMap.set(topic.id, { stage, topic });
    }
  }
  state.user = meData.user || null;
  if (state.user) await loadUserProgress();
  renderAll();
}

init().catch((err) => {
  console.error(err);
  showToast("Не вдалося завантажити дані програми");
});
