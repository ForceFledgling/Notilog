import { defineConfig, loadEnv } from 'vite'

import { convertEnv, getSrcPath, getRootPath } from './build/utils'
import { viteDefine } from './build/config'
import { createVitePlugins } from './build/plugin'
import { OUTPUT_DIR, PROXY_CONFIG } from './build/constant'

// Логгирование переменных окружения
function logEnv(viteEnv) {
  console.log('Loaded environment variables:')
  Object.keys(viteEnv).forEach(key => {
    console.log(`${key}: ${viteEnv[key]}`)
  })
}

// Middleware для логгирования запросов прокси
function logProxyRequests(proxyOptions) {
  return (req, res, next) => {
    console.log(`[Proxy] ${req.method} ${req.url} -> ${proxyOptions.target}${req.url}`)
    next()
  }
}

export default defineConfig(({ command, mode }) => {
  const srcPath = getSrcPath()
  const rootPath = getRootPath()
  const isBuild = command === 'build'

  const env = loadEnv(mode, process.cwd())
  const viteEnv = convertEnv(env)
  const { VITE_PORT, VITE_PUBLIC_PATH, VITE_USE_PROXY, VITE_BASE_API } = viteEnv

  // Логгирование переменных окружения
  logEnv(viteEnv)

  return {
    base: VITE_PUBLIC_PATH || '/',
    resolve: {
      alias: {
        '~': rootPath,
        '@': srcPath,
      },
    },
    define: viteDefine,
    plugins: createVitePlugins(viteEnv, isBuild),
    server: {
      host: '0.0.0.0',
      port: VITE_PORT,
      open: true,
      proxy: VITE_USE_PROXY
        ? {
            [VITE_BASE_API]: {
              ...PROXY_CONFIG[VITE_BASE_API],
              configure: (proxy, options) => {
                // Логгирование запросов прокси
                proxy.on('proxyReq', (proxyReq, req, res) => {
                  console.log(`[Proxy] ${req.method} ${req.url} -> ${options.target}${req.url}`)
                })
              }
            }
          }
        : undefined,
    },
    build: {
      target: 'es2015',
      outDir: OUTPUT_DIR || 'dist',
      reportCompressedSize: false, // Включить/выключить отчет о размере сжатия gzip
      chunkSizeWarningLimit: 1024, // Ограничение предупреждения о размере chunk (в единицах kb)
    },
  }
})
