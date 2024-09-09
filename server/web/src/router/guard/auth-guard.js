import { getToken, isNullOrWhitespace } from '@/utils'

const WHITE_LIST = ['/login', '/404']
export function createAuthGuard(router) {
  router.beforeEach(async (to) => {
    const token = getToken()

    /** Случай, когда нет токена */
    if (isNullOrWhitespace(token)) {
      if (WHITE_LIST.includes(to.path)) return true
      return { path: 'login', query: { ...to.query, redirect: to.path } }
    }

    /** Случай, когда есть токен */
    if (to.path === '/login') return { path: '/' }
    return true
  })
}
