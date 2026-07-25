

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path     : '/',
    name     : 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path     : '/courses',
    name     : 'courses',
    component: () => import('../views/CoursesView.vue')
  },
  {
    path     : '/courses/:id',
    name     : 'course-detail',
    component: () => import('../views/CourseDetailView.vue')
  },
  {
    path     : '/profile',
    name     : 'profile',
    component: () => import('../views/ProfileView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard — logs every route change
router.beforeEach((to, from, next) => {
  console.log(`Navigating to: ${to.path}`)
  next()
})

export default router
