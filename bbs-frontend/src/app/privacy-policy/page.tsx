import Link from 'next/link'
import { FC } from 'react'
// import Link from 'next/link'



// app/privacy-policy/page.tsx
export const metadata = {
  title: 'Privacy Policy - Block Blast Solver',
  description: 'We collect zero user data. All image processing happens in your browser with immediate deletion. No tracking, no cookies, no data storage.',
  openGraph: {
    title: 'Privacy Policy - Block Blast Solver',
    description: '100% private Block Blast puzzle solver - Your gameplay screenshots never leave your device and are deleted instantly',
    url: 'https://blockblastsolverai.com/privacy-policy',
    siteName: 'Block Blast Solver',
    locale: 'en_US',
    type: 'website',
  },
  keywords: [
    'Block Blast privacy',
    'no data collection',
    'client-side processing',
    'game solver security',
    'browser-only processing'
  ],
}







const page: FC = () => {
  return (
    <div className="text-slate-300">
      <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">


      <h1 className="text-2xl font-bold mb-4 text-slate-100">Privacy Policy</h1>
<p className="mb-4">Last updated: May 17, 2025</p>

<h2 className="text-xl font-bold mb-2">Introduction</h2>
<p className="mb-4">Block Blast Solver (&quot;we&quot;, &quot;our&quot;, or &quot;us&quot;) operates the web-based tool available at https://blockblastsolverai.com (the &quot;Service&quot;). This Privacy Policy explains our strict no-data-collection practices and your rights regarding our service.</p>

<h2 className="text-xl font-bold mb-2">No Data Collection</h2>
<p className="mb-4">We explicitly state that:</p>
<ul className="list-disc ml-8 mb-4">
<li>We do <strong>not</strong> collect, store, or process any personal information</li>
<li>We do <strong>not</strong> use tracking cookies, analytics tools, or third-party scripts</li>
<li>We do <strong>not</strong> require user accounts or registration</li>
</ul>

<h3 className="text-lg font-bold mb-2">Image Processing</h3>
<p className="mb-4">When you upload gameplay screenshots:</p>
<ul className="list-disc ml-8 mb-4">
<li>All processing occurs <strong>directly in your browser</strong></li>
<li>Images are <strong>permanently deleted</strong> immediately after analysis</li>
<li>No images or analysis data ever reach our servers</li>
</ul>

<h2 className="text-xl font-bold mb-2">Technical Information</h2>
<p className="mb-4">Our server may temporarily log basic connection data for security purposes:</p>
<ul className="list-disc ml-8 mb-4">
<li>IP address (anonymized after 24 hours)</li>
<li>Timestamp of access</li>
<li>Browser type/version</li>
</ul>
<p className="mb-4">This data cannot identify individual users and is never combined with other information.</p>

<h2 className="text-xl font-bold mb-2">Third-Party Services</h2>
<p className="mb-4">We use <strong>zero</strong> third-party services that collect user data. Our service is completely self-contained with no external trackers or integrations.</p>

<h2 className="text-xl font-bold mb-2">Your Rights</h2>
<p className="mb-4">Since we collect no personal data:</p>
<ul className="list-disc ml-8 mb-4">
<li>There is no data to access, rectify, or delete</li>
<li>No opt-out mechanisms are required</li>
<li>No data retention policies apply</li>
</ul>

<h2 className="text-xl font-bold mb-2">Children&apos;s Privacy</h2>
<p className="mb-4">Our service contains no age restrictions because we collect no personal data. However, we recommend parental supervision for minors using any online services.</p>

<h2 className="text-xl font-bold mb-2">Policy Changes</h2>
<p className="mb-4">We will notify users of any substantial policy changes through:</p>
<ul className="list-disc ml-8 mb-4">
<li>A prominent notice on our website</li>
<li>The updated &quot;Last updated&quot; date at the top of this policy</li>
</ul>

<h2 className="text-xl font-bold mb-2">Contact Information</h2>
<p className="mb-4">For privacy-related inquiries:</p>
<ul className="list-disc ml-8 mb-4">
<li>Email: admin@blockblastsolverai.com</li>
<li>Contact Page: <Link
            className="underline text-blue-400"
            href="https://blockblastsolverai.com/contact"
          >
            https://blockblastsolverai.com/contact
          </Link>
</li>
</ul>
<p className="mb-4">We respond to all requests within 72 hours.</p>


      </div>
    </div>
  )
}

export default page
