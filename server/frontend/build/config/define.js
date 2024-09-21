import dayjs from 'dayjs'

/**
 * * Здесь определены глобальные константы, которые будут добавлены в window после запуска или сборки
 * https://vitejs.cn/config/#define
 */

// Время сборки проекта
const _BUILD_TIME_ = JSON.stringify(dayjs().format('YYYY-MM-DD HH:mm:ss'))

export const viteDefine = {
  _BUILD_TIME_,
}
