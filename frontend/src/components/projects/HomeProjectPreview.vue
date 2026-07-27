<script setup>
import ProjectCover from '@/components/projects/ProjectCover.vue'

defineProps({
  project: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <article class="home-project-row">
    <ProjectCover
      class="home-project-media"
      :image="project.image"
      :image-alt="project.image_alt"
      :image-ready="project.image_ready"
    />

    <div class="home-project-heading">
      <h3 class="home-project-name">{{ project.name }}</h3>
      <div class="home-project-links">
        <a
          v-if="project.website_url"
          class="home-project-action"
          :href="project.website_url"
          target="_blank"
          rel="noopener noreferrer"
          :aria-label="`Open ${project.name} live website in a new tab`"
        >
          Live <span aria-hidden="true">↗</span>
        </a>
        <a
          v-else-if="project.source_url"
          class="home-project-action"
          :href="project.source_url"
          target="_blank"
          rel="noopener noreferrer"
          :aria-label="`Open ${project.name} source code in a new tab`"
        >
          Source <span aria-hidden="true">↗</span>
        </a>
        <span v-else class="home-project-action">🔒 Internal</span>
      </div>
    </div>

    <p class="home-project-description">{{ project.introduction }}</p>

    <ul v-if="project.tags?.length" class="home-project-tags" aria-label="Technologies">
      <li v-for="tag in project.tags" :key="tag">{{ tag }}</li>
    </ul>
  </article>
</template>
