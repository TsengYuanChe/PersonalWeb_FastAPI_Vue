<script setup>
import { onMounted, ref } from 'vue'
import { getAbout } from '@/api/contentApi'

const paragraphs = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await getAbout()
    paragraphs.value = Array.isArray(response.content?.paragraphs)
      ? response.content.paragraphs
      : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load profile.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section class="about-section route-page" aria-labelledby="about-heading">
    <header class="route-page-header">
      <p class="route-eyebrow">Profile</p>
      <h1 id="about-heading" class="fw-bold">About me</h1>
      <p class="text-secondary">My engineering background, current work, and technical focus.</p>
    </header>

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading profile…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>Profile could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="paragraphs.length === 0" class="page-state">
      Profile information is not available yet.
    </div>

    <div v-else class="about-text about-detail-text">
      <p
        v-for="(paragraph, index) in paragraphs"
        :key="index"
        class="text-secondary mb-3"
      >
        <span v-html="paragraph"></span>
      </p>
    </div>
  </section>
</template>
