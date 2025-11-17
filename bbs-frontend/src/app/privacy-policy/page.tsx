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
<p className="mb-4">Last updated: Nov 17, 2025</p>

<h2 className="text-xl font-bold mb-2">Introduction</h2>
<p className="mb-4">Block Blast Solver (&quot;we&quot;, &quot;our&quot;, or &quot;us&quot;) operates the web-based tool available at https://blockblastsolverai.com (the &quot;Service&quot;). This Privacy Policy explains our strict no-data-collection practices and your rights regarding our service.</p>

<h2 className="text-xl font-bold mb-2">No Data Collection</h2>
<p className="mb-4">We explicitly state that:</p>
<ul className="list-disc ml-8 mb-4">
<li>We do <strong>not</strong> collect, store, or process any personal information</li>
<li>We do <strong>not</strong> analytics tools to track user behavior.</li>
<li>We do <strong>not</strong> require user accounts or registration</li>
</ul>

<h3 className="text-lg font-bold mb-2">Advertising and Cookies</h3>
<p className="mb-4">We use Google AdSense, a third-party advertising service, to display ads on our website.</p>

<ul className="list-disc ml-8 mb-4">
<li><strong>How AdSense Works:</strong> Google AdSense uses cookies and other tracking technologies to serve ads based on a user's prior visits to our website and other sites on the Internet.</li>
<li><strong>Data Collected by AdSense:</strong> Google uses information from these cookies to display ads that are relevant and engaging to individual users. This data may include non-personally identifiable information such as your browser type, the domain name of your internet service provider, and your general geographic area.</li>
<li><strong>Your Control Over Ads:</strong> You can learn more about how Google uses your data and how you can control the information collected by visiting <a href="https://policies.google.com/technologies/ads">Google's Privacy & Terms page</a>.</li>

<li><strong>Opting Out:</strong> Users may opt out of personalized advertising by visiting <a href="https://adssettings.google.com/">Google's Ads Settings</a>.</li>
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
<p className="mb-4">We use Google AdSense to display advertisements on our Service. As described in the "Advertising and Cookies" section, AdSense is a third-party service that uses cookies to collect information for the purpose of serving relevant ads.</p>
<p>Otherwise, our core service functionality is completely self-contained with no other external trackers or integrations</p>

<h2 className="text-xl font-bold mb-2">Your Rights</h2>
<p className="mb-4">Since we collect no personal data:</p>
<ul className="list-disc ml-8 mb-4">
<li>There is no data to access, rectify, or delete</li>
<li>No data retention policies apply</li>
</ul>
<p>However, for data collected by third-party advertisers like Google AdSense, you must exercise your rights directly with them. Please refer to the "Advertising and Cookies" section for links to manage your ad preferences.</p>

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
