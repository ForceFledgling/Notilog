<template>
  <!-- Конфигурация Naive UI с использованием темы и её оверрайдов -->
  <n-config-provider
    wh-full
    :locale="ruRU"
    :date-locale="dateRuRU"
    :theme="appStore.isDark ? darkTheme : lightTheme"
    :theme-overrides="appStore.isDark ? darkThemeOverrides : lightThemeOverrides"
  >
    <!-- Провайдеры для глобальных элементов интерфейса -->
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <slot></slot> <!-- Контент приложения -->
            <NaiveProviderContent /> <!-- Включает дополнительную функциональность -->
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup>
import { defineComponent, h } from 'vue'
import {
  ruRU,
  dateRuRU,
  darkTheme,
  lightTheme,
  useLoadingBar,
  useDialog,
  useMessage,
  useNotification
} from 'naive-ui'
import { useCssVar } from '@vueuse/core'
import { kebabCase } from 'lodash-es'
import { setupMessage, setupDialog } from '@/utils'
import { lightThemeOverrides, darkThemeOverrides } from '~/settings'
import { useAppStore } from '@/store'

const appStore = useAppStore()

/**
 * Функция для установки CSS-переменных на основе текущей темы
 */
function setupCssVar() {
  // Определяем оверрайды темы на основе текущего состояния темы (темная или светлая)
  const themeOverrides = appStore.isDark ? darkThemeOverrides : lightThemeOverrides
  const common = themeOverrides.common

  for (const key in common) {
    // Устанавливаем CSS-переменные для каждого цвета
    useCssVar(`--${kebabCase(key)}`, document.documentElement).value = common[key] || ''
    if (key === 'primaryColor') {
      window.localStorage.setItem('__THEME_COLOR__', common[key] || '')
    }
  }
}

/**
 * Функция для настройки глобальных инструментов Naive UI
 */
function setupNaiveTools() {
  window.$loadingBar = useLoadingBar()  // Инициализация глобального индикатора загрузки
  window.$notification = useNotification()  // Инициализация глобальных уведомлений
  window.$message = setupMessage(useMessage())  // Инициализация глобальных сообщений
  window.$dialog = setupDialog(useDialog())     // Инициализация глобальных диалогов
}

/**
 * Внутренний компонент для выполнения настроек при монтировании
 */
const NaiveProviderContent = defineComponent({
  setup() {
    setupCssVar()  // Выполняем настройку CSS-переменных
    setupNaiveTools()  // Инициализируем глобальные инструменты
  },
  render() {
    return h('div')  // Пустой элемент, так как компонент выполняет только настройку
  },
})
</script>
