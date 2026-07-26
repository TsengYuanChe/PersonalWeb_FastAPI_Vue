<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { getAbout } from '@/api/contentApi'
import { useMouseGlow } from '@/composables/useMouseGlow'
import { useScrollProxy } from '@/composables/useScrollProxy'

const route = useRoute()
const updatedTime = ref('—')
let hasLoadedUpdatedTime = false

useScrollProxy()
useMouseGlow()

function updateLayoutVars() {
  const header = document.querySelector('.profile-part')
  const footer = document.querySelector('.mobile-footer')

  document.documentElement.style.setProperty('--header-height', `${header?.offsetHeight || 140}px`)
  document.documentElement.style.setProperty('--footer-height', `${footer?.offsetHeight || 80}px`)
  document.documentElement.style.setProperty('--real-vh', `${window.innerHeight}px`)
}

async function loadUpdatedTime() {
  if (hasLoadedUpdatedTime) return

  hasLoadedUpdatedTime = true
  try {
    const response = await getAbout()
    updatedTime.value = response.updatedAt?.split(' ')[0] || '—'
  } catch {
    updatedTime.value = '—'
  }
}

function scrollMainContent() {
  const container = document.querySelector('.main-content')
  if (!container) return

  const target = route.hash ? document.querySelector(route.hash) : null
  const homeTopSpacing = document.querySelector('#about')?.offsetTop || 0
  container.scrollTo({
    top: target ? Math.max(target.offsetTop - homeTopSpacing, 0) : 0,
    behavior: route.hash ? 'smooth' : 'auto',
  })
}

onMounted(async () => {
  updateLayoutVars()
  window.addEventListener('resize', updateLayoutVars)
  await nextTick()
  scrollMainContent()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateLayoutVars)
})

watch(
  () => route.fullPath,
  async () => {
    await nextTick()
    if (route.name === 'home') await loadUpdatedTime()
    scrollMainContent()
    updateLayoutVars()
  },
  { immediate: true },
)
</script>

<template>
  <div class="cursor-glow"></div>
  <div class="app-wrapper">
    <div class="layout-container text-light min-vh-100">
      <aside class="sidebar d-flex flex-column justify-content-between">
        <div class="inner-content profile-part">
          <RouterLink to="/" class="site-title-link">
            <h1 class="display-6 fw-bold">Adam Tseng</h1>
          </RouterLink>
          <h2 class="h5 text-light">Software Engineer</h2>

          <p class="mt-3 text-secondary sidebar-intro">
            Building reliable digital products from concept to deployment.
          </p>

          <nav class="nav flex-column mt-4 nav-menu" aria-label="Primary navigation">
            <RouterLink :to="{ path: '/', hash: '#about' }" class="nav-link px-0 py-1">
              -- Home
            </RouterLink>
            <RouterLink :to="{ path: '/', hash: '#experiences' }" class="nav-link px-0 py-1">
              -- Journey
            </RouterLink>
            <RouterLink :to="{ path: '/', hash: '#projects' }" class="nav-link px-0 py-1">
              -- Projects
            </RouterLink>
          </nav>
        </div>

        <div class="bottom-area desktop-footer">
          <div class="inner-content social-icons d-flex align-items-center mt-5">
            <a
              href="https://github.com/TsengYuanChe"
              target="_blank"
              rel="noopener noreferrer"
              class="text-secondary fs-2"
              data-label="GitHub"
              aria-label="GitHub"
            >
              <i class="bi bi-github"></i>
            </a>
            <a
              href="https://www.linkedin.com/in/adam-tseng-04838b237/"
              target="_blank"
              rel="noopener noreferrer"
              class="text-secondary fs-2"
              data-label="LinkedIn"
              aria-label="LinkedIn"
            >
              <i class="bi bi-linkedin"></i>
            </a>
            <a
              href="https://www.instagram.com/adam0614__/"
              target="_blank"
              rel="noopener noreferrer"
              class="text-secondary fs-2"
              data-label="Instagram"
              aria-label="Instagram"
            >
              <i class="bi bi-instagram"></i>
            </a>
            <a
              href="https://www.facebook.com/profile.php?id=100006659471037"
              target="_blank"
              rel="noopener noreferrer"
              class="text-secondary fs-2"
              data-label="Facebook"
              aria-label="Facebook"
            >
              <i class="bi bi-facebook"></i>
            </a>
            <a
              href="/files/Adam_Tseng_Resume.pdf"
              target="_blank"
              rel="noopener noreferrer"
              class="text-secondary fs-2"
              data-label="Resume"
              aria-label="Resume"
            >
              <i class="bi bi-file-earmark-arrow-down"></i>
            </a>
          </div>
          <p class="last-updated mt-3 text-secondary small">Last updated: {{ updatedTime }}</p>
        </div>
      </aside>

      <main class="main-content">
        <RouterView />
      </main>

      <footer class="bottom-area mobile-footer">
        <div class="inner-content social-icons d-flex align-items-center">
          <a href="https://github.com/TsengYuanChe" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
            <i class="bi bi-github"></i>
          </a>
          <a href="https://www.linkedin.com/in/adam-tseng-04838b237/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
            <i class="bi bi-linkedin"></i>
          </a>
          <a href="https://www.instagram.com/adam0614__/" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
            <i class="bi bi-instagram"></i>
          </a>
          <a href="https://www.facebook.com/profile.php?id=100006659471037" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
            <i class="bi bi-facebook"></i>
          </a>
          <a href="/files/Adam_Tseng_Resume.pdf" target="_blank" rel="noopener noreferrer" aria-label="Resume">
            <i class="bi bi-file-earmark-arrow-down"></i>
          </a>
        </div>
        <p class="last-updated mt-2 mb-0 text-secondary small">
          Last updated: {{ updatedTime }}
        </p>
      </footer>
    </div>
  </div>
</template>
