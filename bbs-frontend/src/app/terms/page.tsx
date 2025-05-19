import Link from 'next/link'
import { FC } from 'react'

export const metadata = {
  title: 'Terms & Conditions - Block Blast Solver',
  description: 'Legal terms for using Block Blast Solver - your AI-powered puzzle optimization tool',
  openGraph: {
    title: 'Terms & Conditions - Block Blast Solver',
    description: 'Web-based tool for solving Block Blast puzzles via screenshot analysis',
    url: 'https://blockblastsolverai.com/terms',
    siteName: 'Block Blast Solver',
    locale: 'en_US',
    type: 'website',
  },
}


const page: FC = () => {
  return (
    <div className="text-slate-300">


      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
     

      <div className="text-slate-300">
  <h1 className="text-2xl font-bold mb-4 text-slate-100">Terms & Conditions</h1>
  <p className="mb-4">Last updated: May 18, 2025</p>



  <h2 className="text-xl font-bold mb-2">1. Account & Content</h2>
  <ul className="list-disc ml-8 mb-4">
    <li><strong>No user accounts:</strong> Service requires no registration</li>
    <li><strong>No content storage:</strong> Uploaded screenshots are immediately deleted after processing</li>
  </ul>

  <h2 className="text-xl font-bold mb-2">2. Commercial Terms</h2>
  <ul className="list-disc ml-8 mb-4">
    <li><strong>No purchases:</strong> This is a free service</li>
    <li><strong>No subscriptions:</strong> No recurring payment plans</li>
  </ul>

  <h2 className="text-xl font-bold mb-2">3. Intellectual Property</h2>
  <ul className="list-disc ml-8 mb-4">
    <li>Block Blast Solver retains all rights to:
      <ul className="list-circle ml-6">
        <li>Logo and visual design</li>
        <li>Algorithm implementations</li>
        <li>3D visualization systems</li>
      </ul>
    </li>
    <li>User feedback becomes our property:
      <ul className="list-circle ml-6">
        <li>We may implement suggestions without compensation</li>
        <li>No obligation to acknowledge contributors</li>
      </ul>
    </li>
  </ul>

  <h2 className="text-xl font-bold mb-2">4. Promotions</h2>
  <p className="mb-4">We currently offer no contests/sweepstakes. Any future promotions will have separate terms.</p>

  <h2 className="text-xl font-bold mb-2">5. Contact</h2>
  <p className="mb-4">For terms inquiries:</p>
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
    </div>
  )
}

export default page
