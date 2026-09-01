# curo

Know the hour a pour will fail, before the concrete arrives.

curo is a concrete pour window planner for FortyGuard Hackathon'26. It combines FortyGuard hyperlocal temperature heatmaps with a transparent ACI 305R-20 placement model. The result is an operational answer for a named site and hour: safe to pour, window closing, or do not pour.

## What is complete

- Live FortyGuard heatmap integration using the documented asynchronous submit and status flow.
- SQLite response cache keyed by the complete provider request. Cached requests are never fetched again.
- Phoenix map with real GeoJSON cells, source labels, timestamp, and CARTO Positron attribution.
- Twelve-hour forecast model using one cached provider request per hour.
- History samples from 2021 onward reduced to a p25 to p75 climatology band.
- ACI 305R-20 placement limit, mass-concrete adjustment, slab-thickness amber band, signed margins, and fired-rule explanations.
- Real-data breach alert with a live green reschedule counterpart.
- CSV and iCalendar exports generated from the same model output.
- Editable site assumptions for failed-pour cost and avoided re-pour CO2.
- Responsive React console with reduced-motion support, keyboard focus states, and honest error and cached-data paths.

## Data and honesty boundary

FortyGuard is the intelligence layer. The backend calls `POST /v1/heatmap`, then polls `GET /v1/status/{activity_id}` until the job completes. The current API returns GeoJSON map cells and area statistics. The app normalises both forms without inventing temperatures. If the provider key is missing, or the response has no readable temperature values, the UI shows the error and no fabricated readings.

The app uses these provenance labels:

- `live`: the current FortyGuard hour
- `forecast`: the next twelve accepted hours
- `history`: historical samples from 2021 onward
- `model`: deterministic ACI output
- `assumption`: editable construction cost and emissions assumptions
- `cached`: a completed provider result served from SQLite after its first fetch

The model uses a 95°F placement limit. Amber begins within 5°F of that limit, tightens by 10°F for mass concrete, and widens to 7°F for slabs over 12 inches. This is an operational screening aid, not an engineering approval.

## Run locally

Requirements: Node 18 or newer, npm 9 or newer, and Python 3.11 or newer.

```powershell
cd backend
python -m venv .venv
\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Set FORTYGUARD_API_KEY in backend/.env
\.venv\Scripts\python verify.py
\.venv\Scripts\python -m uvicorn curo.main:app --reload --port 8000
```

In another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Deploy to Vercel

The repository includes `vercel.json` for Vercel Services. It deploys the Vite frontend and FastAPI backend under one public domain, routing `/` to the frontend and `/api/*` to the backend.

In Vercel, import the `master` branch, keep the project framework set to `Services`, and add `FORTYGUARD_API_KEY` as an environment variable for Production and Preview. Do not commit the key. Curo uses Vercel's writable `/tmp` directory for its temporary SQLite cache.

After deployment, open the public URL in a private window and check that the map, forecast, history, and export preview load before submitting the URL.

## Checks

```powershell
cd backend
\.venv\Scripts\python -m pytest
\.venv\Scripts\python -m compileall curo verify.py

cd ..\frontend
npm run build
```

`verify.py` deliberately fails before the app is considered ready if `FORTYGUARD_API_KEY` is not set or if current, forecast, or historical data cannot be read. No mock or fabricated payload is included in this repository.

## Sources

- [FortyGuard API quickstart](https://docs-api.fortyguard.com/docs/quickstart)
- [FortyGuard Create Heatmap](https://docs-api.fortyguard.com/docs/create-heatmap)
- [FortyGuard known limitations](https://docs-api.fortyguard.com/docs/limitations)
- ACI 305R-20 placement guidance, represented in the model constants and shown as a named source in the console.

## Recording

The recording is silent. Use [RECORDING_GUIDE.md](RECORDING_GUIDE.md) for the complete take sequence. The app itself provides the labels, provenance, breach margin, and export preview.
