import { createI18n } from 'vue-i18n'
import { lStorage } from '@/utils'

import messages from './messages'

const currentLocale = lStorage.get('locale')

const i18n = createI18n({
  legacy: false,  // Используем Composition API
  globalInjection: true,
  locale: 'ru',  // Язык по умолчанию
  fallbackLocale: 'en',  // Запасной язык
  messages: messages,
})

export default i18n
