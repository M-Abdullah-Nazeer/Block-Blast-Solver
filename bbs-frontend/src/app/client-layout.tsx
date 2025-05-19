'use client'

import { Toaster } from '@/ui/toaster'
import { SiteHeader } from '../components/site-header'
import { TooltipProvider } from '../components/ui/tooltip'
import { TabProvider } from '../context/TabContext'
import { Button, buttonVariants } from '@/ui/button'

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <TabProvider>
      <Toaster />
      <SiteHeader />
      <TooltipProvider>
        <main>{children}</main>
        <footer className="flex flex-col items-center justify-center gap-0 mt-12 border-t border-t-slate-200 dark:border-t-slate-700">
          <div className="flex items-center justify-end gap-2">
            <Button href="terms" className={buttonVariants({ variant: 'link', size: 'sm' })}>
              Terms
            </Button>
            <Button href="privacy-policy" className={buttonVariants({ variant: 'link', size: 'sm' })}>
              Privacy Policy
            </Button>
            <Button href="disclaimer" className={buttonVariants({ variant: 'link', size: 'sm' })}>
              Disclaimer
            </Button>
            <Button href="contact" className={buttonVariants({ variant: 'link', size: 'sm' })}>
              Contact
            </Button>
          </div>
          <p className='text-xs leading-7 text-gray-300'>© 2025 Block Blast Solver. All rights reserved.</p>
        </footer>
      </TooltipProvider>
    </TabProvider>
  )
}