# curo — App Blueprint

## Product Summary

curo is a pour window planner for concrete construction. It joins FortyGuard hyperlocal temperature data with the ACI 305 hot weather rules and tells a contractor which hours and days are safe to pour concrete, which are risky, and when a scheduled pour is about to breach its temperature window. It ends in a machine readable schedule export, not just a dashboard.

Built for FortyGuard Hackathon'26, deadline August 30 2026. The temperature api is the entire intelligence layer. Remove it and there is no product, only a calendar.

The physics is the differentiator. Every heat hackathon protects workers, almost nobody protects the material. A bad pour costs six figures in rework, and cement production is one of the largest industrial sources of global co2, so every avoided re-pour is avoided emissions. The demo turns that into two counters the judges watch tick.

---

## One Line Pitch

Know the hour a pour will fail, before the concrete arrives.

---

## Market Context

**Who this is for:**

1. General contractors and concrete subcontractors scheduling pours across active sites, who currently decide pour days by gut and a generic weather app
2. Readymix suppliers whose trucks get rejected at the site when the placement window blows, burning a load and a delivery slot
3. Cities and engineering firms running capital works programmes, who carry the rework cost of every failed pour downstream

**What they currently use:** the phone weather app, a written copy of ACI 305 pinned to the site trailer wall, and experience. None of these are location specific, hour specific, or machine readable.

**Why they switch:** curo answers the one question that costs money, is this specific hour at this specific slab safe, and it answers it in the tools they already run. The export drops into the scheduler. The alert fires before the truck leaves.

---

## MVP Feature Set

### Feature 1: Site verification against the api

**User story:** as a builder I want proof that the fortyguard api returns current, forecast and historical data for my demo city before anything else is built.

**How it works:** a script hits the api for a downtown Phoenix geohash and logs current temperature, the 12 hour forecast, and a slice of history from 2021 or later.

**Acceptance criteria:** all three return data. If any fails, the build stops and reports the exact error.

**Complexity:** low

---

### Feature 2: Heat map console

**User story:** as a contractor I want to see hyperlocal temperature around my sites so that I can pick the right pour location.

**How it works:** Leaflet renders the geohash grid over a light basemap, cells coloured on a six band heat ramp, with a callout showing the selected site's temperature, coordinates and data source.

**Acceptance criteria:** grid renders from live api data, timestamps visible, every cell labelled with its provenance.

**Complexity:** medium

---

### Feature 3: The ACI 305 curing model

**User story:** as a contractor I want the hot weather rules computed for me so that I never misread a threshold at 5am.

**How it works:** for the selected site and hour the model classifies the pour as green, amber or red. The placement limit is 95 degrees fahrenheit per ACI 305R-20. Amber triggers within 5 degrees of the limit. The model shows which rules fired and why.

**Acceptance criteria:** any hour can be classified, the margin is displayed, the rule source is named on screen.

**Complexity:** low

---

### Feature 4: Two week pour calendar

**User story:** as a contractor I want a two week window with confidence bands so that I can lock the crew and the pump in advance.

**How it works:** the next 12 hours come from the live api forecast, labelled forecast. The remaining days come from api history reduced to climatological percentiles, labelled climatology. Confidence shrinks as the horizon extends, and the label says so. This respects the faq limits exactly and uses all three api data products at once.

**Acceptance criteria:** forecast hours and climatology days are visually distinct, every day carries a status band and a confidence figure.

**Complexity:** medium

---

### Feature 5: Breach alert

**User story:** as a contractor I want to be interrupted the moment a scheduled pour is about to breach its window.

**How it works:** the console checks the latest forecast against the model every hour. A breach fires a full alert with the time, the margin and a reschedule action. A cancelled day turning safe again fires the green counterpart.

**Acceptance criteria:** the alert fires on a real hot hour during the demo, states the numbers, and dismisses cleanly.

**Complexity:** low

---

### Feature 6: Schedule export

**User story:** as a contractor I want the plan in a file my scheduler can read.

**How it works:** csv and ics downloads generated from the calendar, with a preview shown in the export drawer.

**Acceptance criteria:** both files open in standard tools, filenames carry the date.

**Complexity:** low

---

### Feature 7: Impact counters

**User story:** as a builder I want the avoided cost and emissions visible because that is the pitch.

**How it works:** cost avoided and co2 avoided counters computed from editable assumptions, labelled as assumptions on screen, never presented as measured facts.

**Acceptance criteria:** counters count up on load, assumption labels visible, values editable.

**Complexity:** low

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Backend | Python + FastAPI | Small async api, proxies fortyguard, owns the cache and the model |
| Data cache | SQLite, single table | Trial credits are finite, every api hour is fetched once and stored |
| Model | Plain python functions | ACI 305 thresholds and percentile math, no ml needed, and no fake ml impresses a judge who hunts fake precision |
| Frontend | React 18 + Vite + TypeScript | Fast build, standard tooling |
| Map | Leaflet + react-leaflet | Free, light basemap support, polygon rendering |
| Basemap | CARTO Positron light tiles | Free tier, attribution friendly |
| Styling | Tailwind CSS v4 | Utility first, theme tokens in css |
| Animation | motion/react | Blur-in entrances, overlay transitions |
| Icons | Inline SVG + Material Icons CDN | Per the frontend skill rules |
| Fonts | Archivo + IBM Plex Mono | Google Fonts, swiss rational pairing |

No database server, no auth, no payments. The app runs locally for the demo recording, with an optional free host for the submission link.

---

## Database Schema

```sql
CREATE TABLE api_cache (
  key        TEXT PRIMARY KEY,   -- query params hashed
  payload    TEXT NOT NULL,      -- raw json response
  fetched_at INTEGER NOT NULL    -- unix timestamp
);

CREATE TABLE sites (
  id         TEXT PRIMARY KEY,
  name       TEXT NOT NULL,
  lat        REAL NOT NULL,
  lon        REAL NOT NULL,
  thickness  REAL DEFAULT 8,     -- inches, affects the amber band
  mass       INTEGER DEFAULT 0,  -- mass concrete flag tightens the limit
  pour_cost  REAL DEFAULT 12000, -- usd assumption per failed pour
  re_pour_co2 REAL DEFAULT 0.9  -- tonnes per re-pour avoided, assumption
);
```

The alert is derived state, no table needed. The cache never expires during the hackathon, which is the whole point of credit safety.

---

## API Architecture

All fortyguard calls live server side. The frontend never holds the api key.

```
GET  /api/health            -> { status, credits }
GET  /api/cells?lat&lon     -> current grid for the area, cached
GET  /api/forecast?siteId   -> next 12 hours, cached
GET  /api/climatology?siteId&date -> percentiles from history, cached
GET  /api/sites             -> list of demo sites
POST /api/sites             -> create a site
GET  /api/sites/{id}/window -> the aci model output for the next 12 hours
GET  /api/export.csv?siteId -> the two week schedule as csv
GET  /api/export.ics?siteId -> the two week schedule as ics
```

Every endpoint returns a `source` field with its provenance tag, live, forecast, history, model, or cached. The frontend renders that tag verbatim.

---

## User Flow and Screens

One screen. Load, the console blurs in, the map draws the heat grid over Phoenix, the counters count up. Click a grid cell, the site pins, the callout shows the temperature, the rail computes the window. The twelve hour strip shows the forecast, the calendar shows the two weeks. The breach alert fires live when the hottest forecast hour crosses the limit, the demo dismisses it, opens the export drawer, shows the csv preview, ends on the counters.

The silent recording follows exactly that path. No dead ends, no menu navigation, every click is part of the story.

---

## What Is Not Being Built in the Hackathon

- No user accounts or auth
- No payment or monetisation flow
- No mobile app
- No humidity and wind data integration, the temperature only model is the honest scope
- No multi city support beyond the demo cities
- No machine learning, the physics model is the model
- No landing page, the console is the deliverable

All deferred until after the hackathon, except the landing page which is a deliberate scope decision.

---

## Post Hackathon Monetisation Sketch

Free tier for one site with limited history, a per project tier at twenty nine dollars a month for unlimited sites and exports, and an enterprise tier for cities and capital programmes. Readymix suppliers are the natural first paying segment because a rejected truck is a measurable loss they already track.

---

## Hackathon Build Priority

The deadline is August 30 2026. The judges were told in the mentor session to hunt fake correlations and fake precision, so honesty labels are a scoring feature, not a nicety.

Priority order:

1. Verification script proves the api works for Phoenix, current, forecast and history
2. Backend cache layer, one fetch per hour forever
3. Map renders the real grid
4. ACI model classifies any hour green, amber or red
5. Calendar shows forecast and climatology with honest labels
6. Breach alert fires on real data
7. Exports download and open
8. Counters with assumption labels
9. Silent demo video recorded per the recording guide
10. Submission with a day of buffer for api problems

---

## Hackathon Checklist

- Project name: curo
- Hackathon: FortyGuard Hackathon'26, building the world's temperature ai
- Submission deadline: August 30 2026
- Track: Industrial and Enterprise, track 03, with the model work crossing into track 05
- FortyGuard data is central, the faq requires it
- No non us locations, demo in Phoenix, Arizona
- Data from January 2021 to present only, forecast 12 hours ahead only
- No mock data anywhere, every number carries its provenance tag
- Silent screen recording, no voiceover, no captions, per the owner's style
- Public repo required before submission
- Readme explains the physics, the assumptions and the data sources
