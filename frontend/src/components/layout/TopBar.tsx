import { FadeBlur } from '../ui/FadeBlur'
import type { Ref } from 'react'

type TopBarProps = { timestamp: string; onExport: () => void; providerReady: boolean; exportRef: Ref<HTMLButtonElement> }

/** Render the sticky split-pill console header. */
export function TopBar({ timestamp, onExport, providerReady, exportRef }: TopBarProps) {
  return <header className="sticky top-0 z-200 px-4 py-3 lg:px-6">
    <div className="flex items-center justify-between gap-3">
      <FadeBlur><div className="glass-light rounded-full px-5 py-2.5"><span className="font-ui text-[1.125rem] font-semibold lowercase tracking-tight text-ink">curo</span></div></FadeBlur>
      <FadeBlur delay={0.08}><div className="glass-light flex items-center gap-1 rounded-full px-2 py-1.5">
        <div className="flex items-center gap-2 px-3 py-1.5"><span className={`h-2 w-2 rounded-full ${providerReady ? 'bg-success animate-pulse-soft' : 'bg-warning'}`} aria-hidden="true" /><span className="font-mono text-sm text-ink">{providerReady ? 'live' : 'offline'}</span><span className="font-mono text-[0.6875rem] text-text-3">phoenix az</span></div>
        <div className="h-4 w-px bg-line-2" aria-hidden="true" />
        <div className="hidden px-3 py-1.5 sm:block"><span className="font-mono text-[0.6875rem] tabular-nums text-text-2">{timestamp}</span></div>
        <div className="h-4 w-px bg-line-2" aria-hidden="true" />
        <button ref={exportRef} onClick={onExport} className="flex min-h-11 items-center gap-2 rounded-full bg-ink px-4 py-2 text-sm font-medium text-elevated transition-colors duration-150 hover:bg-text-2 focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-bg"><DownloadIcon />export</button>
      </div></FadeBlur>
    </div>
  </header>
}

/** Render the shared download glyph. */
export function DownloadIcon() { return <svg className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24" aria-hidden="true"><path strokeLinecap="round" strokeLinejoin="round" d="M12 4v12m0 0l-4-4m4 4l4-4M4 20h16" /></svg> }
