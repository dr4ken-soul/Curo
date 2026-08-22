import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { getCells, getClimatology, getForecast, getSites, getWindow, apiGetText } from './lib/api'
import type { Cell, DayWindow, ForecastHour, ModelWindow, Site } from './lib/types'
import { TopBar } from './components/layout/TopBar'
import { MapCell } from './components/console/MapCell'
import { DecisionRail } from './components/console/DecisionRail'
import { BreachAlert } from './components/overlays/BreachAlert'
import { ExportDrawer } from './components/overlays/ExportDrawer'
import { GrainOverlay } from './components/ui/GrainOverlay'

function dateStamp(): string { return new Intl.DateTimeFormat('en-GB', { hour: '2-digit', minute: '2-digit', hour12: false, timeZoneName: 'short' }).format(new Date()).toLowerCase() }

/** Trigger a browser download from a fetched export response. */
async function downloadExport(path: string, filename: string): Promise<void> { const response = await fetch(path); if (!response.ok) throw new Error(`download failed with ${response.status}`); const blob = await response.blob(); const url = URL.createObjectURL(blob); const link = document.createElement('a'); link.href = url; link.download = filename; link.click(); URL.revokeObjectURL(url) }

/** Render the complete Curo console and coordinate live data loading. */
export default function App() {
  const [site, setSite] = useState<Site | null>(null)
  const [cells, setCells] = useState<Cell[]>([])
  const [selected, setSelected] = useState<Cell | null>(null)
  const [forecast, setForecast] = useState<ForecastHour[]>([])
  const [days, setDays] = useState<DayWindow[]>([])
  const [model, setModel] = useState<ModelWindow | null>(null)
  const [errors, setErrors] = useState<string[]>([])
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [alertHour, setAlertHour] = useState<ForecastHour | null>(null)
  const [reopenedHour, setReopenedHour] = useState<ForecastHour | null>(null)
  const [csvPreview, setCsvPreview] = useState('')
  const [exportError, setExportError] = useState('')
  const exportRef = useRef<HTMLButtonElement>(null)
  const [timestamp, setTimestamp] = useState(dateStamp())

  const loadData = useCallback(async () => {
    setErrors([])
    try {
      const sites = await getSites()
      const currentSite = sites[0]
      if (!currentSite) throw new Error('no construction site configured')
      setSite(currentSite)
      const results = await Promise.allSettled([getCells(currentSite), getForecast(currentSite.id), getClimatology(currentSite.id), getWindow(currentSite.id)])
      const nextErrors: string[] = []
      const cellsResult = results[0]; if (cellsResult.status === 'fulfilled') { setCells(cellsResult.value.cells); setSelected(cellsResult.value.cells[0] || null) } else nextErrors.push(cellsResult.reason instanceof Error ? cellsResult.reason.message : 'map data request failed')
      const forecastResult = results[1]; if (forecastResult.status === 'fulfilled') setForecast(forecastResult.value.forecast); else nextErrors.push(forecastResult.reason instanceof Error ? forecastResult.reason.message : 'forecast request failed')
      const daysResult = results[2]; if (daysResult.status === 'fulfilled') setDays(daysResult.value.days); else nextErrors.push(daysResult.reason instanceof Error ? daysResult.reason.message : 'history request failed')
      const modelResult = results[3]; if (modelResult.status === 'fulfilled') { setModel(modelResult.value); setForecast(modelResult.value.hours); const breach = modelResult.value.hours.find((hour) => hour.status === 'red'); if (breach) setAlertHour(breach) } else nextErrors.push(modelResult.reason instanceof Error ? modelResult.reason.message : 'model request failed')
      setErrors([...new Set(nextErrors)])
    } catch (error) { setErrors([error instanceof Error ? error.message : 'api request failed']) }
  }, [])

  useEffect(() => { void loadData(); const interval = window.setInterval(() => setTimestamp(dateStamp()), 60000); return () => window.clearInterval(interval) }, [loadData])

  const csvPath = site ? `/api/export.csv?siteId=${encodeURIComponent(site.id)}` : ''
  const icsPath = site ? `/api/export.ics?siteId=${encodeURIComponent(site.id)}` : ''
  const preview = useCallback(async () => { if (!csvPath) return; try { setCsvPreview(await apiGetText(csvPath)); setExportError('') } catch (error) { setExportError(error instanceof Error ? error.message : 'export preview unavailable') } }, [csvPath])
  const openDrawer = useCallback(() => { setDrawerOpen(true); void preview() }, [preview])
  const closeDrawer = useCallback(() => { setDrawerOpen(false); window.setTimeout(() => exportRef.current?.focus(), 160) }, [])
  const triggerDownload = useCallback(async (path: string, filename: string) => { try { await downloadExport(path, filename); setExportError('') } catch (error) { setExportError(error instanceof Error ? error.message : 'download unavailable') } }, [])
  const reschedule = useCallback(() => { const nextGreen = model?.hours.find((hour) => hour.status === 'green') || null; setAlertHour(null); setReopenedHour(nextGreen) }, [model])
  const clearAlert = useCallback(() => { setAlertHour(null); setReopenedHour(null) }, [])
  const action = useMemo(() => site ? { csv: () => void triggerDownload(csvPath, 'curo-pour-plan.csv'), ics: () => void triggerDownload(icsPath, 'curo-pour-plan.ics') } : { csv: () => undefined, ics: () => undefined }, [csvPath, icsPath, site, triggerDownload])
  return <div className="relative min-h-screen overflow-hidden bg-bg"><div className="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true"><div className="absolute -left-24 -top-24 h-[420px] w-[520px] rounded-full bg-blueprint blur-[140px] animate-breathe-a" /><div className="absolute -bottom-32 -right-20 h-[440px] w-[560px] rounded-full bg-accent blur-[150px] animate-breathe-b" /></div><TopBar timestamp={timestamp} onExport={openDrawer} providerReady={errors.length === 0 && Boolean(site)} exportRef={exportRef} /><main className="relative z-0 grid grid-cols-12 gap-4 px-4 pb-4 lg:min-h-[calc(100vh-76px)] lg:px-6"><div className="col-span-12 grid min-h-0 grid-cols-12 gap-4 lg:col-span-12"><MapCell site={site || { id: 'site-01', name: 'downtown Phoenix', lat: 33.4484, lon: -112.074, thickness: 8, mass: false, pour_cost: 12000, re_pour_co2: 0.9 }} cells={cells} selected={selected} onSelect={setSelected} error={errors[0]} timestamp={cells.length ? timestamp : undefined} source={cells[0]?.source} /><DecisionRail site={site || { id: 'site-01', name: 'downtown Phoenix', lat: 33.4484, lon: -112.074, thickness: 8, mass: false, pour_cost: 12000, re_pour_co2: 0.9 }} forecast={forecast} days={days} model={model} errors={errors} onExportCsv={openDrawer} onExportIcs={openDrawer} onRetry={() => void loadData()} onAlert={() => { const breach = model?.hours.find((hour) => hour.status === 'red'); if (breach) setAlertHour(breach) }} /></div></main><BreachAlert alertHour={alertHour} reopenedHour={reopenedHour} onDismiss={clearAlert} onReschedule={reschedule} /><ExportDrawer open={drawerOpen} csvPreview={csvPreview} error={exportError} onClose={closeDrawer} onDownloadCsv={action.csv} onDownloadIcs={action.ics} /><GrainOverlay /></div>
}

