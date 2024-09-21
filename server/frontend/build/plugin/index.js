import vue from '@vitejs/plugin-vue'

/**
 * * плагин unocss, атомарные стили CSS
 * https://github.com/antfu/unocss
 */
import Unocss from 'unocss/vite'

// Плагин для анализа сборки rollup
import visualizer from 'rollup-plugin-visualizer'
// Сжатие
import viteCompression from 'vite-plugin-compression'

import { configHtmlPlugin } from './html'
import unplugin from './unplugin'

export function createVitePlugins(viteEnv, isBuild) {
  const plugins = [vue(), ...unplugin, configHtmlPlugin(viteEnv, isBuild), Unocss()]

  if (viteEnv.VITE_USE_COMPRESS) {
    plugins.push(viteCompression({ algorithm: viteEnv.VITE_COMPRESS_TYPE || 'gzip' }))
  }

  if (isBuild) {
    plugins.push(
      visualizer({
        open: true,
        gzipSize: true,
        brotliSize: true,
      }),
    )
  }

  return plugins
}
