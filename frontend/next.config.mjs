/** @type {import('next').NextConfig} */
const nextConfig = {
  // Google Identity Services requires the public OAuth client ID in the browser.
  // Support the existing local variable while standardising on NEXT_PUBLIC_*. Never
  // expose a Google client secret here.
  env: {
    NEXT_PUBLIC_GOOGLE_CLIENT_ID:
      process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || process.env.GOOGLE_CLIENT_ID,
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
      },
      {
        protocol: "https",
        hostname: "res.cloudinary.com",
      },
      {
        protocol: "https",
        hostname: "plus.unsplash.com",
      },
    ],
  },
};

export default nextConfig;
