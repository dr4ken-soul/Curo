import { motion } from 'motion/react'
import { MapContainer, Polygon, TileLayer } from 'react-leaflet'
import type { Cell, Site } from '../../lib/types'
import { FadeBlur } from '../ui/FadeBlur'

type MapCellProps = { site: Site; cells: Cell[]; timestamp?: string; source?: string; selected: Cell | null; onSelect: (cell: Cell) => void; error?: string }

function heatColour(tempF: number): string {
  if (tempF < 80) return 'var(--color-heat-0)'
  if (tempF < 89) return 'var(--color-heat-1)'
  if (tempF < 96) return 'var(--color-heat-2)'
  if (tempF < 103) return 'var(--color-heat-3)'
  if (tempF < 110) return 'var(--color-heat-4)'
  return 'var(--color-heat-5)'
}

function polygonPositions(bounds: number[][]): [number, number][] {
  return bounds.map(([longitude, latitude]) => [latitude, longitude])
}

/** Render the live FortyGuard heatmap and site annotation layer. */
export function MapCell({ site, cells, timestamp, source, selected, onSelect, error }: MapCellProps) {
  const selectedCell = selected || cells[0]
  return <motion.section className="relative col-span-12 min-h-[420px] overflow-hidden rounded-xl border border-line-2 bg-bg-2 lg:col-span-7 lg:min-h-0" initial={{ opacity: 0, filter: 'blur(10px)', scale: 0.98 }} animate={{ opacity: 1, filter: 'blur(0px)', scale: 1 }} transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1], delay: 0.1 }}>
    <MapContainer center={[site.lat, site.lon]} zoom={13} zoomControl={false} attributionControl className="absolute inset-0 z-10">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' />
      {cells.map((cell) => <Polygon key={cell.id} positions={polygonPositions(cell.bounds)} pathOptions={{ color: 'rgba(253, 254, 254, 0.7)', weight: 1, fillColor: heatColour(cell.tempF), fillOpacity: 0.8 }} eventHandlers={{ click: () => onSelect(cell) }} />)}
    </MapContainer>
    <FadeBlur delay={0.45}><div className="absolute left-4 top-4 z-20 max-w-[250px] rounded-lg border border-line-2 bg-elevated/95 p-3 backdrop-blur-sm">
      <p className="font-ui text-sm font-semibold text-ink">site 01 · {site.name}</p>
      <p className="mt-1 font-mono text-[0.6875rem] tabular-nums text-text-3">{Math.abs(site.lat).toFixed(4)} n · {Math.abs(site.lon).toFixed(4)} w</p>
      {selectedCell ? <><p className="mt-2 font-mono text-xl font-medium tabular-nums text-ink">{selectedCell.tempF.toFixed(1)}<span className="text-[0.6875rem] text-text-3">°f</span></p><p className="mt-1 font-mono text-[10px] uppercase tracking-[0.12em] text-text-3">source: api {selectedCell.source}</p></> : <p className="mt-2 font-mono text-[0.6875rem] text-text-3">temperature unavailable</p>}
    </div></FadeBlur>
    {selectedCell && <div className="pointer-events-none absolute left-1/2 top-1/2 z-20 -translate-x-1/2 -translate-y-1/2"><span className="absolute inset-0 -m-3 rounded-full border border-blueprint animate-ring-pulse" aria-hidden="true" /><svg className="h-6 w-6 text-blueprint" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" aria-hidden="true"><circle cx="12" cy="12" r="7" /><path d="M12 3v4M12 17v4M3 12h4M17 12h4" /></svg></div>}
    {error && <div className="absolute inset-0 z-20 flex items-center justify-center bg-bg/50 p-6"><div className="rounded-lg border border-error/30 bg-elevated/95 p-4 text-center backdrop-blur-sm"><p className="font-ui text-sm font-semibold text-ink">heatmap unavailable</p><p className="mt-1 max-w-xs font-mono text-[0.6875rem] text-text-2">{error}</p></div></div>}
    <FadeBlur delay={0.55}><div className="absolute bottom-4 left-4 z-20 flex items-center gap-2 rounded-full border border-line-2 bg-elevated/90 px-3 py-1.5 backdrop-blur-sm"><span className="font-mono text-[10px] text-text-3">cool</span><div className="h-2 w-28 rounded-full" style={{ background: 'linear-gradient(90deg, var(--color-heat-0) 0%, var(--color-heat-1) 20%, var(--color-heat-2) 40%, var(--color-heat-3) 60%, var(--color-heat-4) 80%, var(--color-heat-5) 100%)' }} /><span className="font-mono text-[10px] text-text-3">extreme</span></div></FadeBlur>
    <FadeBlur delay={0.55}><div className="absolute right-4 top-4 z-20 rounded-full border border-line-2 bg-elevated/90 px-3 py-1.5 backdrop-blur-sm"><span className="font-mono text-[0.6875rem] tabular-nums text-text-2">{timestamp || 'waiting for api'} · {source || 'no source'}</span></div></FadeBlur>
  </motion.section>
}
