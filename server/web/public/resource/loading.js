/**
 * Инициализация SVG логотипа с эффектом загрузки
 * @param {string} id - id элемента
 */
function initSvgLogo(id) {
  const svgStr = `<svg viewBox="0 0 24 24" fill="#000000" xmlns="http://www.w3.org/2000/svg">
  <path d="M 4 18.944 L 5.995 22.4 L 18.005 22.4 L 20 18.944 L 4 18.944 Z M 24 12 L 21.987 15.488 L 9.216 15.488 L 21.987 8.512 L 24 12 Z M 0 12 L 2.013 8.512 L 14.784 8.512 L 2.013 15.488 L 0 12 Z M 4 5.056 L 5.995 1.6 L 18.005 1.6 L 20 5.056 L 4 5.056 Z" style="transform-origin: 12px 12px;" transform="matrix(0, 1, -1, 0, 3.57628e-7, 3.57628e-7)"/>
</svg>`
  const appEl = document.querySelector(id)
  const div = document.createElement('div')
  div.innerHTML = svgStr
  if (appEl) {
    appEl.appendChild(div)
  }
}

function addThemeColorCssVars() {
  const key = '__THEME_COLOR__'
  // const defaultColor = '#F4511E'
  const defaultColor = '#FFFFFF'
  const themeColor = window.localStorage.getItem(key) || defaultColor
  const cssVars = `--primary-color: ${themeColor}`
  document.documentElement.style.cssText = cssVars
}

addThemeColorCssVars()

initSvgLogo('#loadingLogo')
