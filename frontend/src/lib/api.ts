import type { Cell, DayWindow, ModelWindow, Site, ForecastHour } from './types'

const apiRoot = '/api'

function apiUrl(path: string): string {
  return path.startsWith(apiRoot) ? path : `${apiRoot}${path}`
}

/** Fetch JSON from the Curo backend and preserve a useful error message. */
export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(apiUrl(path))
  if (!response.ok) {
    const body = await response.json().catch(() => ({})) as { detail?: { message?: string } | string }
    const detail = typeof body.detail === 'string' ? body.detail : body.detail?.message
    throw new Error(detail || `request failed with ${response.status}`)
  }
  return response.json() as Promise<T>
}

/** Fetch text from the Curo backend for export previews and downloads. */
export async function apiGetText(path: string): Promise<string> {
  const response = await fetch(apiUrl(path))
  if (!response.ok) throw new Error(`export request failed with ${response.status}`)
  return response.text()
}

/** Load the configured construction sites. */
export async function getSites(): Promise<Site[]> {
  const result = await apiGet<{ sites: Site[] }>('/sites')
  return result.sites
}

/** Load current map cells for a site coordinate. */
export async function getCells(site: Site): Promise<{ cells: Cell[]; timestamp: string; source: string }> {
  return apiGet(`/cells?lat=${site.lat}&lon=${site.lon}`)
}

/** Load the next twelve forecast hours. */
export async function getForecast(siteId: string): Promise<{ forecast: ForecastHour[]; source: string }> {
  return apiGet(`/forecast?siteId=${encodeURIComponent(siteId)}`)
}

/** Load the historical percentile window. */
export async function getClimatology(siteId: string): Promise<{ days: DayWindow[]; source: string }> {
  return apiGet(`/climatology?siteId=${encodeURIComponent(siteId)}`)
}

/** Load the ACI model output. */
export async function getWindow(siteId: string): Promise<ModelWindow> {
  return apiGet(`/sites/${encodeURIComponent(siteId)}/window`)
}
