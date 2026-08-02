<script setup>
import { RouterLink } from 'vue-router'
import SocialLinks from '@/components/layout/SocialLinks.vue'

defineProps({
  updatedTime: {
    type: String,
    default: '—',
  },
})
</script>

<template>
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
        <RouterLink :to="{ path: '/', hash: '#journey' }" class="nav-link px-0 py-1">
          -- Journey
        </RouterLink>
        <RouterLink :to="{ path: '/', hash: '#projects' }" class="nav-link px-0 py-1">
          -- Projects
        </RouterLink>
      </nav>
    </div>

    <div class="bottom-area desktop-footer">
      <SocialLinks variant="desktop" />
      <p class="last-updated mt-3 text-secondary small">Last updated: {{ updatedTime }}</p>
    </div>
  </aside>
</template>
