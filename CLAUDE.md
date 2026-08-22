# curo — Agent Context

## What This Is

curo is a pour window planner for concrete construction, built on the FortyGuard Temperature API for Hackathon'26, the building the world's temperature ai event. It joins hyperlocal temperature data with the ACI 305 hot weather rules and tells a contractor which hours and days are safe to pour concrete. The export drops into any scheduler. The breach alert fires before the truck leaves.

Built for FortyGuard Hackathon'26. Build sprint ends August 30 2026, submission deadline August 30. Demo city is Phoenix, Arizona. The api covers the United States only.

---

## One Line Pitch

Know the hour a pour will fail, before the concrete arrives.

---

## Non Negotiables

1. No mock data. Every number on screen is live api data, api history or a model output, and every one carries its provenance tag.
2. Every api response is cached in sqlite. Never fetch the same hour twice. Trial credits are finite.
3. The demo video is silent. No voiceover, no captions. The app's labels are the narration.
4. FortyGuard data must be central to the project, the faq requires it.
5. Api limits: us only, data from January 2021 to present, forecast 12 hours ahead only.
6. No logo, no favicon, no brand mark. Slots are code comments until the owner provides assets. The wordmark is plain text.

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI + httpx |
| Cache | SQLite, single table, key is hashed query params |
| Model | Plain python functions, ACI 305R-20 rules, no ml |
| Frontend | React 18 + Vite + TypeScript |
| Map | Leaflet + react-leaflet, CARTO Positron light tiles |
| Styling | Tailwind CSS v4, theme tokens in css |
| Animation | motion/react |
| Fonts | Archivo (ui) + IBM Plex Mono (numbers and labels) |
| Icons | Inline SVG + Material Icons CDN |

---

## Design System

All design decisions are confirmed across seven gates. Do not deviate from any value below. Full detail lives in FRONTEND_SPEC.md.

**Aesthetic:** light field console. Daylight utility surfaces, the heat map is the only vivid element. Blueprint annotation accents.

**Fonts:** Archivo for ui text and headings, IBM Plex Mono for every number, label, timestamp and provenance tag. Load via Google Fonts in index.html.

**Colour palette — Cool Concrete:**

```css
--bg-primary:     #eef1f4;
--bg-secondary:   #e6eaee;
--surface:        #f7f9fb;
--elevated:       #fdfefe;
--ink:            #14181d;
--text-secondary: #4c545e;
--text-muted:     #8a939d;
--border-subtle:  rgba(20, 24, 29, 0.06);
--border-default: rgba(20, 24, 29, 0.12);
--accent:         #c2410c;
--accent-hover:   #9a3412;
--accent-soft:    rgba(194, 65, 12, 0.08);
--blueprint:      #4a7a94;
--success:        #15803d;
--warning:        #b45309;
--error:          #dc2626;
```

The heat ramp runs #3b82f6, #14b8a6, #84cc16, #facc15, #f97316, #dc2626 and belongs to the map alone, never to ui chrome.

**Structure:** top bar with dual pill split, wordmark left, live status and export right, empty centre. Main console 60/40, map cell left, decision rail right. Rail is one surface with hairline dividers, borders over cards.

**Motion:** subtle precision. Blur-in entrances only, staggered 0.08 to 0.55 seconds. Ambient breathing washes behind the page at 4 to 9 percent opacity, 14s and 18s loops. The breach alert sweeps in on a 0.25s curve and exits in 0.15s. Counters count up once over 1.2s.

**Z-index scale:** page 0, map 10, map ui 20, top bar 200, backdrop 300, overlays 400, grain 500.

---

## Physics Model

Placement limit 95 degrees fahrenheit per ACI 305R-20. Amber band within 5 degrees. Mass concrete tightens the limit by 10 degrees. Slab thickness over 12 inches widens amber to 7 degrees. The model shows which rules fired and why, on screen, always.

---

## Code Rules, Follow Without Exception

**TypeScript and Python:**
- camelCase for variables and functions
- JSDoc comments on every function and custom hook
- No inline styles in React unless a dynamic value requires it
- Theme tokens from the css file, never hardcoded hex values in components
- No emojis as ui elements, no third party icon libraries
- No onMouseEnter or onMouseLeave for styling, css class hover states only
- No localStorage or sessionStorage
- No console.log in production paths

**Writing rules, all copy, labels, comments, docs:**
- British English throughout
- No em dashes anywhere
- Short direct sentences
- No filler phrases: no seamlessly, powerful, robust, leverage, cutting-edge, unlock
- Button labels are verb plus object: export csv, reschedule pour, retry
- Error messages state the cause and the fix: api unreachable, showing cached data from 14:00
- Empty states are honest: select a site to begin, click any grid cell on the map

**Component rules:**
- All entrances blur in, filter blur plus opacity plus translate
- Loading states use skeleton shimmer, never spinners
- Hover feedback shifts border colour or lifts the card, never scales imagery
- Every interactive element has a visible focus ring
- All motion respects prefers-reduced-motion

**Never do these:**
- Never fabricate, mock or demo-fake any data
- Never fetch the same api hour twice
- Never add branding, logos or icons the owner has not provided
- Never use JetBrains Mono, Inter, Roboto, Arial or Space Grotesk
- Never use pure black or pure white
- Never use gradient text, outer neon glows or custom cursors
- Never use warm cream or beige surfaces
- Never put a purple gradient anywhere

---

## Hackathon Checklist

- Project name: curo
- Hackathon: FortyGuard Hackathon'26
- Submission deadline: August 30 2026
- Track: Industrial and Enterprise, track 03, model work crosses into track 05
- Demo city: Phoenix, Arizona
- Silent screen recording, no voiceover, no captions, per RECORDING_GUIDE.md
- Public repo required, readme explains the physics, assumptions and data sources
