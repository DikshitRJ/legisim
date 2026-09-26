/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    // Inside Docker, the backend service is named 'fastapi-backend'.
    // In local dev, fall back to localhost:8000.
    const backendUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://fastapi-backend:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
