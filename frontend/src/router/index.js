import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import JourneyView from '@/views/JourneyView.vue'
import ProjectView from '@/views/ProjectView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { layout: 'home' } },
  { path: '/about', name: 'about', component: AboutView, meta: { layout: 'detail' } },
  {
    path: '/journey',
    name: 'journey',
    component: JourneyView,
    meta: { layout: 'detail' },
  },
  { path: '/project', name: 'project', component: ProjectView, meta: { layout: 'detail' } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
