import { useUserStore } from '@/store'

export function addBaseParams(params) {
  if (!params.userId) {
    params.userId = useUserStore().userId
  }
}

export function resolveResError(code, message) {
  switch (code) {
    case 400:
      message = message ?? 'Ошибка параметров запроса'
      break
    case 401:
      message = message ?? 'Срок действия сессии истек'
      break
    case 403:
      message = message ?? 'Нет прав'
      break
    case 404:
      message = message ?? 'Ресурс или интерфейс не существует'
      break
    case 500:
      message = message ?? 'Ошибка сервера'
      break
    default:
      message = message ?? `【${code}】: Неизвестная ошибка!`
      break
  }
  return message
}
