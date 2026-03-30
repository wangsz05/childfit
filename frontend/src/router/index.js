import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/children',
    name: 'Children',
    component: () => import('@/pages/Children.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/plan',
    name: 'Plan',
    component: () => import('@/pages/Plan.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/checkin',
    name: 'CheckIn',
    component: () => import('@/pages/CheckIn.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/achievements',
    name: 'Achievements',
    component: () => import('@/pages/Achievements.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/pages/Profile.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/home')
  } else {
    next()
  }
})

export default router
