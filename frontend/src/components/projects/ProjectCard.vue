<script setup>
import { useProjectHelpers } from '@/composables/useProjectHelpers'
import ProjectCover from '@/components/projects/ProjectCover.vue'

defineProps({
  project: {
    type: Object,
    required: true,
  },
})

const { safeArray, getGithubLink, getDemoLink } = useProjectHelpers()
</script>

<template>
  <article class="project-card">
    <div class="project-card-summary">
      <ProjectCover
        :image="project.image"
        :image-alt="project.image_alt || `${project.title} cover`"
        :image-ready="project.image_ready"
      />

      <div class="project-card-summary-content">
        <div class="d-flex justify-content-between align-items-center gap-3 flex-wrap">
          <div>
            <p v-if="project.category" class="project-category mb-1">{{ project.category }}</p>
            <h2 class="h4 text-info mb-0">{{ project.title }}</h2>
          </div>

          <div class="d-flex gap-2">
            <a
              v-if="getGithubLink(project)"
              :href="getGithubLink(project)"
              target="_blank"
              rel="noopener noreferrer"
              class="code-btn"
            >
              <i class="bi bi-code-slash"></i> GitHub
            </a>
            <a
              v-if="getDemoLink(project)"
              :href="getDemoLink(project)"
              target="_blank"
              rel="noopener noreferrer"
              class="code-btn"
            >
              <i class="bi bi-box-arrow-up-right"></i> Demo
            </a>
          </div>
        </div>

        <p class="text-secondary mt-2 mb-0 project-description">
          {{ project.overview || 'No overview provided.' }}
        </p>
      </div>
    </div>

    <div v-if="safeArray(project.features).length" class="mt-3">
      <p class="text-light mb-1"><strong>Features</strong></p>
      <ul class="text-secondary mb-2">
        <li v-for="(item, index) in safeArray(project.features)" :key="`feature-${index}`">
          {{ item }}
        </li>
      </ul>
    </div>

    <div v-if="safeArray(project.engineering).length" class="mt-2">
      <p class="text-light mb-1"><strong>Engineering</strong></p>
      <ul class="text-secondary mb-2">
        <li v-for="(item, index) in safeArray(project.engineering)" :key="`engineering-${index}`">
          {{ item }}
        </li>
      </ul>
    </div>

    <div v-if="project.architecture" class="mt-2">
      <p class="text-light mb-1"><strong>Architecture</strong></p>
      <p class="text-secondary mb-2">{{ project.architecture }}</p>
    </div>

    <div v-if="safeArray(project.tradeoffs).length" class="mt-2">
      <p class="text-light mb-1"><strong>Trade-offs</strong></p>
      <ul class="text-secondary mb-2">
        <li v-for="(item, index) in safeArray(project.tradeoffs)" :key="`tradeoff-${index}`">
          {{ item }}
        </li>
      </ul>
    </div>

    <div v-if="safeArray(project.future).length" class="mt-2">
      <p class="text-light mb-1"><strong>Future</strong></p>
      <ul class="text-secondary mb-2">
        <li v-for="(item, index) in safeArray(project.future)" :key="`future-${index}`">
          {{ item }}
        </li>
      </ul>
    </div>

    <div v-if="safeArray(project.tech).length" class="tag-group mt-3">
      <span v-for="item in safeArray(project.tech)" :key="item" class="tag tag-tool">
        {{ item }}
      </span>
    </div>
  </article>
</template>
