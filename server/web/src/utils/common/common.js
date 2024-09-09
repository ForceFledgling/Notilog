import dayjs from 'dayjs'

/**
 * @desc Форматирование времени
 * @param {(Object|string|number)} time
 * @param {string} format
 * @returns {string | null}
 */
export function formatDateTime(time = undefined, format = 'YYYY-MM-DD HH:mm:ss') {
  return dayjs(time).format(format)
}

export function formatDate(date = undefined, format = 'YYYY-MM-DD') {
  return formatDateTime(date, format)
}

/**
 * @desc Функция троттлинга (ограничение частоты вызова)
 * @param {Function} fn
 * @param {Number} wait
 * @returns {Function}
 */
export function throttle(fn, wait) {
  var context, args
  var previous = 0

  return function () {
    var now = +new Date()
    context = this
    args = arguments
    if (now - previous > wait) {
      fn.apply(context, args)
      previous = now
    }
  }
}

/**
 * @desc Функция дебаунса (отложенное выполнение)
 * @param {Function} func
 * @param {number} wait
 * @param {boolean} immediate
 * @return {*}
 */
export function debounce(method, wait, immediate) {
  let timeout
  return function (...args) {
    let context = this
    if (timeout) {
      clearTimeout(timeout)
    }
    // Немедленное выполнение требует двух условий: immediate должно быть true и timeout не должен быть задан или должен быть равен null
    if (immediate) {
      /**
       * Если таймер отсутствует, то выполнить немедленно и установить таймер, который через wait миллисекунд установит таймер в null
       * Это гарантирует, что после немедленного выполнения не будет повторного срабатывания в течение wait миллисекунд
       */
      let callNow = !timeout
      timeout = setTimeout(() => {
        timeout = null
      }, wait)
      if (callNow) {
        method.apply(context, args)
      }
    } else {
      // Если immediate равно false, функция будет выполнена через wait миллисекунд
      timeout = setTimeout(() => {
        /**
         * args - это псевдомассив, поэтому используется fn.apply
         * Также можно написать как method.call(context, ...args)
         */
        method.apply(context, args)
      }, wait)
    }
  }
}
