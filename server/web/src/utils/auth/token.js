import { lStorage } from '@/utils'

const TOKEN_CODE = 'access_token'

export function getToken() {
  return lStorage.get(TOKEN_CODE)
}

export function setToken(token) {
  lStorage.set(TOKEN_CODE, token)
}

export function removeToken() {
  lStorage.remove(TOKEN_CODE)
}

// export async function refreshAccessToken() {
//   const tokenItem = lStorage.getItem(TOKEN_CODE)
//   if (!tokenItem) {
//     return
//   }
//   const { time } = tokenItem
//   // Не выполнять обновление токена в течение 30 минут после его создания или обновления
//   if (new Date().getTime() - time <= 1000 * 60 * 30) return
//   try {
//     const res = await api.refreshToken()
//     setToken(res.data.token)
//   } catch (error) {
//     console.error(error)
//   }
// }
