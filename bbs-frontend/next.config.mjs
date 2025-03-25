/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    appDir: true,
    fontLoaders: [
      {
        loader: "@next/font/google",
        options: { subsets: ["latin"] },
      },
    ],
  },
  images: {
    domains: ["image-to-alt.s3.eu-central-1.amazonaws.com"],
  },
  transpilePackages: ['framer-motion'],
}

export default nextConfig


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