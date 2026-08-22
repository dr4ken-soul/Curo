# curo — Frontend Spec

## Overview

This document is the authoritative frontend specification for curo, the concrete pour planning console built on the FortyGuard Temperature API for Hackathon'26. It exists alongside CLAUDE.md and BUILD_GUIDE.md. CLAUDE.md holds design system values and code rules. BUILD_GUIDE.md holds component build order and implementation detail. This file holds the complete visual and interaction specification for every element of the console, written to be passed directly to a coding agent.

Read all three files before writing any component.

The deliverable is a single screen app interior, not a landing page. The console is the product. The demo is a silent screen recording, so every on screen label carries the story. Every element must earn its place.

---

## Design System

### Colour palette — Cool Concrete

```css
:root {
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

  /* Heat ramp, data use only, never in ui chrome */
  --heat-0: #3b82f6;
  --heat-1: #14b8a6;
  --heat-2: #84cc16;
  --heat-3: #facc15;
  --heat-4: #f97316;
  --heat-5: #dc2626;
}
```

Colour strategy: restrained. Tinted neutrals plus one action accent on less than ten percent of the surface. The only saturated colour fields are the heat ramp cells on the map, the status banners and the alert. That contrast is the design.

No cream, no sand, no beige. The light surface is deliberately cool, per the 2026 anti default rules in FRONTEND_SKILL.md. No pure black and no pure white anywhere.

### Fonts

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
```

- `font-ui` = Archivo, for all interface text and headings, weights 400, 500, 600, 700
- `font-mono` = IBM Plex Mono, for every number, label, timestamp, coordinate and provenance tag, weights 400, 500, 600

Every numeric value uses `font-variant-numeric: tabular-nums`. No other fonts appear in the project.

### Typography scale

```
display:   font-ui 700, clamp(2rem, 3vw, 2.5rem) / leading-none / tracking-[-0.02em]   (counter numbers)
heading:   font-ui 600, 1.125rem / leading-snug                                      (module titles, alert headline)
body:      font-ui 400, 0.9375rem / leading-relaxed                                   (explanatory text)
label:     font-mono 500, 0.6875rem / tracking-[0.12em] / uppercase                    (section labels)
data:      font-mono 500, 0.875rem / tabular-nums                                      (temperatures, times, coordinates)
data-sm:   font-mono 400, 0.6875rem / tabular-nums                                     (secondary data)
```

### Spacing and radius tokens

```
spacing scale: 4 8 12 16 20 24 32 40 48 64 px
radius: sm 6px, md 10px, lg 14px, xl 20px, pill 9999px
```

One radius language. Cards and panels are `rounded-xl` (20px), inner cells `rounded-lg` (14px), chips and buttons `rounded-full`. Nothing over 20px, nothing else.

### Transitions

```
fast:    150ms cubic-bezier(0.16, 1, 0.3, 1)
default: 220ms cubic-bezier(0.16, 1, 0.3, 1)
slow:    400ms cubic-bezier(0.16, 1, 0.3, 1)
```

All transitions use these curves. No linear, no bounce, no elastic.

### Semantic z-index scale

```
z-0:     page background and ambient washes
z-10:    map canvas and grid layer
z-20:    map ui (callout, legend, timestamp chip, marker)
z-200:   top bar (sticky)
z-300:   overlay backdrop (breach alert)
z-400:   overlay panels (breach alert, export drawer)
z-500:   toasts
```

Never use arbitrary values like 999.

### Tailwind v4 theme block

In `src/styles/globals.css`, after `@import "tailwindcss"`:

```css
@theme {
  --color-bg: #eef1f4;
  --color-bg-2: #e6eaee;
  --color-surface: #f7f9fb;
  --color-elevated: #fdfefe;
  --color-ink: #14181d;
  --color-text-2: #4c545e;
  --color-text-3: #8a939d;
  --color-line: rgba(20, 24, 29, 0.06);
  --color-line-2: rgba(20, 24, 29, 0.12);
  --color-accent: #c2410c;
  --color-accent-hover: #9a3412;
  --color-blueprint: #4a7a94;
  --color-success: #15803d;
  --color-warning: #b45309;
  --color-error: #dc2626;
  --color-heat-0: #3b82f6;
  --color-heat-1: #14b8a6;
  --color-heat-2: #84cc16;
  --color-heat-3: #facc15;
  --color-heat-4: #f97316;
  --color-heat-5: #dc2626;
  --font-ui: "Archivo", sans-serif;
  --font-mono: "IBM Plex Mono", monospace;

  --animate-pulse-soft: pulse-soft 2s ease-in-out infinite;
  --animate-breathe-a: breathe-a 14s ease-in-out infinite;
  --animate-breathe-b: breathe-b 18s ease-in-out infinite;
  --animate-shimmer: shimmer 1.8s linear infinite;
  --animate-ring-pulse: ring-pulse 2.4s ease-out infinite;

  @keyframes pulse-soft {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.45; }
  }
  @keyframes breathe-a {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.055; }
    50% { transform: translate(24px, -16px) scale(1.08); opacity: 0.09; }
  }
  @keyframes breathe-b {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.04; }
    50% { transform: translate(-28px, 18px) scale(1.12); opacity: 0.07; }
  }
  @keyframes shimmer {
    from { background-position: -200% 0; }
    to { background-position: 200% 0; }
  }
  @keyframes ring-pulse {
    0% { transform: scale(0.9); opacity: 0.7; }
    70%, 100% { transform: scale(2.1); opacity: 0; }
  }
}
```

This generates classes `bg-bg`, `bg-surface`, `text-ink`, `border-line-2`, `font-ui`, `font-mono`, `animate-breathe-a` and so on. Never hardcode hex values in component files.

### Ambient background washes

The page background carries two breathing washes at very low opacity, per the gate three decision. They live behind the console, never inside panels, and they must be invisible in a paused frame, only perceptible in motion.

```tsx
<div className="absolute inset-0 z-0 overflow-hidden pointer-events-none" aria-hidden="true">
  <div className="absolute -top-24 -left-24 w-[520px] h-[420px] rounded-full bg-blueprint blur-[140px] animate-breathe-a" />
  <div className="absolute -bottom-32 -right-20 w-[560px] h-[440px] rounded-full bg-accent blur-[150px] animate-breathe-b" />
</div>
```

All of it wrapped in `@media (prefers-reduced-motion: reduce)` that sets `animation: none` and `opacity: 0.05`.

### Grain overlay

One fixed grain layer over the entire console, from FRONTEND_SKILL.md Technique 7, at 2 percent opacity so it textures the light surface without reading as dirt.

```tsx
<div className="fixed inset-0 pointer-events-none z-500 opacity-[0.02]" aria-hidden="true"
  style={{
    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
    backgroundSize: '128px 128px',
  }}
/>
```

z-500 is above the overlays on purpose. Grain covers everything uniformly, film style.

### Scrollbar hiding

```css
html {
  scrollbar-width: none;
}
html::-webkit-scrollbar {
  display: none;
}
```

The console fits one viewport. The only scrollable region is the decision rail and its scrollbar is hidden the same way.

### Glass classes, light variant

Backdrop blur applies only to fixed and sticky elements, per FRONTEND_SKILL.md Step 17. Two uses: the top bar pills and the overlay panels.

```css
.glass-light {
  background: rgba(253, 254, 254, 0.82);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-subtle);
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.6);
}
```

---

## Global Code Rules

- No hardcoded hex values in component files. CSS variables and theme tokens only.
- Icons come from inline SVG or the Material Icons CDN link. No emoji as ui elements. No third party icon libraries.
- British English throughout. No em dashes anywhere, in copy, comments or docs.
- Copy is plain functional language. Banned words: elevate, seamless, unleash, unlock, next-gen, empower, revolutionise, transform, cutting-edge, supercharge.
- No placeholder data of any kind. Every number on screen is live api data, api history, or a model output, and every one carries its provenance tag.
- No onMouseEnter or onMouseLeave for styling. CSS class hover states only.
- No localStorage or sessionStorage. The api cache lives in the backend sqlite store.
- No logo, no favicon, no brand mark. Both slots are code comments until the owner provides assets. The wordmark is plain text.
- No gradient text on any heading.
- No outer neon glows. No custom cursors.
- Hover feedback never scales images. Cards lift or shift border colour only.
- Every interactive element has a visible focus ring: `focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg`.
- All entrances use blur-in, filter blur plus opacity plus translate, never bare opacity fades.
- All motion respects `prefers-reduced-motion: reduce` by collapsing to instant state.

---

## Screen Inventory

One screen, the console, plus three transient layers.

1. Top bar, dual pill split, sticky
2. Main console, 60/40 grid, map cell left, decision rail right
3. Breach alert overlay, modal
4. Export drawer, right slide panel

Plus designed states: loading skeletons, empty state with no site selected, api error banner with cached data fallback.

---

## Section 1 — Top Bar

**Component:** `src/components/layout/TopBar.tsx`

**Behaviour:** Sticky top of viewport, dual pill split per the gate two decision. Wordmark pill left, status and export pill right. Nothing in the centre. The empty middle is the design.

```tsx
<header className="sticky top-0 z-200 px-4 lg:px-6 py-3">
  <div className="flex items-center justify-between gap-3">

    {/* Left pill: wordmark */}
    <div className="glass-light rounded-full px-5 py-2.5">
      {/* Logo slot: replace with public/logo.svg once provided */}
      <span className="font-ui text-[1.125rem] font-semibold lowercase tracking-tight text-ink">
        curo
      </span>
    </div>

    {/* Right pill: live status, timestamp, export */}
    <div className="glass-light rounded-full px-2 py-1.5 flex items-center gap-1">

      <div className="flex items-center gap-2 px-3 py-1.5">
        <span className="w-2 h-2 rounded-full bg-success animate-pulse-soft" aria-hidden="true" />
        <span className="font-mono text-data text-ink">live</span>
        <span className="font-mono text-data-sm text-text-3">phoenix az</span>
      </div>

      <div className="h-4 w-px bg-line-2" aria-hidden="true" />

      <div className="px-3 py-1.5">
        <span className="font-mono text-data-sm text-text-2 tabular-nums">14:00 utc-7</span>
      </div>

      <div className="h-4 w-px bg-line-2" aria-hidden="true" />

      <button
        onClick={openExport}
        className="flex items-center gap-2 px-4 py-2 rounded-full bg-ink text-elevated text-sm font-medium
                   hover:bg-text-2 transition-colors duration-fast
                   focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v12m0 0l-4-4m4 4l4-4M4 20h16" />
        </svg>
        export
      </button>

    </div>
  </div>
</header>
```

The export button is the primary action of the top bar and it is the only dark element in the bar, so it reads as the action from a paused frame.

**Entrance:** Left pill `initial={{ opacity: 0, filter: 'blur(8px)', y: 12 }}`, `animate={{ opacity: 1, filter: 'blur(0px)', y: 0 }}`, `transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1], delay: 0 }}`. Right pill same values, `delay: 0.08`.

---

## Section 2 — Map Cell

**Component:** `src/components/console/MapCell.tsx`

**Behaviour:** The dominant visual. 60 percent of the console width. Leaflet map with a light basemap, the FortyGuard geohash grid rendered as a heat ramp, blueprint annotation callouts, and a selected site crosshair.

**Structure and z-index:**

```
z-10: map canvas (leaflet, absolute inset-0)
z-10: heat grid polygon layer (leaflet pane)
z-20: selected site marker with pulsing ring
z-20: callout card with leader line
z-20: legend bar
z-20: timestamp chip
z-20: empty state (when no site selected)
```

**Map cell wrapper:**

```tsx
<section className="col-span-12 lg:col-span-7 relative overflow-hidden rounded-xl border border-line-2 bg-bg-2 min-h-[420px] lg:min-h-0">
  <MapContainer
    center={[33.4484, -112.074]}
    zoom={13}
    zoomControl={false}
    attributionControl={true}
    className="absolute inset-0 z-10"
  >
    <TileLayer
      url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    />
  </MapContainer>
</section>
```

CARTO Positron is the light basemap. Attribution is mandatory and visible.

**Heat grid layer:**

Each geohash cell renders as a polygon. Fill from the heat ramp by temperature band, opacity 0.8, hairline stroke.

```tsx
<Polygon
  positions={cell.bounds}
  pathOptions={{
    color: 'rgba(253, 254, 254, 0.7)',
    weight: 1,
    fillColor: heatColor(cell.tempF),
    fillOpacity: 0.8,
  }}
/>
```

`heatColor()` maps temperature to ramp bands:

```
below 80°f:    heat-0
80 to 88°f:    heat-1
89 to 95°f:    heat-2
96 to 102°f:   heat-3
103 to 109°f:  heat-4
110°f and up:  heat-5
```

Cell fills transition between colours with `transition: fill 400ms cubic-bezier(0.16, 1, 0.3, 1)` so live updates read as a slow colour drift, never a blink.

**Selected site marker:**

A crosshair drawn as inline SVG over the site cell, blueprint coloured, with a soft ring pulse, the one deliberate motion element on the map.

```tsx
<div className="absolute z-20 pointer-events-none" style={{ left: x, top: y }}>
  <span className="absolute inset-0 -m-3 rounded-full border border-blueprint animate-ring-pulse" aria-hidden="true" />
  <svg className="w-6 h-6 text-blueprint" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6">
    <circle cx="12" cy="12" r="7" />
    <path d="M12 3v4M12 17v4M3 12h4M17 12h4" />
  </svg>
</div>
```

**Callout card:**

Blueprint style annotation, top left of the map cell, connected to the marker by a dashed leader line. This is the blueprint trend accent.

```tsx
<div className="absolute top-4 left-4 z-20 max-w-[240px] bg-elevated/95 backdrop-blur-sm border border-line-2 rounded-lg p-3">
  <p className="font-ui text-sm font-semibold text-ink">site 01 · downtown phoenix</p>
  <p className="font-mono text-data-sm text-text-3 tabular-nums mt-1">33.4484 n · 112.0740 w</p>
  <p className="font-mono text-xl font-medium text-ink tabular-nums mt-2">
    102<span className="text-text-3 text-data-sm">°f</span>
  </p>
  <p className="font-mono text-[10px] uppercase tracking-[0.12em] text-text-3 mt-1">source: api live · measured 2m</p>
</div>
```

The leader line is an SVG dashed line drawn from the callout's bottom right corner toward the marker. Stroke `var(--blueprint)`, `strokeDasharray="3 3"`, width 1. Rendered in an absolutely positioned svg layer at z-20, pointer-events none. Recompute the path when the map pans.

**Legend bar:**

```tsx
<div className="absolute bottom-4 left-4 z-20 flex items-center gap-2 bg-elevated/90 backdrop-blur-sm border border-line-2 rounded-full px-3 py-1.5">
  <span className="font-mono text-[10px] text-text-3">cool</span>
  <div className="w-28 h-2 rounded-full"
    style={{ background: 'linear-gradient(90deg, #3b82f6 0%, #14b8a6 20%, #84cc16 40%, #facc15 60%, #f97316 80%, #dc2626 100%)' }} />
  <span className="font-mono text-[10px] text-text-3">extreme</span>
</div>
```

The gradient is the one place a literal heat ramp appears, it is data colour, not decoration.

**Timestamp chip:**

```tsx
<div className="absolute top-4 right-4 z-20 bg-elevated/90 backdrop-blur-sm border border-line-2 rounded-full px-3 py-1.5">
  <span className="font-mono text-data-sm text-text-2 tabular-nums">2026-08-22 14:00 · api live</span>
</div>
```

**Empty state, no site selected:**

```tsx
<div className="absolute inset-0 z-20 flex flex-col items-center justify-center gap-3 bg-bg/40">
  <svg className="w-8 h-8 text-text-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true">
    <circle cx="12" cy="12" r="8" />
    <circle cx="12" cy="12" r="2" />
    <path d="M12 4v2M12 18v2M4 12h2M18 12h2" />
  </svg>
  <p className="font-ui text-sm font-medium text-ink">select a site to begin</p>
  <p className="font-mono text-data-sm text-text-3">click any grid cell on the map</p>
</div>
```

**Map entrance:** wrapper `initial={{ opacity: 0, filter: 'blur(10px)', scale: 0.98 }}`, `animate={{ opacity: 1, filter: 'blur(0px)', scale: 1 }}`, `transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1], delay: 0.1 }}`. Callout delay 0.45. Legend and chip delay 0.55.

---

## Section 3 — Decision Rail

**Component:** `src/components/console/DecisionRail.tsx`

**Behaviour:** The right 40 percent. One surface panel with hairline dividers between modules, per the dashboard hardening rule in FRONTEND_SKILL.md Step 17. Borders over cards. No boxed metrics, no floating cards.

```tsx
<aside className="col-span-12 lg:col-span-5 flex flex-col min-h-0 overflow-y-auto rounded-xl border border-line-2 bg-surface">
  <SiteStatus />
  <HourStrip />
  <Calendar />
  <Counters />
</aside>
```

Modules separated by `divide-y divide-line`. The rail scrolls internally if it overflows the viewport, scrollbar hidden.

### Module 1 — Site Status

```tsx
<section className="p-4 lg:p-5">
  <p className="font-mono text-label text-text-3">site 01 · pour window</p>

  <div className={`mt-3 rounded-lg border-l-4 p-3 ${
    status === 'green'  ? 'border-success bg-success/8'
    : status === 'amber' ? 'border-warning bg-warning/8'
    : 'border-error bg-error/8'
  }`}>
    <p className="font-ui text-lg font-semibold text-ink">
      {status === 'green' ? 'safe to pour' : status === 'amber' ? 'window closing' : 'do not pour'}
    </p>
    <p className="font-mono text-data-sm text-text-2 tabular-nums mt-1">
      {status === 'green'
        ? 'margin +11°f under the 95°f placement limit'
        : status === 'amber'
        ? 'forecast within 5°f of the 95°f placement limit'
        : 'forecast 102°f exceeds the 95°f placement limit'}
    </p>
  </div>

  <div className="mt-3 space-y-1.5">
    <RuleLine ok label="placement limit 95°f · aci 305r-20" />
    <RuleLine ok label="humidity and wind within limits" />
    <RuleLine warn label="slab thickness 8in · amber band ±5°f" />
  </div>
</section>
```

RuleLine renders a check or warning inline svg in blueprint colour plus a mono label.

```tsx
function RuleLine({ ok, warn, label }: { ok?: boolean; warn?: boolean; label: string }) {
  return (
    <p className="flex items-center gap-2 font-mono text-data-sm text-text-2">
      {ok ? (
        <svg className="w-3.5 h-3.5 text-success" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4 10-10" />
        </svg>
      ) : warn ? (
        <svg className="w-3.5 h-3.5 text-warning" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01" />
        </svg>
      ) : null}
      {label}
    </p>
  )
}
```

Status changes animate the banner colour with `transition-colors duration-slow`.

### Module 2 — Twelve Hour Strip

```tsx
<section className="p-4 lg:p-5">
  <div className="flex items-center justify-between">
    <p className="font-mono text-label text-text-3">next 12 hours</p>
    <p className="font-mono text-data-sm text-text-3">api forecast</p>
  </div>

  <div className="mt-3 grid grid-cols-12 gap-1">
    {hours.map((hour, i) => (
      <div key={i} className={`rounded-md h-16 flex flex-col items-center justify-center gap-1
        ${hour.status === 'green' ? 'bg-success/10' : hour.status === 'amber' ? 'bg-warning/10' : 'bg-error/10'}
        ${i === currentIndex ? 'ring-2 ring-ink/15' : ''}`}>
        <span className="font-mono text-data-sm text-ink tabular-nums">{hour.tempF}°</span>
        <span className="font-mono text-[10px] text-text-3">{hour.hour}</span>
      </div>
    ))}
  </div>
</section>
```

Cell colours use the status scale, not the heat ramp. The heat ramp belongs to the map alone. The current hour carries the ring. A forecast hour predicted to breach renders with `bg-error/10` and its temperature in `text-error`.

### Module 3 — Two Week Calendar

The centrepiece module. Fourteen day cells, two rows of seven. Forecast hours first, climatology after, per the hackathon faq limits.

```tsx
<section className="p-4 lg:p-5 flex-1 min-h-0">
  <div className="flex items-center justify-between">
    <p className="font-mono text-label text-text-3">two week window</p>
    <div className="flex items-center gap-2">
      <span className="font-mono text-[10px] uppercase tracking-[0.12em] text-text-3">first 12h forecast</span>
      <span className="font-mono text-[10px] uppercase tracking-[0.12em] text-text-3">then climatology p25–p75</span>
    </div>
  </div>

  <div className="mt-3 grid grid-cols-7 gap-1.5">
    {days.map((day) => (
      <div key={day.date} className="rounded-lg border border-line-2 p-2 bg-elevated">
        <p className="font-mono text-[10px] uppercase tracking-[0.08em] text-text-3">{day.weekday}</p>
        <p className="font-mono text-data-sm text-ink tabular-nums mt-0.5">{day.date}</p>
        <div className={`mt-1.5 h-1.5 rounded-full ${
          day.worst === 'red' ? 'bg-error' : day.worst === 'amber' ? 'bg-warning' : 'bg-success'
        }`} />
        <p className="font-mono text-[10px] text-text-2 tabular-nums mt-1.5">{day.range}</p>
        <p className="font-mono text-[10px] text-text-3 tabular-nums">{day.confidence}</p>
      </div>
    ))}
  </div>
</section>
```

Day data: `weekday` short form, `date` like "22", `worst` the worst hour status that day, `range` like "91°–104°", `confidence` the percentile band width as a percentage. Confidence shrinks as the horizon extends, and the label is honest about it.

### Module 4 — Counters and Export

```tsx
<section className="p-4 lg:p-5">
  <div className="grid grid-cols-2 gap-3">
    <div className="rounded-lg border border-line-2 bg-elevated p-3">
      <p className="font-mono text-label text-text-3">cost avoided</p>
      <p className="font-ui text-[2rem] font-bold leading-none tracking-[-0.02em] text-ink mt-2 tabular-nums">
        $24,000
      </p>
      <p className="font-mono text-[10px] text-text-3 mt-1.5">assumption · $12k per failed pour · 2 avoided</p>
    </div>
    <div className="rounded-lg border border-line-2 bg-elevated p-3">
      <p className="font-mono text-label text-text-3">co2 avoided</p>
      <p className="font-ui text-[2rem] font-bold leading-none tracking-[-0.02em] text-ink mt-2 tabular-nums">
        1.8<span className="text-base">t</span>
      </p>
      <p className="font-mono text-[10px] text-text-3 mt-1.5">assumption · 0.9t per re-pour avoided</p>
    </div>
  </div>

  <div className="mt-3 flex items-center gap-2">
    <button className="flex items-center gap-2 rounded-full border border-line-2 px-4 py-2 text-sm font-medium text-ink
      hover:border-ink/40 transition-colors duration-fast
      focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-surface">
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v12m0 0l-4-4m4 4l4-4M4 20h16" />
      </svg>
      export csv
    </button>
    <button className="flex items-center gap-2 rounded-full border border-line-2 px-4 py-2 text-sm font-medium text-ink
      hover:border-ink/40 transition-colors duration-fast
      focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-surface">
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v12m0 0l-4-4m4 4l4-4M4 20h16" />
      </svg>
      export ics
    </button>
    <p className="ml-auto font-mono text-[10px] uppercase tracking-[0.12em] text-text-3">imports into any scheduler</p>
  </div>
</section>
```

Counter animation: numbers count up from zero over 1.2 seconds, ease-out, starting at 0.6s after load, once per page load. Formatting keeps the dollar sign and unit static while digits roll. This is the one moment of showmanship in the console, and it lands before any judge's eyes have left the map.

**Rail entrance stagger:** module 1 delay 0.2, module 2 delay 0.3, module 3 delay 0.4, module 4 delay 0.5. Each module `initial={{ opacity: 0, filter: 'blur(8px)', y: 16 }}`, `animate={{ opacity: 1, filter: 'blur(0px)', y: 0 }}`, `transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}`.

---

## Section 4 — Breach Alert Overlay

**Component:** `src/components/overlays/BreachAlert.tsx`

**Behaviour:** Fires when the latest forecast crosses the placement limit for a scheduled pour. This is the dramatic beat of the silent demo, so it must read like a headline in a paused frame.

**Z-index:** backdrop z-300, panel z-400.

```tsx
<AnimatePresence>
  {alert && (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        className="fixed inset-0 z-300 bg-ink/50 backdrop-blur-sm"
        onClick={dismiss}
      />

      <motion.div
        role="alertdialog"
        aria-modal="true"
        aria-labelledby="breach-title"
        initial={{ opacity: 0, scale: 0.96, y: 8, filter: 'blur(8px)' }}
        animate={{ opacity: 1, scale: 1, y: 0, filter: 'blur(0px)' }}
        exit={{ opacity: 0, scale: 0.97, y: 6, filter: 'blur(4px)' }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
        className="fixed inset-x-0 top-1/2 z-400 mx-auto w-full max-w-md -translate-y-1/2 p-4"
      >
        <div className="rounded-xl border border-error/30 bg-elevated p-6 shadow-[0_16px_48px_rgba(20,24,29,0.18)]">
          <p className="font-mono text-label text-error">breach · pour site 01</p>
          <h2 id="breach-title" className="font-ui text-2xl font-bold text-ink mt-2">
            do not pour at 15:00
          </h2>
          <p className="font-mono text-data text-text-2 tabular-nums mt-2">
            forecast 102°f · limit 95°f · margin -7°f
          </p>

          <div className="mt-6 flex items-center justify-end gap-3">
            <button
              onClick={dismiss}
              className="text-sm font-medium text-text-2 hover:text-ink transition-colors duration-fast
                focus-visible:ring-2 focus-visible:ring-accent rounded-full px-3 py-2"
            >
              dismiss
            </button>
            <button
              onClick={reschedule}
              className="rounded-full bg-ink text-elevated px-5 py-2.5 text-sm font-medium
                hover:bg-text-2 transition-colors duration-fast
                focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-elevated"
            >
              reschedule pour
            </button>
          </div>
        </div>
      </motion.div>
    </>
  )}
</AnimatePresence>
```

Behaviour rules from FRONTEND_SKILL.md Step 16:

- Focus moves into the primary action on open, returns to the export button on close
- Escape closes the alert
- Exit is faster than enter, 0.15s versus 0.25s
- Backdrop click dismisses, the panel itself does not
- The alert never blocks the app behind it for more than the moment it takes to read

The same panel pattern renders the green counterpart when a cancelled day turns safe again, headline "window reopened at 09:00", border-success instead of border-error. Judges see the alert as a two way system, not a one note alarm.

---

## Section 5 — Export Drawer

**Component:** `src/components/overlays/ExportDrawer.tsx`

**Behaviour:** Slides in from the right edge. Lists the two schedule files with live metadata and a mono preview of the csv.

**Z-index:** backdrop z-300, drawer z-400.

```tsx
<AnimatePresence>
  {open && (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2, ease: 'easeOut' }}
        className="fixed inset-0 z-300 bg-ink/30"
        onClick={close}
      />

      <motion.div
        role="dialog"
        aria-modal="true"
        aria-label="Export pour schedule"
        initial={{ x: 40, opacity: 0, filter: 'blur(8px)' }}
        animate={{ x: 0, opacity: 1, filter: 'blur(0px)' }}
        exit={{ x: 24, opacity: 0, filter: 'blur(4px)' }}
        transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
        className="fixed top-0 right-0 z-400 h-full w-[360px] border-l border-line-2 bg-elevated p-6 flex flex-col"
      >
        <p className="font-mono text-label text-text-3">export schedule</p>

        <div className="mt-6 space-y-4">
          <ExportRow name="curo-pour-plan-2026-08-22.csv" size="4.1 kb" lines={previewLines} />
          <ExportRow name="curo-pour-plan-2026-08-22.ics" size="2.8 kb" lines={icsPreviewLines} />
        </div>

        <div className="mt-8 rounded-lg border border-line-2 bg-bg-2 p-3">
          <p className="font-mono text-[10px] uppercase tracking-[0.12em] text-text-3 mb-2">csv preview</p>
          <pre className="font-mono text-data-sm text-text-2 leading-relaxed whitespace-pre-wrap">{csvPreview}</pre>
        </div>

        <p className="mt-auto font-mono text-[10px] uppercase tracking-[0.12em] text-text-3">
          imports into procore · ms project · any scheduler
        </p>
      </motion.div>
    </>
  )}
</AnimatePresence>
```

ExportRow is a row with the filename in mono, size in mono muted, and a download button with the download inline svg. Escape closes the drawer, focus returns to the export button.

---

## Section 6 — Loading, Error and Empty States

**Loading skeletons** (skeleton shimmer, never spinners):

```tsx
<div className="absolute inset-0 z-20 bg-bg-2 overflow-hidden rounded-xl">
  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-elevated/60 to-transparent animate-shimmer"
    style={{ backgroundSize: '200% 100%' }} />
</div>
```

The map cell shows one full surface skeleton. Each rail module shows a `h-20 rounded-lg bg-bg-2` block with the same shimmer inside, staggered 0.05s apart.

**Api error banner** sits at the top of the rail, above the modules:

```tsx
<div className="m-4 rounded-lg border border-error/30 bg-error/8 p-3 flex items-center gap-3">
  <svg className="w-4 h-4 text-error" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v4m0 4h.01" />
  </svg>
  <p className="font-mono text-data-sm text-ink">api unreachable · showing cached data from 14:00</p>
  <button className="ml-auto rounded-full border border-line-2 px-3 py-1.5 text-sm font-medium text-ink hover:border-ink/40 transition-colors duration-fast">
    retry
  </button>
</div>
```

Every error message states the cause and the fix, per the form and feedback rules. The cached fallback is a feature, the demo recording never dies on a dropped request.

---

## Entrance Animation Schedule

All entrances blur in. Full schedule in seconds:

```
0.00   top bar left pill
0.08   top bar right pill
0.10   map cell
0.20   rail module 1
0.30   rail module 2
0.40   rail module 3
0.45   map callout
0.50   rail module 4
0.55   map legend and timestamp chip
0.60   counter count up begins, runs 1.2s ease-out
```

Ambient washes breathe from first paint on a 14s and 18s loop. Grain is static.

---

## Responsive Behaviour

Primary canvas is 1920x1080, the recording resolution. The safe zone is 1280x800, every element must remain fully visible there without internal scroll in the rail.

- Below `lg` (1024px): the console stacks, map on top at `min-h-[420px]`, rail below, page scrolls, top bar pills stay sticky
- Mobile: touch targets minimum 44px, the hour strip becomes a horizontal scroll row with hidden scrollbar, the calendar grid stays 7 columns with reduced padding
- `prefers-reduced-motion: reduce`: every animation collapses to an instant state, including the ambient washes and the counter

---

## Asset Briefs

```
ASSET BRIEF: basemap tiles
  Source: CARTO Positron light tiles, free tier
  URL: https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png
  Attribution: OpenStreetMap and CARTO, visible in map control
  No image generation needed

ASSET BRIEF: logo
  Status: not provided. The wordmark is plain text.
  Slot: {/* Logo slot: replace with public/logo.svg once provided */}
  Never substitute a hardcoded symbol, emoji or generated icon

ASSET BRIEF: favicon
  Status: not provided.
  Slot: <!-- Favicon slot: replace with public/favicon.ico once provided -->

ASSET BRIEF: none other
  The console uses no imagery. Every visual is data, the map, and type.
```

No videos, no photographs, no illustrations. The heat map is the hero image.

---

## Data Provenance System

Every number on screen carries its source. These tags are the narration of the silent video.

```
api live       the current reading from the fortyguard api
api forecast   the 12 hour forecast from the api
api history    climatology percentiles from api history, 2021 to present
model          the aci 305 curing model output
assumption     an editable default used in a counter or limit
cached         served from the local cache after an api failure
```

Tags render as mono uppercase text at 10px in text-3. A judge pausing the video can audit every number.

---

## Spec Self-Check

Run before handing this file to the coding agent.

- [ ] Every element has exact Tailwind classes, no vague descriptions
- [ ] Every animation states initial, animate, duration, ease and delay
- [ ] Every layer has a z-index from the semantic scale
- [ ] Every asset need is covered by an asset brief
- [ ] Every positional class has responsive variants where the layout changes
- [ ] Quality benchmarks referenced: FRONTEND_SKILL.md Step 17 Dashboard Hardening, the Bento Grid Operational rules in section 2E, the counter pattern from the Premium Component Library, Reference 2 light surface treatment from Step 3C
- [ ] No em dashes anywhere in copy, comments or docs
- [ ] No banned copy words, no placeholder data, no emoji, no third party icon libraries
- [ ] The spec could be handed to a junior developer who could build it without asking a single design question

---

## Banned Patterns

The following must not appear anywhere in the codebase:

- Emoji as ui elements, third party icon libraries, raster icons
- Inter, Roboto, Arial, Space Grotesk or JetBrains Mono in any font declaration
- Hardcoded hex values in component files, theme tokens only
- Pure black or pure white backgrounds or text
- Gradient text on headings, outer neon glows, custom cursors
- Purple gradients, warm beige or cream surfaces
- Generic placeholder content, John Doe, Acme Inc, 99.9 percent
- Version labels, beta badges, section number eyebrows
- onMouseEnter or onMouseLeave styling logic
- localStorage or sessionStorage
- Spinner loading states, skeletons only
- Three equal feature cards in a row
- Any logo or favicon the owner has not provided, the slot must be a code comment
- Mock or fabricated data of any kind
