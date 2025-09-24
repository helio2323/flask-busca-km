import path from 'path'

/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:50001/api/v1',
  },
  // Configuração para Docker
  output: 'standalone',
  // Configurações de debug
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
  // Configurações de desenvolvimento
  experimental: {
    serverComponentsExternalPackages: [],
  },
  // Configurações de webpack para debug
  webpack: (config, { dev, isServer }) => {
    if (dev) {
      config.devtool = 'source-map'
    }
    
    // Configuração para resolver módulos - versão 2
    config.resolve = {
      ...config.resolve,
      alias: {
        ...config.resolve.alias,
        '@': path.resolve(process.cwd(), '.'),
        '@/lib': path.resolve(process.cwd(), './lib'),
      },
    }
    
    return config
  },
}

export default nextConfig
