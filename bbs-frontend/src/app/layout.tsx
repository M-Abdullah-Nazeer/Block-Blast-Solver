
import { Inter as FontSans } from '@next/font/google'
import { ClientLayout } from './client-layout'
import '@/styles/globals.css'
import { cn } from '@/lib/utils'
import Script from 'next/script'
// import Head from 'next/head'

const fontSans = FontSans({
  subsets: ['latin'],
  variable: '--font-inter',
})

interface RootLayoutProps {
  children: React.ReactNode
}




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


      <link rel="canonical" href="https://blockblastsolverai.com" />

        <link rel="preconnect" href="https://www.googletagmanager.com" />



        {/* GA */}


        <Script
        strategy="afterInteractive"
        src="https://www.googletagmanager.com/gtag/js?id=G-Q65E3ED3L4"
      />
      <Script
        id="google-analytics-config"
        strategy="afterInteractive"
        dangerouslySetInnerHTML={{
          __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-Q65E3ED3L4');
            `,
        }}
      />





        {/* Canonical URL - Good! */}
        {/* <link rel="canonical" href="https://blockblastsolverai.com" /> */}

        {/* SoftwareApplication Schema (Main Focus) */}

        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "SoftwareApplication",
              "name": "Block Blast Solver",
              "url": "https://blockblastsolverai.com",
              "description": "Free AI-powered tool that analyzes Block Blast gameplay screenshots to generate optimal moves with 3D visualization. No downloads required - works directly in your browser.",
              "applicationCategory": ["GameTool", "PuzzleSolver"],
              "operatingSystem": "Web",
              "browserRequirements": "Modern web browser with JavaScript enabled",
              "featureList": [
                "Browser-based (no installations)",
                "AI-powered move suggestions",
                "3D color-coded visualization",
                "Instant screenshot analysis",
                "Free unlimited attempts"
              ],
              "screenshot": {
                "@type": "ImageObject",
                "url": "https://blockblastsolverai.com/og-image.webp",
                "width": 1200,
                "height": 630
              },
              "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "url": "https://blockblastsolverai.com"
              },
              "author": {
                "@type": "Organization",
                "name": "Block Blast Solver AI",
                "url": "https://blockblastsolverai.com"
              },
              "datePublished": "2025-05-18" // Use actual launch date
            })
          }}
        />

        {/*  HowTo Schema (For User Process) */}



        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "HowTo",
              "name": "How to Use Block Blast Solver",
              "description": "3-step process to optimize your Block Blast gameplay",
              // "image": "https://blockblastsolverai.com/process-visual.jpg",
              "totalTime": "PT1M",
              "step": [
                {
                  "@type": "HowToStep",
                  "name": "Upload Screenshot",
                  "text": "Capture and upload your current Block Blast gameplay screen",
                  "image": "https://blockblastsolverai.com/how-to-step-1.webp"
                },
                {
                  "@type": "HowToStep",
                  "name": "Wait for AI Analysis",
                  "text": "Wait until our algorithms process the board state and possible moves",
                },
                {
                  "@type": "HowToStep",
                  "name": "Get Optimal Moves",
                  "text": "Receive color-coded 3D visualization of best placement strategies",
                  "image": "https://blockblastsolverai.com/how-to-step-3.webp"
                }
              ]
            })
          }}
        />



        {/*  Organization Schema (Brand Trust) */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "Organization",
              "name": "Block Blast Solver",
              "url": "https://blockblastsolverai.com",
              "logo": "https://blockblastsolverai.com/block-blast-solver-logo.webp",
              "foundingDate": "2025", // Replace with actual
              "founder": {
                "@type": "Person",
                "name": "Abdullah" // Add if applicable
              },
              "sameAs": [
                "https://www.youtube.com/channel/UCedt5ABWMaOOFqTzjl6jBnw",
                "https://discord.com/users/1373829130042474619",
                "https://github.com/blockblastsolver",
                "https://www.pinterest.com/blockblastsolverai",
              ]
            })
          }}
        />


        {/* WebSite Schema (Simplified) */}


        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "WebSite",
              "name": "Block Blast Solver",
              "url": "https://blockblastsolverai.com",
              "description": "Achieve Block Blast high score just by uploading image. Our AI solver gives detailed solution."
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