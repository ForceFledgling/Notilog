import { defineStore } from 'pinia'
import { basicRoutes, vueModules } from '@/router/routes'
import Layout from '@/layout/index.vue'
import api from '@/api'

// * Функции для работы с маршрутами от бэкэнда
// Создание фронтенд-маршрутов на основе данных от бэкэнда
function buildRoutes(routes = []) {
  return routes.map((e) => ({
    name: e.name,
    path: e.path, // Обработка случаев, когда каталог является основным меню
    component: shallowRef(Layout), // ? Использование shallowRef для предотвращения предупреждений в консоли
    isHidden: e.is_hidden,
    redirect: e.redirect,
    meta: {
      title: e.name,
      icon: e.icon,
      order: e.order,
      keepAlive: e.keepalive,
    },
    children: e.children.map((e_child) => ({
      name: e_child.name,
      path: e_child.path, // Родительский путь + текущий путь меню
      // ! Динамическая загрузка модулей маршрутов
      component: vueModules[`/src/views${e_child.component}/index.vue`],
      isHidden: e_child.is_hidden,
      meta: {
        title: e_child.name,
        icon: e_child.icon,
        order: e_child.order,
        keepAlive: e_child.keepalive,
      },
    })),
  }))
}

export const usePermissionStore = defineStore('permission', {
  state() {
    return {
      accessRoutes: [],
      accessApis: [],
    }
  },
  getters: {
    routes() {
      return basicRoutes.concat(this.accessRoutes)
    },
    menus() {
      return this.routes.filter((route) => route.name && !route.isHidden)
    },
    apis() {
      return this.accessApis
    },
  },
  actions: {
    async generateRoutes() {
      const res = await api.getUserMenu() // Вызов API для получения маршрутов меню от бэкэнда
      this.accessRoutes = buildRoutes(res.data) // Преобразование в формат фронтенд-маршрутов
      return this.accessRoutes
    },
    async getAccessApis() {
      const res = await api.getUserApi()
      this.accessApis = res.data
      return this.accessApis
    },
    resetPermission() {
      this.$reset()
    },
  },
})
