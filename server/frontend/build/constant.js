export const OUTPUT_DIR = 'dist'

export const PROXY_CONFIG = {
  '/api/v1': {
    target: 'http://localhost:9999',
    changeOrigin: true,
  },
}
