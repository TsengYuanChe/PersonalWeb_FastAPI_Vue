<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { getAbout } from '@/api/contentApi'
import HomeSidebar from '@/components/layout/HomeSidebar.vue'
import MobileFooter from '@/components/layout/MobileFooter.vue'
import { useHomeSectionNavigation } from '@/composables/shell/useHomeSectionNavigation'
import { useHomeViewportMetrics } from '@/composables/shell/useHomeViewportMetrics'
import { useMouseGlow } from '@/composables/shell/useMouseGlow'
import { useScrollProxy } from '@/composables/shell/useScrollProxy'

const route = useRoute()
const isHomeLayout = computed(() => route.meta.layout === 'home')
const scrollProxyEnabled = computed(() => isHomeLayout.value)
const updatedTime = ref('—')
const profilePart = ref(null)
const mobileFooter = ref(null)
const mainContent = ref(null)
let hasLoadedUpdatedTime = false

const { scrollToCurrentSection } = useHomeSectionNavigation({ route, mainContent })
const { updateLayoutVars } = useHomeViewportMetrics({ profilePart, mobileFooter })
useScrollProxy({ container: mainContent, enabled: scrollProxyEnabled })
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

onMounted(async () => {
  await nextTick()
  scrollToCurrentSection()
})

watch(
  () => route.fullPath,
  async () => {
    await nextTick()
    if (route.name === 'home') await loadUpdatedTime()
    scrollToCurrentSection()
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

      <main ref="mainContent" class="main-content" :class="{ 'detail-main': !isHomeLayout }">
        <RouterView />
      </main>

      <MobileFooter v-if="isHomeLayout" ref="mobileFooter" :updated-time="updatedTime" />
    </div>
  </div>
</template>
