/** @type {import('next').NextConfig} */




// next.config.mjs

// const securityHeaders = [
//   { key: 'X-Content-Type-Options', value: 'nosniff' },
//   { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
//   { key: 'X-XSS-Protection', value: '1; mode=block' },
// ];

// const nextConfig = {
//   reactStrictMode: true,
//   images: {
//     domains: ["image-to-alt.s3.eu-central-1.amazonaws.com"],
//   },
//   transpilePackages: ['framer-motion'],
//   async headers() {
//     return [{ source: '/:path*', headers: securityHeaders }];
//   },
//   // Remove experimental config if not needed
// };

// export default nextConfig;





// next.config.mjs

import { createRequire } from 'module'
const require = createRequire(import.meta.url)

// load CJS bundle-analyzer via require-shim
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'false',
  openAnalyzer: false, 
})

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  images: {
    domains: ['i.ytimg.com'],
  },
  // transpilePackages: ['framer-motion'],
  experimental: {
    appDir: true,
    fontLoaders: [
      { loader: '@next/font/google', options: { subsets: ['latin'] } }
    ],
  },
}

export default withBundleAnalyzer(nextConfig)








// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   reactStrictMode: true,
//   images: {
//     domains: ["image-to-alt.s3.eu-central-1.amazonaws.com"],
//   },
//   transpilePackages: ['framer-motion'],
//   // Removed experimental flags as they're now stable
// }

// export default nextConfig;