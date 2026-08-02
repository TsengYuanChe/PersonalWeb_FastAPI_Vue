<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { getAbout } from '@/api/contentApi'
import HomeSidebar from '@/components/layout/HomeSidebar.vue'
import MobileFooter from '@/components/layout/MobileFooter.vue'
import { useHomeViewportMetrics } from '@/composables/useHomeViewportMetrics'
import { useMouseGlow } from '@/composables/useMouseGlow'
import { useScrollProxy } from '@/composables/useScrollProxy'

const route = useRoute()
const isHomeLayout = computed(() => route.meta.layout === 'home')
const updatedTime = ref('—')
const profilePart = ref(null)
const mobileFooter = ref(null)
let hasLoadedUpdatedTime = false

const { updateLayoutVars } = useHomeViewportMetrics({ profilePart, mobileFooter })
useScrollProxy()
useMouseGlow()

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
  await nextTick()
  scrollMainContent()
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
    <div
      class="layout-container text-light min-vh-100"
      :class="isHomeLayout ? 'layout-container--home' : 'layout-container--detail'"
    >
      <HomeSidebar v-if="isHomeLayout" ref="profilePart" :updated-time="updatedTime" />

      <main class="main-content" :class="{ 'detail-main': !isHomeLayout }">
        <RouterView />
      </main>

      <MobileFooter v-if="isHomeLayout" ref="mobileFooter" :updated-time="updatedTime" />
    </div>
  </div>
</template>
