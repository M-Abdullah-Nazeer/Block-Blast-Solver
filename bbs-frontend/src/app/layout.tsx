// import { Inter as FontSans } from '@next/font/google'

// import '@/styles/globals.css'
// import { Toaster } from '@/ui/toaster'
// import { Button, buttonVariants } from '@/ui/button'
// import { cn } from '@/lib/utils'
// import { SiteHeader } from '../components/site-header'
// import { TooltipProvider } from '../components/ui/tooltip'
// import { TabProvider } from '../context/TabContext';

// const fontSans = FontSans({
//   subsets: ['latin'],
//   variable: '--font-inter',
// })

// interface RootLayoutProps {
//   children: React.ReactNode
// }

// export default function RootLayout({ children }: RootLayoutProps) {
//   return (
//     <>
//       <html
//         lang="en"
//         className={cn(
//           'dark bg-white font-sans text-slate-900 antialiased',
//           fontSans.variable
//         )}
//       >
//         <body className="min-h-screen bg-white font-sans text-slate-900 antialiased dark:bg-slate-900 dark:text-slate-50">
//         <TabProvider>

//           <Toaster />
//           <SiteHeader />
//           <TooltipProvider>
//             <main>{children}</main>
//             <footer className="flex flex-col items-center justify-center gap-0 mt-12 border-t border-t-slate-200 dark:border-t-slate-700">





// <div className="flex items-center justify-end gap-2">
//   <Button href="#" className={buttonVariants({ variant: 'link', size: 'sm' })}>
//     Terms
//   </Button>
//   <Button href="#" className={buttonVariants({ variant: 'link', size: 'sm' })}>
//     Privacy Policy
//   </Button>
// </div>

// <p className='text-xs leading-7 text-gray-300'>© 2025 Block Blast Solver. All rights reserved.</p>

// </footer>
//           </TooltipProvider>

//           </TabProvider>

//         </body>
//       </html>
//     </>
//   )
// }



import { Inter as FontSans } from '@next/font/google'
import { ClientLayout } from './client-layout'
import '@/styles/globals.css'
import { cn } from '@/lib/utils'
// import Head from 'next/head'

const fontSans = FontSans({
  subsets: ['latin'],
  variable: '--font-inter',
})

interface RootLayoutProps {
  children: React.ReactNode
}


// Website Schema
// const websiteSchema = {
//   "@context": "https://schema.org",
//   "@type": "WebSite",
//   "name": "Block Blast Solver",
//   "url": "https://yourdomain.com",
//   "description": "Your tool description here...",
//   "potentialAction": {
//     "@type": "SearchAction",
//     "target": "{search_term_string}",
//     "query-input": "required name=search_term_string"
//   }
// };



export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html
      lang="en"
      className={cn(
        'dark bg-white font-sans text-slate-900 antialiased',
        fontSans.variable
      )}
    >

      <head>
        {/* Website Schema */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              "name": "Block Blast Solver",
              "url": "https://yourdomain.com",
              "description": "Your tool description here...",
              "potentialAction": {
                "@type": "SearchAction",
                "target": "{search_term_string}",
                "query-input": "required name=search_term_string"
              }
            })
          }}
        />
      </head>

      <body className="min-h-screen bg-white font-sans text-slate-900 antialiased dark:bg-slate-900 dark:text-slate-50">
        <ClientLayout>{children}</ClientLayout>
      </body>
    </html>
  )
}