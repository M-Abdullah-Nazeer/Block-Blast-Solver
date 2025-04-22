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









const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ["image-to-alt.s3.eu-central-1.amazonaws.com"],
  },
  transpilePackages: ['framer-motion'],
  experimental: {
    // Only include if you actually need these
    appDir: true,
    fontLoaders: [
      { loader: "@next/font/google", options: { subsets: ["latin"] } }
    ],
  }
}

export default nextConfig;







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