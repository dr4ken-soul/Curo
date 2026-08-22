import { motion } from 'motion/react'
import type { ReactNode } from 'react'

type FadeBlurProps = { children: ReactNode; delay?: number; className?: string }

/** Apply Curo's standard blur-in entrance to a content block. */
export function FadeBlur({ children, delay = 0, className }: FadeBlurProps) {
  return <motion.div className={className} initial={{ opacity: 0, filter: 'blur(8px)', y: 16 }} animate={{ opacity: 1, filter: 'blur(0px)', y: 0 }} transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1], delay }}>{children}</motion.div>
}

