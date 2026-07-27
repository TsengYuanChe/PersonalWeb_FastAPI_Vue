<script setup>
import ProjectCover from '@/components/projects/ProjectCover.vue'
import ProjectAction from '@/components/projects/ProjectAction.vue'

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
      <ProjectAction :project="project" :name="project.name" />
    </div>

    <p class="home-project-description">{{ project.introduction }}</p>

    <ul v-if="project.tags?.length" class="home-project-tags" aria-label="Technologies">
      <li v-for="tag in project.tags" :key="tag">{{ tag }}</li>
    </ul>
  </article>
</template>
