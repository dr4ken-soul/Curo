# curo recording guide

This is a silent screen recording of the working Curo console. The app is the narrator. Do not speak, add captions, add music, or place text over the video.

## What the recording must prove

The viewer should be able to see this story without audio:

1. Curo is connected to live FortyGuard data for Phoenix.
2. A concrete site has a temperature-based pour decision.
3. The next twelve hours are classified by the ACI model.
4. The two-week view separates forecast data from historical climatology.
5. A real red forecast creates a breach warning.
6. The plan can be exported for another scheduler.
7. Cost and CO2 values are assumptions, clearly labelled as assumptions.

Do not invent a red hour if the live forecast is green or amber. A real green or amber result is better evidence than a fabricated breach.

## Before recording

### 1. Check the API and start the app

Open PowerShell in the Curo folder and run the verification command first:

```powershell
cd "C:\Users\Paul\Documents\Coding Area\Hackathon\Curo\backend"
.\.venv\Scripts\python.exe verify.py
```

The command must print three successful lines labelled `current`, `forecast`, and `history`. The lines include Fahrenheit values and their sources. Do not record the terminal. Close it or minimise it after verification.

Start the backend in that same terminal:

```powershell
.\.venv\Scripts\python.exe -m uvicorn curo.main:app --reload --port 8000
```

Open a second PowerShell window and start the frontend:

```powershell
cd "C:\Users\Paul\Documents\Coding Area\Hackathon\Curo\frontend"
npm run dev
```

Open `http://localhost:5173` in Chrome. Use a private browser window if saved extensions or notifications may appear. Keep only the browser visible during the recording.

### 2. Warm the cache and prepare the browser

Refresh the page once and wait for the console to finish loading. You should see:

- the `curo` wordmark in the top-left pill;
- a `live` pill with `phoenix az` in the top-right;
- a CARTO light map with coloured FortyGuard cells;
- the site callout and its temperature source;
- the decision rail on the right;
- the twelve-hour strip, two-week window, and counters.

The first load can take a few minutes because FortyGuard heatmap jobs are asynchronous. The backend submits a job and polls its status. Do not refresh repeatedly while it is working. The SQLite cache keeps completed requests so later loads are faster and do not repeat the same hourly request.

Set the browser to fullscreen with `F11`. Use 1920 by 1080 if available. The minimum safe size is 1280 by 800. Hide bookmarks and close other applications. Move the mouse to an empty corner before starting the recorder.

### 3. Practise the path once

Do one complete run without recording. Check that the map cells are present, the rail contains actual readings, and the export preview loads. If the page says `api unavailable`, stop and fix the backend or wait for FortyGuard. Do not record an empty or fabricated state.

## The nine-step take

### 1. Open on the finished console

Start the screen recorder, then refresh `http://localhost:5173` once.

Keep the cursor still for three to five seconds while the blur-in entrance completes. The first frame should show the map, the decision rail, the `live` status, and the two impact counters. Let the viewer read the page before moving the cursor.

### 2. Establish the live Phoenix data

Move the cursor slowly to the top-right status pill. Do not click it. Pause over the `live` label and `phoenix az` text, then move to the map timestamp chip.

The map chip should show the current timestamp and its source. The map callout should show the Phoenix site coordinate, a Fahrenheit reading, and `source: api live` or `source: api cached`.

This pause establishes that the heatmap is location-specific and that the number has a provenance label. Do not zoom the map or open another browser tab.

### 3. Select a real map cell

Move the cursor to a coloured polygon in the map and click once. Choose a cell near the middle of the map so the change is easy to see.

After the click, pause for two seconds. The callout should show the selected cell temperature and source. The blue blueprint crosshair marks the selected area. If the selected cell is not obvious, click one neighbouring polygon once and pause again.

Do not claim that the map cell is a different construction site. In this build, the map cell is a hyperlocal reading for the configured Phoenix site.

### 4. Read the pour decision

Move the cursor to the first module in the right-hand decision rail, labelled `site 01 · pour window`. Pause on the coloured status banner.

The banner will say one of the following:

- `safe to pour` for a green model result;
- `window closing` for an amber model result;
- `do not pour` for a red model result.

Read the temperature, signed margin, placement limit, and `source model` label. Then move down to the rule lines. The rule lines show the ACI 305R-20 limit, the temperature source, and the slab-thickness amber-band assumption.

The exact result depends on the live data. Do not wait for or create a particular colour.

### 5. Show the next twelve hours

Move the cursor across the `next 12 hours` strip. Pause first on the current or earliest hour, then on the warmest visible hour.

The strip is labelled `api forecast`. Each hour shows a temperature and time. Green, amber, and red backgrounds match the model classification. A red temperature is a forecast breach, not a measured current value.

Keep the cursor still on the warmest hour for two seconds. The purpose of this pause is to show the moment Curo turns a forecast into a pour decision.

### 6. Show forecast, climatology, and confidence

Move the cursor to the `two week window` module. Point first at the header labels `first 12h forecast` and `then climatology p25 to p75`.

Move slowly over one of the day cells. Each cell shows its day, date, status band, temperature range, confidence, model label, and API source label. Pause on one early cell and one later cell so the viewer can see the confidence value change with the horizon.

This demonstrates that the app does not pretend to have a fourteen-day FortyGuard forecast. The first twelve hours use forecast data. The longer view uses historical percentile data from 2021 onward.

### 7. Show and close the breach alert

If a live forecast hour is red, the breach alert should appear automatically after the page loads. Let it remain visible for four seconds. The headline will say `do not pour at HH:MM` and the panel will show the forecast temperature, limit, and signed margin.

If the alert has already been dismissed, click `open breach alert` in the site status module. If the button is not present, the current live forecast has no red hour. Do not force an alert. Continue the recording with the real green or amber state, or repeat the recording when a real red forecast is available.

To demonstrate the two-way behaviour, click `reschedule pour` only when the red alert is visible and a green hour exists in the same live forecast. The panel closes the breach and opens the green `window reopened at HH:MM` message. Leave it visible for two seconds, then click `dismiss`.

If you do not use rescheduling, click `dismiss` on the red alert. The backdrop click also dismisses it, but the button is clearer in the recording.

### 8. Open the export drawer and download a file

Move the cursor to the dark `export` button in the top-right pill and click it once. The drawer slides in from the right.

Wait for the drawer to load its preview. You should see:

- `curo-pour-plan.csv`;
- `curo-pour-plan.ics`;
- the `csv preview` block;
- source, temperature, status, and margin columns in the CSV text.

Move to the CSV download icon and click once. The browser should download `curo-pour-plan.csv`. Do not open the downloaded file during the recording because that would leave the Curo console.

Close the drawer by clicking `close` in its top-right corner. The cursor should return to the main console. If the preview says the schedule is unavailable, the live export request did not complete. Do not present an empty export as finished.

### 9. End on the impact counters

Move the cursor to the bottom of the decision rail and pause on `cost avoided` and `co2 avoided`.

Hold for five seconds. The values should have finished counting up. Keep the assumption labels visible, including the failed-pour cost, avoided re-pour value, and number of forecast red hours used by the model.

End the recording while the counters, their assumptions, and the export buttons are visible. Stop the recording without adding an end card.

## After the take

Watch the entire recording once before uploading it. Check that the following are readable without sound:

- `live`, `phoenix az`, and a current source label;
- one selected map cell;
- a model status and signed margin;
- the forecast and climatology labels;
- a real breach panel if one was available;
- the CSV preview and download action;
- both counters and their assumption labels.

The video must be silent, 1080p where possible, fullscreen, and free of captions, subtitles, music, notifications, and other windows. Follow the submission form's required duration and file format.

## Troubleshooting during practice

### The page says `api unavailable`

Check that the backend terminal is still running and that `backend/.env` contains the key. Run `verify.py` again. If verification fails, do not record. A provider outage should be shown as an honest error, not hidden with made-up data.

### The first request takes several minutes

This is normal for a new FortyGuard heatmap job. Leave the page open and let the backend poll. Do not start a second backend process. Completed results are cached in SQLite.

### The map has no coloured cells

Run `verify.py`. If current, forecast, and history all pass but the map is empty, refresh once after the backend has finished its request. If it remains empty, stop the recording and inspect the backend response.

### No breach alert appears

This means the current twelve-hour live forecast contains no red hour, or the model request has not completed. Do not invent a breach. Record the real green or amber decision, then record the breach scene later when FortyGuard returns a real red forecast.
