<script setup>
import { onMounted, ref } from 'vue'
import { getExperience } from '@/api/contentApi'
import ExperienceCard from '@/components/experience/ExperienceCard.vue'

const experiences = ref([])
const loading = ref(true)
const error = ref('')

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
  <section class="exp-section route-page" aria-labelledby="experience-heading">
    <header class="route-page-header">
      <p class="route-eyebrow">Career & education</p>
      <h1 id="experience-heading" class="fw-bold">Experiences</h1>
      <p class="text-secondary">A detailed view of my professional and academic experience.</p>
    </header>

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
      <ExperienceCard
        v-for="experience in experiences"
        :key="`${experience.location}-${experience.position}-${experience.duration}`"
        :experience="experience"
      />
    </div>
  </section>
</template>
