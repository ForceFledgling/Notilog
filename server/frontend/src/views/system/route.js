// const Layout = () => import('@/layout/index.vue')

// export default {
//   name: 'System',
//   path: '/system',
//   component: Layout,
//   redirect: '/system/user',
//   meta: {
//     title: 'Управление системой',
//     icon: 'ph:user-list-bold',
//     order: 5,
//     // role: ['admin'],
//     // requireAuth: true,
//   },
//   children: [
//     {
//       name: 'User',
//       path: 'user',
//       component: () => import('./user/index.vue'),
//       meta: {
//         title: 'Список пользователей',
//         icon: 'mdi:account',
//         keepAlive: true,
//       },
//     },
//     {
//       name: 'Menu',
//       path: 'menu',
//       component: () => import('./menu/index.vue'),
//       meta: {
//         title: 'Список меню',
//         icon: 'ic:twotone-menu-book',
//         keepAlive: true,
//       },
//     },
//   ],
// }
