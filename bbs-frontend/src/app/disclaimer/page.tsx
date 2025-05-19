import Link from 'next/link'
import { FC } from 'react'
// import Link from 'next/link'



// app/privacy-policy/page.tsx
// app/disclaimer/page.tsx
export const metadata = {
    title: 'Disclaimer - Block Blast Solver',
    description: 'Important limitations and terms of use for our AI-powered Block Blast puzzle solver - no data collection, client-side processing, and immediate image deletion',
    openGraph: {
      title: 'Service Disclaimer - Block Blast Solver',
      description: 'Understand the terms of using our browser-based Block Blast solution tool with AI-generated suggestions',
      url: 'https://blockblastsolverai.com/disclaimer',
      siteName: 'Block Blast Solver',
      locale: 'en_US',
      type: 'website',
    },
    keywords: [
      'Block Blast disclaimer',
      'game solver terms',
    ],
  }







const page: FC = () => {
  return (






    
    <div className="text-slate-300">
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">




  
  <h1 className="text-2xl font-bold mb-4 text-slate-100">Disclaimer</h1>
  <p className="mb-4">Last updated: May 18, 2025</p>

  <h2 className="text-xl font-bold mb-2">Service Overview</h2>
  <p className="mb-4">
    Block Blast Solver AI ("we", "our", or "us") operates the web-based tool available at<a href="https://blockblastsolverai.com" className="text-blue-400 hover:underline"> https://blockblastsolverai.com</a> (the "Service"). This AI-powered tool analyzes gameplay screenshots to suggest optimal moves.
  </p>

  <h2 className="text-xl font-bold mb-2">Key Disclosures</h2>
  <h3 className="text-lg font-bold mb-2">No Data Collection</h3>
  <ul className="list-disc ml-8 mb-4">
    <li>We do not collect, store, or share personal information</li>
    <li>Uploaded images are deleted immediately after processing</li>
    <li>No user accounts or registration required</li>
  </ul>

  <h3 className="text-lg font-bold mb-2">Advertising Disclosure</h3>
  <p className="mb-4">
    We display third-party advertisements to support service maintenance. These ads may use cookies 
    through their own tracking systems. We have no access to or control over these external tracking 
    technologies.
  </p>

  <h3 className="text-lg font-bold mb-2">Game Disclaimer</h3>
  <p className="mb-4">
    This service is not affiliated with, endorsed by, or sponsored by the official Block Blast game 
    developers. All game assets and trademarks belong to their respective owners.
  </p>

  <h2 className="text-xl font-bold mb-2">Service Limitations</h2>
  <ul className="list-disc ml-8 mb-4">
    <li>Results are AI-generated suggestions, not guaranteed solutions</li>
    <li>Game outcomes may vary based on actual gameplay conditions</li>
    <li>We assume no responsibility for game scores or rankings</li>
  </ul>

  <h2 className="text-xl font-bold mb-2">Technical Disclaimer</h2>
  <p className="mb-4">
    The Service is provided "as is" without warranties of any kind. While we strive for 24/7 availability:
  </p>
  <ul className="list-disc ml-8 mb-4">
    <li>We don't guarantee error-free operation</li>
    <li>Service may be interrupted for maintenance</li>
    <li>Browser compatibility not guaranteed for all devices</li>
  </ul>

  <h2 className="text-xl font-bold mb-2">Contact Information</h2>
  <p className="mb-4">
    For disclaimer-related inquiries: </p>
    <ul className="list-disc ml-8 mb-4">
      <li>Email: admin@blockblastsolverai.com</li>
      <li>
        Contact Form: <Link
            className="underline text-blue-400"
            href="https://blockblastsolverai.com/contact"
          >
            https://blockblastsolverai.com/contact
          </Link>
      </li>
    </ul>
 





      </div>
    </div>
  )
}

export default page
