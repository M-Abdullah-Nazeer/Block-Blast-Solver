import Link from 'next/link'
import { FC } from 'react'

export const metadata = {
  title: 'Terms & Conditions - Block Blast Solver',
  description: 'Legal terms for using Block Blast Solver - your puzzle optimization tool',
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
  <p className="mb-4">Last updated: Nov 17, 2025</p>



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



  <h2 className="text-xl font-bold mb-2">4. Third-Party Advertising Intellectual Property</h2>
  <p className="mb-4">The Service displays advertisements provided by Google AdSense. The content of these advertisements, including all text, images, and trademarks, is the intellectual property of the respective advertisers and Google LLC. We do not endorse and are not responsible for the intellectual property contained within these third-party advertisements.</p>


  <h2 className="text-xl font-bold mb-2">5. Prohibited Uses</h2>
  <p className="mb-4">You agree not to use the Service to:</p>
  <ul className="list-disc ml-8 mb-4">
    <li>Engage in any activity that interferes with or disrupts the advertisements served on the Service, including but not limited to artificially clicking on ads, using automated systems to generate impressions, or employing ad-blocking tools to circumvent the display of ads.
    </li>
    <li>Use the Service for any illegal purpose or in violation of any local, state, national, or international law.
    </li>
  </ul>


  <h2 className="text-xl font-bold mb-2">6. Limitation of Liability</h2>
  <p className="mb-4">To the fullest extent permitted by law, Block Blast Solver shall not be liable for any indirect, incidental, special, consequential, or punitive damages resulting from your use of the Service. This includes, but is not limited to, any liability arising from:</p>

  <ul className="list-disc ml-8 mb-4">
    <li>The content, accuracy, or availability of third-party advertisements served by Google AdSense.
    </li>
    <li>Any interactions you have with third-party advertisers.
    </li>
    <li>The conduct or omissions of any third-party service providers.
    </li>
  </ul>


  <h2 className="text-xl font-bold mb-2">7. Promotions</h2>
  <p className="mb-4">We currently offer no contests/sweepstakes. Any future promotions will have separate terms.</p>

  <h2 className="text-xl font-bold mb-2">8. Service Modifications and Termination</h2>
  <p className="mb-4">We reserve the right to modify, suspend, or discontinue the Service (or any part of it) at any time, with or without notice.</p>

  <h2 className="text-xl font-bold mb-2">9. Contact</h2>
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
