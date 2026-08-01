<script setup>
import { onMounted, ref } from 'vue'
import { getExperience } from '@/api/contentApi'
import JourneyCard from '@/components/experience/JourneyCard.vue'
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'

const experiences = ref([])
const loading = ref(true)
const error = ref('')
const expandedExperienceSlug = ref(null)

function toggleExperience(slug) {
  expandedExperienceSlug.value = expandedExperienceSlug.value === slug ? null : slug
}

onMounted(async () => {
  try {
    const response = await getExperience()
    experiences.value = Array.isArray(response.content?.experience)
      ? response.content.experience
      : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load experiences.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section
    class="exp-section route-page detail-page-container"
    aria-labelledby="experience-heading"
  >
    <DetailPageHeader
      current="JOURNEY"
      heading-id="experience-heading"
      title="Journey"
      description="A detailed view of my professional and academic experience."
    />

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading experiences…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>Experiences could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="experiences.length === 0" class="page-state">
      No experience entries are available yet.
    </div>

    <div v-else>
      <JourneyCard
        v-for="experience in experiences"
        :key="experience.slug"
        :experience="experience"
        :expanded="expandedExperienceSlug === experience.slug"
        @toggle="toggleExperience"
      />
    </div>
  </section>
</template>
