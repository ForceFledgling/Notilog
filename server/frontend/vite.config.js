import { defineConfig, loadEnv } from 'vite'

import { convertEnv, getSrcPath, getRootPath, getEnvConfig } from './build/utils'
import { viteDefine } from './build/config'
import { createVitePlugins } from './build/plugin'
import { OUTPUT_DIR, PROXY_CONFIG } from './build/constant'

export default defineConfig(({ command, mode }) => {
  const srcPath = getSrcPath()
  const rootPath = getRootPath()
  const isBuild = command === 'build'

  // Загрузка переменных окружения
  const envConfig = getEnvConfig('VITE_', mode);
  const viteEnv = convertEnv(envConfig);
  const { VITE_TITLE, VITE_PORT, VITE_PUBLIC_PATH, VITE_USE_PROXY, VITE_BASE_API } = viteEnv
  
  // Автоматическая обработка всех переменных окружения, начинающихся с VITE_
  const envKeys = Object.entries(viteEnv).reduce((prev, [key, val]) => {
    prev[`import.meta.env.${key}`] = JSON.stringify(val);
    return prev;
  }, {});

  // Вывод всех подгруженных переменных окружения
  console.log('Подгруженные переменные окружения:', viteEnv)

  return {
    base: VITE_PUBLIC_PATH || '/',
    resolve: {
      alias: {
        '~': rootPath,
        '@': srcPath,
      },
    },
    define: {
      ...viteDefine, // сохраняем оригинальные определения
      ...envKeys,    // автоматически добавляем все переменные окружения
    },
    plugins: createVitePlugins(viteEnv, isBuild),
    server: {
      host: '0.0.0.0',
      port: VITE_PORT,
      open: true,
      proxy: VITE_USE_PROXY
        ? {
            [VITE_BASE_API]: PROXY_CONFIG[VITE_BASE_API],
          }
        : undefined,
    },
    build: {
      target: 'es2015',
      outDir: 'dist',
      reportCompressedSize: false,
      chunkSizeWarningLimit: 1024,
    },
  }
})
