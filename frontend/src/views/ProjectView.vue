<script setup>
import { onMounted, ref } from 'vue'
import { getProjects } from '@/api/contentApi'
import ProjectCard from '@/components/projects/ProjectCard.vue'
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'

const projects = ref([])
const loading = ref(true)
const error = ref('')
const expandedProjectSlug = ref(null)

function toggleProject(slug) {
  expandedProjectSlug.value = expandedProjectSlug.value === slug ? null : slug
}

onMounted(async () => {
  try {
    const response = await getProjects()
    projects.value = Array.isArray(response.content?.projects) ? response.content.projects : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load projects.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section
    class="projects-section route-page detail-page-container"
    aria-labelledby="project-heading"
  >
    <DetailPageHeader
      current="PROJECTS"
      heading-id="project-heading"
      title="Projects"
      description="Architecture, implementation details, trade-offs, and future work."
    />

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading projects…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>Projects could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="projects.length === 0" class="page-state">
      No project entries are available yet.
    </div>

    <div v-else>
      <ProjectCard
        v-for="project in projects"
        :key="project.slug"
        :project="project"
        :expanded="expandedProjectSlug === project.slug"
        @toggle="toggleProject"
      />
    </div>
  </section>
</template>
