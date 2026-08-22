# curo — Build Guide

## Before You Write a Single Line of Code

Read CLAUDE.md, FRONTEND_SPEC.md and APP_BLUEPRINT.md in full. Every design decision is in CLAUDE.md. Every data structure, api call pattern and model rule is in APP_BLUEPRINT.md. Every visual and interaction value is in FRONTEND_SPEC.md. This guide tells you the order to build things. The other three files tell you what to build and how.

The rules that matter most, repeated here because they have ended projects:

1. No mock data. No demo data. No fabricated data. Every number on screen is live api data, api history, or a model output, and every one carries its provenance tag.
2. Trial credits are finite. Cache every api response in the sqlite table and never fetch the same hour twice.
3. The demo video is silent. The app's labels are the narration. Keep them short, plain and legible from a paused frame.

---

## Prerequisites

```bash
node --version   # 18 or higher
npm --version    # 9 or higher
python3 --version # 3.11 or higher
git --version
```

The FortyGuard api key lives in the backend environment only. Request trial keys at registration before anything else.

---

## Repository Setup

```bash
mkdir curo && cd curo
git init
mkdir -p backend/curo
mkdir -p frontend/src/{components/{layout,console,overlays,ui},hooks,lib,styles}
```

Frontend scaffold:

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
npm install tailwindcss @tailwindcss/vite
npm install motion leaflet react-leaflet
npm install -D @types/leaflet
```

Backend scaffold:

```bash
cd ../backend
python3 -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn httpx
```

---

## Tailwind v4 Warning, Read Before Styling

FRONTEND_SKILL.md Step 12 documents a silent cascade bug in Tailwind v4. A reset rule written outside any css layer overrides every spacing utility in the project.

```css
/* This is the bug. Never write this outside a layer. */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
```

If spacing classes stop working while the build succeeds, search globals.css for this pattern first. Tailwind v4 ships its own reset inside @layer base. Add nothing outside a layer.

---

## Phase 0 — Verification Script, Build This First

`backend/verify.py`. Hits the api for a downtown Phoenix geohash, latitude 33.4484, longitude minus 112.0740, and logs three things:

1. Current temperature
2. The 12 hour forecast
3. A slice of history from 2021 or later

Read the official FortyGuard api documentation before writing the first call. Do not invent endpoints. Confirm every parameter and response field against the docs.

If all three return data, proceed. If any fails, stop and report the exact error before building anything else. This is the single risk point of the entire project and it costs one hour instead of one day if it fails early.

---

## Phase 1 — Backend

### Step 1.1: Cache layer

`backend/curo/cache.py`. SQLite table per APP_BLUEPRINT.md. Every api call checks the cache before the network. The key is the hashed query parameters. Store the raw json plus the fetched timestamp.

```python
"""Cache layer for FortyGuard api responses.

Every response is stored once and reused forever during the hackathon.
Trial credits are finite, this table is the safety net.
"""
```

### Step 1.2: FortyGuard client

`backend/curo/fortyguard.py`. Async httpx client, key from environment, every call returns the payload with a `source` field attached. The three sources are `live`, `forecast`, `history`. On any network failure, fall back to the newest cached payload and mark it `cached`.

### Step 1.3: ACI 305 model

`backend/curo/model.py`. Pure functions, no ml, no dependencies.

```python
PLACEMENT_LIMIT_F = 95  # aci 305r-20 hot weather placement limit
AMBER_BAND_F = 5        # amber when within this band of the limit
```

- `classify(temp_f: float, mass: bool, thickness: float) -> str` returns `green`, `amber` or `red`
- `margin(temp_f: float) -> float` returns the signed distance from the limit
- `percentiles(history: list[float], date: datetime) -> tuple[float, float]` returns the p25 and p75 climatology band for that site and calendar date
- `window(forecast: list[float]) -> dict` returns the full 12 hour model output with every rule that fired

Mass concrete tightens the limit by 10 degrees, slab thickness over 12 inches widens the amber band to 7 degrees. Both are stated on screen as model rules.

### Step 1.4: Routes

Implement the endpoint list from APP_BLUEPRINT.md. Every response includes `source`. No auth, no rate limiting beyond the cache. Run with:

```bash
uvicorn curo.main:app --reload --port 8000
```

---

## Phase 2 — Frontend Foundation

### Step 2.1: Theme

`frontend/src/styles/globals.css`. Copy the @theme block, the keyframes, the glass-light class, the grain pattern, the scrollbar hiding and the reduced motion overrides from FRONTEND_SPEC.md verbatim. Add the Tailwind v4 plugin to vite.config.ts:

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

### Step 2.2: index.html

Set the title to `curo`, add the Google Fonts link, the Material Icons link and the favicon comment slot, all exactly as the spec shows.

### Step 2.3: Shared pieces

`src/components/ui/GrainOverlay.tsx`, fixed, z-500, 2 percent opacity, no animation.

`src/components/ui/FadeBlur.tsx`, a wrapper with the standard blur-in entrance:

```
initial={{ opacity: 0, filter: 'blur(8px)', y: 16 }}
animate={{ opacity: 1, filter: 'blur(0px)', y: 0 }}
transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1], delay }}
```

Takes `delay` as a prop. Every entrance in the app goes through this component or matches its values exactly.

`src/lib/api.ts`, fetch wrappers with the source field passthrough.

### Step 2.4: Build order

1. `TopBar.tsx`, dual pill split, sticky, with the export button wiring to a placeholder
2. `MapCell.tsx`, basemap, then the grid polygons, then the marker, callout, legend, timestamp chip
3. `DecisionRail.tsx`, the four modules, static data first, then live wiring
4. `BreachAlert.tsx`, the overlay with the two way alert, green and red variants
5. `ExportDrawer.tsx`, with real csv and ics downloads from the backend
6. Loading skeletons, error banner, empty state

Wire the data last for each component, never first. The visuals come up fast, then each number swaps from static placeholder to live data, and the swap is where you test the provenance tags.

---

## Phase 3 — Data Wiring Order

1. Current grid into the map, confirm the cells and timestamps
2. Forecast into the hour strip, confirm the current hour ring
3. History percentiles into the calendar, confirm the climatology labels
4. Model output into the status module, confirm every rule that fired
5. Breach alert on the real hottest forecast hour
6. Counters with editable assumptions, count up on load

Phoenix in late August will produce amber and red hours on real data. Use them. Do not invent a breach.

---

## Phase 4 — Quality Audit

Run through this list before recording anything.

- [ ] Verification script logged current, forecast and history for Phoenix
- [ ] Map renders real api data with timestamps visible
- [ ] Every number has a provenance tag, live, forecast, history, model, assumption or cached
- [ ] ACI model classifies any hour green, amber or red with the rule shown
- [ ] Calendar shows forecast and climatology clearly labelled, confidence visible
- [ ] Breach alert fires on real data and its green counterpart works
- [ ] csv and ics downloads open in standard tools
- [ ] Counters count up on load and the assumption labels are visible
- [ ] App runs fully from cache if the api is unreachable
- [ ] No hardcoded hex values in components, no emojis, no third party icon libraries
- [ ] No em dashes anywhere, British English throughout
- [ ] All entrances blur in, no bare fades
- [ ] Every interactive element has a visible focus state
- [ ] 1280x800 safe zone check, everything visible without rail scroll
- [ ] reduced motion collapses everything to instant state
- [ ] Logo and favicon are comment slots, not placeholders

---

## Phase 5 — Recording and Submission

Follow `RECORDING_GUIDE.md` for the recording. Then:

- [ ] Public repo, readme explains the physics, assumptions and data sources
- [ ] Demo video uploaded and linked in the submission
- [ ] Submission form requirements checked before recording, video length first
- [ ] Submit before August 30 with a full day of buffer

The readme is judged. Spend the last hour on it, not on a new feature.
