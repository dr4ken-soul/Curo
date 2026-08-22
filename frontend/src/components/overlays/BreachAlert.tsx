import { AnimatePresence, motion } from 'motion/react'
import { useEffect, useRef } from 'react'
import type { ForecastHour } from '../../lib/types'

type BreachAlertProps = { alertHour: ForecastHour | null; reopenedHour?: ForecastHour | null; onDismiss: () => void; onReschedule: () => void }

/** Render the red breach alert or its live green reschedule counterpart. */
export function BreachAlert({ alertHour, reopenedHour, onDismiss, onReschedule }: BreachAlertProps) {
  const actionRef = useRef<HTMLButtonElement>(null)
  const open = Boolean(alertHour || reopenedHour)
  useEffect(() => { if (open) actionRef.current?.focus() }, [open])
  useEffect(() => { const handler = (event: KeyboardEvent) => { if (event.key === 'Escape' && open) onDismiss() }; window.addEventListener('keydown', handler); return () => window.removeEventListener('keydown', handler) }, [open, onDismiss])
  const reopened = Boolean(reopenedHour)
  const hour = alertHour || reopenedHour
  return <AnimatePresence>{open && hour && <><motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.15, ease: 'easeOut' }} className="fixed inset-0 z-300 bg-ink/50 backdrop-blur-sm" onClick={onDismiss} /><motion.div role="alertdialog" aria-modal="true" aria-labelledby="breach-title" initial={{ opacity: 0, scale: 0.96, y: 8, filter: 'blur(8px)' }} animate={{ opacity: 1, scale: 1, y: 0, filter: 'blur(0px)' }} exit={{ opacity: 0, scale: 0.97, y: 6, filter: 'blur(4px)' }} transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }} className="fixed inset-x-0 top-1/2 z-400 mx-auto w-full max-w-md -translate-y-1/2 p-4"><div className={`rounded-xl border bg-elevated p-6 shadow-[0_16px_48px_rgba(20,24,29,0.18)] ${reopened ? 'border-success/30' : 'border-error/30'}`}><p className={`font-mono text-[0.6875rem] font-medium uppercase tracking-[0.12em] ${reopened ? 'text-success' : 'text-error'}`}>{reopened ? 'window reopened · pour site 01' : 'breach · pour site 01'}</p><h2 id="breach-title" className="mt-2 font-ui text-2xl font-bold text-ink">{reopened ? `window reopened at ${hour.hour}` : `do not pour at ${hour.hour}`}</h2><p className="mt-2 font-mono text-sm tabular-nums text-text-2">{reopened ? `forecast ${hour.tempF.toFixed(1)}°f · limit restored · margin ${hour.marginF?.toFixed(1)}°f` : `forecast ${hour.tempF.toFixed(1)}°f · limit 95°f · margin ${hour.marginF?.toFixed(1)}°f`}</p><div className="mt-6 flex items-center justify-end gap-3"><button onClick={onDismiss} className="rounded-full px-3 py-2 text-sm font-medium text-text-2 transition-colors hover:text-ink focus-visible:ring-2 focus-visible:ring-accent">dismiss</button>{!reopened && <button ref={actionRef} onClick={onReschedule} className="rounded-full bg-ink px-5 py-2.5 text-sm font-medium text-elevated transition-colors hover:bg-text-2 focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-elevated">reschedule pour</button>}</div></div></motion.div></>}</AnimatePresence>
}

