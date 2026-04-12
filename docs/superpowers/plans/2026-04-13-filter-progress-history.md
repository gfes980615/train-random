# Filter, No-Repeat Draw & Persistent History — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add tag-based station filtering, no-repeat drawing with conquer-all progress tracking, and localStorage-persisted history to the Taiwan Railway lottery app.

**Architecture:** All changes are in `generate_app.py`, which generates a single-file HTML app. The file contains a Python f-string template with embedded CSS, HTML, and JS. Python braces must be doubled (`{{`/`}}`) inside the template. New features add CSS styles, HTML elements, and JS functions into the existing template.

**Tech Stack:** Python 3 (generator), vanilla JS, CSS, localStorage API, Leaflet.js (existing)

**Important f-string note:** All JS/CSS code inside the `html = f"""..."""` template in `generate_app.py` must use `{{` and `}}` for literal braces. Single `{` is only for Python variable interpolation like `{len(candidates)}` or `{data_json}`.

---

### Task 1: Add CSS for filter tags and progress bar

**Files:**
- Modify: `generate_app.py:886-893` (insert new CSS before `/* history */` comment)
- Modify: `generate_app.py:1020-1026` (add mobile responsive rules)

- [ ] **Step 1: Add filter tag and progress bar CSS after the `.count-row select` rule (line 885) and before the `/* history */` comment (line 887)**

Find this in `generate_app.py`:
```python
.count-row select{{background:#1e293b;border:1px solid #334155;color:#e2e8f0;
  border-radius:8px;padding:6px 14px;font-size:.95rem}}

/* history */
```

Replace with:
```python
.count-row select{{background:#1e293b;border:1px solid #334155;color:#e2e8f0;
  border-radius:8px;padding:6px 14px;font-size:.95rem}}

/* filter tags */
.filter-group{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}
.filter-group-label{{width:100%;text-align:center;font-size:.7rem;color:#475569;
  text-transform:uppercase;letter-spacing:1px;margin-bottom:2px}}
.filter-tag{{padding:4px 12px;border-radius:8px;font-size:.75rem;cursor:pointer;
  border:1px solid #334155;background:#1e293b;color:#64748b;
  transition:all .2s;user-select:none}}
.filter-tag.active{{background:linear-gradient(135deg,#6366f1,#818cf8);
  color:#fff;border-color:#818cf8;box-shadow:0 2px 8px rgba(99,102,241,.3)}}
.filter-tag:hover{{border-color:#6366f1}}

/* progress bar */
.progress-wrap{{width:100%;padding:0 24px;margin-top:2px}}
.progress-bar{{width:100%;height:4px;background:#1e293b;border-radius:2px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:2px;transition:width .5s ease;
  background:linear-gradient(90deg,#6366f1,#38bdf8)}}
.progress-label{{display:flex;justify-content:center;align-items:center;gap:8px;
  font-size:.72rem;color:#64748b;margin-top:4px}}
.progress-label em{{color:#38bdf8;font-style:normal;font-weight:600}}
.btn-reset{{background:none;border:1px solid #334155;color:#64748b;
  padding:2px 8px;border-radius:4px;font-size:.65rem;cursor:pointer;transition:all .2s}}
.btn-reset:hover{{border-color:#f87171;color:#f87171}}

/* conquer overlay */
.conquer-overlay{{position:fixed;top:0;left:0;width:100%;height:100%;
  z-index:10000;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:rgba(15,23,42,.9);opacity:0;transition:opacity .5s;pointer-events:none}}
.conquer-overlay.active{{opacity:1;pointer-events:auto}}
.conquer-title{{font-size:3rem;font-weight:900;
  background:linear-gradient(135deg,#fbbf24,#f472b6,#818cf8);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  text-shadow:0 0 80px rgba(251,191,36,.4)}}
.conquer-sub{{font-size:1.2rem;color:#94a3b8;margin-top:12px}}

/* history */
```

- [ ] **Step 2: Add mobile responsive CSS for filter tags and progress bar**

Find this in `generate_app.py`:
```python
  .history{{padding:0 16px 12px;max-height:70px}}
  .history-tag{{font-size:.7rem;padding:2px 8px}}
```

Replace with:
```python
  .filter-tag{{padding:3px 8px;font-size:.65rem}}
  .filter-group-label{{font-size:.6rem}}
  .progress-wrap{{padding:0 16px}}
  .progress-label{{font-size:.65rem}}

  .history{{padding:0 16px 12px;max-height:70px}}
  .history-tag{{font-size:.7rem;padding:2px 8px}}
```

- [ ] **Step 3: Run generator to verify no syntax errors**

Run: `cd /Users/fred_chen/train-random && python3 generate_app.py`
Expected: "已產出" message with no errors.

- [ ] **Step 4: Commit**

```bash
git add generate_app.py
git commit -m "style: add CSS for filter tags, progress bar, and conquer overlay"
```

---

### Task 2: Add HTML for filter tags, progress bar, and conquer overlay

**Files:**
- Modify: `generate_app.py:1048-1052` (stats bar — add progress counter)
- Modify: `generate_app.py:1069-1080` (controls section — add filter tags)
- Modify: `generate_app.py:1082-1085` (history section — always visible, placeholder)
- Modify: `generate_app.py:1037-1039` (add conquer overlay element)

- [ ] **Step 1: Add conquer overlay div after the screen flash div**

Find this in `generate_app.py`:
```python
<!-- screen flash -->
<div class="screen-flash" id="screenFlash"></div>
```

Replace with:
```python
<!-- screen flash -->
<div class="screen-flash" id="screenFlash"></div>
<!-- conquer overlay -->
<div class="conquer-overlay" id="conquerOverlay">
  <div class="conquer-title">&#127942; 恭喜全制霸！</div>
  <div class="conquer-sub">你已經抽過所有 138 個秘境小站！</div>
</div>
```

- [ ] **Step 2: Update stats bar to include progress counter**

Find this in `generate_app.py`:
```python
    <div class="stats">
      <span>全部 <em>{len(stations)}</em> 站</span>
      <span>候選 <em>{len(candidates)}</em> 站</span>
      <span>已排除自強號 <em>{len(stations)-len(candidates)}</em> 站</span>
    </div>
```

Replace with:
```python
    <div class="stats">
      <span>全部 <em>{len(stations)}</em> 站</span>
      <span>候選 <em id="statCandidateCount">{len(candidates)}</em> 站</span>
      <span>制霸 <em id="statProgress">0</em>/{len(candidates)}</span>
    </div>
    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
      <div class="progress-label">
        <span>已抽 <em id="progressText">0</em>/{len(candidates)} 站</span>
        <button class="btn-reset" id="btnReset" onclick="resetProgress()">重置</button>
      </div>
    </div>
```

- [ ] **Step 3: Add filter tag rows above draw count inside the controls section**

Find this in `generate_app.py`:
```python
    <div class="controls">
      <div class="count-row">
        <label for="drawCount">抽籤數量</label>
```

Replace with:
```python
    <div class="controls">
      <div class="filter-group" id="filterRoute">
        <span class="filter-group-label">路線</span>
      </div>
      <div class="filter-group" id="filterRegion">
        <span class="filter-group-label">區域</span>
      </div>
      <div class="count-row">
        <label for="drawCount">抽籤數量</label>
```

- [ ] **Step 4: Change history section to always visible with placeholder**

Find this in `generate_app.py`:
```python
    <div class="history" id="historyWrap" style="display:none">
      <h3>抽籤記錄</h3>
      <div class="history-list" id="historyList"></div>
    </div>
```

Replace with:
```python
    <div class="history" id="historyWrap">
      <h3>抽籤記錄</h3>
      <div class="history-list" id="historyList">
        <span class="history-tag" style="color:#475569">尚無記錄</span>
      </div>
    </div>
```

- [ ] **Step 5: Run generator to verify no syntax errors**

Run: `cd /Users/fred_chen/train-random && python3 generate_app.py`
Expected: "已產出" message with no errors.

- [ ] **Step 6: Commit**

```bash
git add generate_app.py
git commit -m "feat: add HTML for filter tags, progress bar, conquer overlay, and persistent history"
```

---

### Task 3: Add JS — Route/region mapping and filter logic

**Files:**
- Modify: `generate_app.py:1097-1100` (after data declarations, add filter constants and state)

- [ ] **Step 1: Add route/region constants and filter state after the `stationInfo` declaration**

Find this in `generate_app.py`:
```python
const stationInfo = {info_json};
```

Replace with:
```python
const stationInfo = {info_json};

// ============================================================
// Filter & Progress State
// ============================================================
const TOTAL_CANDIDATES = candidates.length;

const ROUTE_MAP = {{
  '縱貫線': ['縱貫線'],
  '海岸線': ['海岸線'],
  '山線': ['臺中線(山線)'],
  '宜蘭線': ['宜蘭線'],
  '北迴線': ['北迴線'],
  '南迴線': ['南迴線'],
  '臺東線': ['臺東線'],
  '屏東線': ['屏東線'],
  '支線': ['平溪線','內灣線','集集線','深澳線','沙崙線','六家線','花蓮臨港線'],
}};
const REGION_MAP = {{
  '北部': ['基隆市','新北市','臺北市','桃園市','新竹縣','新竹市'],
  '中部': ['苗栗縣','臺中市','彰化縣','南投縣','雲林縣'],
  '南部': ['嘉義縣','嘉義市','臺南市','高雄市','屏東縣'],
  '東部': ['宜蘭縣','花蓮縣','臺東縣'],
}};

const activeRoutes = new Set(Object.keys(ROUTE_MAP));
const activeRegions = new Set(Object.keys(REGION_MAP));

// localStorage persistence
let drawnStations = new Set(JSON.parse(localStorage.getItem('train-random-drawn') || '[]'));
let historyData = JSON.parse(localStorage.getItem('train-random-history') || '[]');

function saveDrawn() {{
  localStorage.setItem('train-random-drawn', JSON.stringify([...drawnStations]));
}}
function saveHistory() {{
  localStorage.setItem('train-random-history', JSON.stringify(historyData));
}}

function getFilteredCandidates() {{
  const allowedLines = new Set();
  activeRoutes.forEach(r => ROUTE_MAP[r].forEach(l => allowedLines.add(l)));
  const allowedCities = new Set();
  activeRegions.forEach(r => REGION_MAP[r].forEach(c => allowedCities.add(c)));
  return candidates.filter(s =>
    allowedLines.has(s.line) && allowedCities.has(s.city) && !drawnStations.has(s.name)
  );
}}

function updateFilteredCount() {{
  const pool = getFilteredCandidates();
  document.getElementById('statCandidateCount').textContent = pool.length;
  const btn = document.getElementById('btnDraw');
  if (pool.length === 0 && !isSpinning) {{
    btn.disabled = true;
    btn.textContent = drawnStations.size >= TOTAL_CANDIDATES
      ? '已全制霸！' : '無可用車站';
  }} else if (!isSpinning) {{
    btn.disabled = false;
    btn.textContent = '開始抽籤';
  }}
}}

function updateProgress() {{
  const count = drawnStations.size;
  const pct = (count / TOTAL_CANDIDATES * 100).toFixed(1);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressText').textContent = count;
  document.getElementById('statProgress').textContent = count;
}}
```

- [ ] **Step 2: Run generator to verify no syntax errors**

Run: `cd /Users/fred_chen/train-random && python3 generate_app.py`
Expected: "已產出" message with no errors.

- [ ] **Step 3: Commit**

```bash
git add generate_app.py
git commit -m "feat: add JS filter/region mapping, localStorage persistence, and pool filtering"
```

---

### Task 4: Add JS — Filter tag rendering and toggle logic

**Files:**
- Modify: `generate_app.py` (at the bottom, before `buildTrack();` init line)

- [ ] **Step 1: Add filter tag rendering and event handling before `buildTrack();`**

Find this in `generate_app.py`:
```python
// init
buildTrack();
```

Replace with:
```python
// ============================================================
// Filter Tags — render & toggle
// ============================================================
function renderFilterTags() {{
  const routeWrap = document.getElementById('filterRoute');
  const regionWrap = document.getElementById('filterRegion');

  // keep the label, clear tags
  routeWrap.innerHTML = '<span class="filter-group-label">路線</span>';
  regionWrap.innerHTML = '<span class="filter-group-label">區域</span>';

  Object.keys(ROUTE_MAP).forEach(name => {{
    const tag = document.createElement('span');
    tag.className = 'filter-tag' + (activeRoutes.has(name) ? ' active' : '');
    tag.textContent = name;
    tag.onclick = () => {{
      if (activeRoutes.has(name)) activeRoutes.delete(name);
      else activeRoutes.add(name);
      tag.classList.toggle('active');
      updateFilteredCount();
    }};
    routeWrap.appendChild(tag);
  }});

  Object.keys(REGION_MAP).forEach(name => {{
    const tag = document.createElement('span');
    tag.className = 'filter-tag' + (activeRegions.has(name) ? ' active' : '');
    tag.textContent = name;
    tag.onclick = () => {{
      if (activeRegions.has(name)) activeRegions.delete(name);
      else activeRegions.add(name);
      tag.classList.toggle('active');
      updateFilteredCount();
    }};
    regionWrap.appendChild(tag);
  }});
}}

// ============================================================
// Reset progress
// ============================================================
function resetProgress() {{
  if (!confirm('確定要重置制霸進度嗎？所有抽籤記錄將被清除')) return;
  drawnStations.clear();
  historyData = [];
  saveDrawn();
  saveHistory();
  updateProgress();
  updateFilteredCount();
  renderHistory();
}}

// ============================================================
// History — render with timestamps
// ============================================================
function renderHistory() {{
  const list = document.getElementById('historyList');
  if (historyData.length === 0) {{
    list.innerHTML = '<span class="history-tag" style="color:#475569">尚無記錄</span>';
    return;
  }}
  list.innerHTML = historyData.slice(0, 50).map(h => {{
    const d = new Date(h.time);
    const label = (d.getMonth() + 1) + '/' + d.getDate() + ' ' + h.name;
    return '<span class="history-tag">' + label + '</span>';
  }}).join('');
}}

// ============================================================
// Conquer-all celebration
// ============================================================
function checkConquer() {{
  if (drawnStations.size >= TOTAL_CANDIDATES) {{
    const overlay = document.getElementById('conquerOverlay');
    overlay.classList.add('active');
    spawnFullScreenConfetti();
    spawnFullScreenConfetti();
    setTimeout(() => overlay.classList.remove('active'), 4000);
  }}
}}

// ============================================================
// Init
// ============================================================
renderFilterTags();
renderHistory();
updateProgress();
updateFilteredCount();
buildTrack();
```

- [ ] **Step 2: Run generator to verify no syntax errors**

Run: `cd /Users/fred_chen/train-random && python3 generate_app.py`
Expected: "已產出" message with no errors.

- [ ] **Step 3: Commit**

```bash
git add generate_app.py
git commit -m "feat: add filter tag rendering, reset, history display, and conquer celebration"
```

---

### Task 5: Modify startDraw to use filtered pool, track drawn stations, and persist history

**Files:**
- Modify: `generate_app.py` — the `startDraw()` function and `buildTrack()` function
- Modify: `generate_app.py` — the `updateHistory()` function (replace entirely)

- [ ] **Step 1: Update `buildTrack()` to use filtered candidates**

Find this in `generate_app.py`:
```python
function buildTrack() {{
  slotTrack.innerHTML = '';
  const pool = [];
  for (let i = 0; i < 80; i++) {{
    pool.push(candidates[Math.floor(Math.random() * candidates.length)]);
  }}
```

Replace with:
```python
function buildTrack(filteredPool) {{
  slotTrack.innerHTML = '';
  const source = filteredPool || candidates;
  const pool = [];
  for (let i = 0; i < 80; i++) {{
    pool.push(source[Math.floor(Math.random() * source.length)]);
  }}
```

- [ ] **Step 2: Update `startDraw()` to use filtered pool, save drawn stations, and persist history**

Find this in `generate_app.py`:
```python
async function startDraw() {{
  if (isSpinning) return;
  isSpinning = true;
  btnDraw.disabled = true;
  ensureAudio();

  const count = parseInt(document.getElementById('drawCount').value);
  const shuffled = [...candidates].sort(() => Math.random() - 0.5);
  const winners = shuffled.slice(0, count);
```

Replace with:
```python
async function startDraw() {{
  if (isSpinning) return;
  const pool = getFilteredCandidates();
  if (pool.length === 0) return;

  isSpinning = true;
  btnDraw.disabled = true;
  ensureAudio();

  const count = Math.min(parseInt(document.getElementById('drawCount').value), pool.length);
  const shuffled = [...pool].sort(() => Math.random() - 0.5);
  const winners = shuffled.slice(0, count);
```

- [ ] **Step 3: Update the `buildTrack` call inside `animateOne` to pass filtered pool**

Find this in `generate_app.py` (inside `animateOne`):
```python
    const pool = buildTrack();
```

Replace with:
```python
    const filteredPool = getFilteredCandidates();
    const displayPool = filteredPool.length > 0 ? filteredPool : candidates;
    const pool = buildTrack(displayPool);
```

- [ ] **Step 4: Update the history/tracking code after `updateHistory()` call in the landed section**

Find this in `generate_app.py`:
```python
        // add to history
        history.unshift(winner);
        updateHistory();
```

Replace with:
```python
        // add to history & track drawn
        drawnStations.add(winner.name);
        saveDrawn();
        historyData.unshift({{ name: winner.name, city: winner.city, line: winner.line, time: new Date().toISOString() }});
        saveHistory();
        updateProgress();
        renderHistory();
```

- [ ] **Step 5: Add conquer check and filter update after the "all done" section**

Find this in `generate_app.py`:
```python
          isSpinning = false;
          btnDraw.disabled = false;
        }}
```

Replace with:
```python
          isSpinning = false;
          btnDraw.disabled = false;
          updateFilteredCount();
          checkConquer();
        }}
```

- [ ] **Step 6: Remove the old `let history = [];` declaration and `updateHistory` function**

Find this in `generate_app.py`:
```python
let isSpinning = false;
let history = [];
```

Replace with:
```python
let isSpinning = false;
```

Find this in `generate_app.py`:
```python
function updateHistory() {{
  const wrap = document.getElementById('historyWrap');
  const list = document.getElementById('historyList');
  wrap.style.display = 'block';
  list.innerHTML = history.slice(0, 20).map(h =>
    '<span class="history-tag">' + h.name + '</span>'
  ).join('');
}}
```

Replace with (remove entirely — functionality moved to `renderHistory`):
```python
```

(Delete the entire `updateHistory` function — it is replaced by `renderHistory` added in Task 4.)

- [ ] **Step 7: Run generator and verify output**

Run: `cd /Users/fred_chen/train-random && python3 generate_app.py`
Expected: "已產出" message with no errors.

- [ ] **Step 8: Commit**

```bash
git add generate_app.py
git commit -m "feat: integrate filtered draw pool, no-repeat tracking, persistent history, and conquer check"
```

---

### Task 6: Generate final output, copy to index.html, and push

**Files:**
- Regenerate: `draw_station.html`
- Copy: `index.html`

- [ ] **Step 1: Regenerate and copy**

Run:
```bash
cd /Users/fred_chen/train-random
python3 generate_app.py
cp draw_station.html index.html
```

Expected: "已產出" with 241 stations, 138 candidates.

- [ ] **Step 2: Verify the generated HTML contains all new elements**

Run:
```bash
grep -c 'filter-tag\|progress-fill\|conquer-overlay\|train-random-drawn\|renderHistory\|getFilteredCandidates' /Users/fred_chen/train-random/index.html
```

Expected: At least 6 matches (one per feature keyword).

- [ ] **Step 3: Commit and push**

```bash
git add generate_app.py draw_station.html index.html
git commit -m "feat: 新增篩選標籤、不重複抽籤制霸進度、持久化歷史記錄

- 路線/區域快速標籤篩選（9 路線 + 4 區域）
- 不重複抽籤，抽過自動排除
- 制霸進度條 + 全制霸慶祝動畫
- localStorage 持久化抽籤記錄（含時間戳）
- 重置進度功能"
git push
```
