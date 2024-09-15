export const OUTPUT_DIR = 'dist'

export const PROXY_CONFIG = {
  // /**
  //  * @description    Заменить совпадающие значения
  //  * @request_path   http://localhost:3100/api/user
  //  * @redirect_path  http://localhost:9999/api/v1 +/user
  //  */
  // '/api': {
  //   target: 'http://localhost:9999/api/v1',
  //   changeOrigin: true,
  //   rewrite: (path) => path.replace(new RegExp('^/api'), ''),
  // },
  
  /**
   * @description     Не заменять совпадающие значения
   * @request_path    http://localhost:3100/api/v1/user
   * @redirect_path   http://localhost:9999/api/v1/user
   */
  '/api/v1': {
    target: 'http://127.0.0.1:9999',
    changeOrigin: false,
  },
}
