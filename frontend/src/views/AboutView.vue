<script setup>
import { onMounted, ref } from 'vue'
import { getAbout } from '@/api/contentApi'
import AboutSection from '@/components/about/AboutSection.vue'
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'

const sections = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await getAbout()
    sections.value = Array.isArray(response.content?.sections) ? response.content.sections : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load about content.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <article
    class="about-page route-page detail-page-container"
    aria-labelledby="about-heading"
  >
    <DetailPageHeader
      current="ABOUT"
      heading-id="about-heading"
      title="About Me"
      description="A closer look at my background, engineering approach, and the work I care about."
    />

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading about content…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>About content could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="sections.length === 0" class="page-state">
      No about sections are available yet.
    </div>

    <div v-else class="about-page-sections">
      <AboutSection v-for="section in sections" :key="section.id" :section="section" />
    </div>
  </article>
</template>
