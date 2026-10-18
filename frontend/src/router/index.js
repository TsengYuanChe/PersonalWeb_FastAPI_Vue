import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import JourneyView from '@/views/JourneyView.vue'
import ProjectView from '@/views/ProjectView.vue'
import { trackWebsiteVisit } from '@/services/websiteVisit'

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

// Track website visits after successful navigation
router.afterEach((to, from, failure) => {
  if (failure) return

  // Ignore query-only changes
  if (to.path === from.path) return

  // Exclude admin pages
  if (to.path === '/admin' || to.path.startsWith('/admin/')) return

  // Send tracking request without blocking navigation
  void trackWebsiteVisit(to.path)
})

export default router
