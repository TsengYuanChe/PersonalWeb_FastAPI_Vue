<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
})

const imageFailed = ref(false)
const showImage = computed(
  () => props.project.image_ready && props.project.image && !imageFailed.value,
)
</script>

<template>
  <article class="home-project-row">
    <div class="home-project-media">
      <img
        v-if="showImage"
        class="home-project-image"
        :src="project.image"
        :alt="project.image_alt"
        @error="imageFailed = true"
      />
      <div v-else class="home-project-placeholder">Coming soon</div>
    </div>

    <div class="home-project-heading">
      <h3 class="home-project-name">{{ project.name }}</h3>
      <div v-if="project.website_url || project.source_url" class="home-project-links">
        <a
          v-if="project.website_url"
          :href="project.website_url"
          target="_blank"
          rel="noopener noreferrer"
          :aria-label="`Open ${project.name} live website in a new tab`"
        >
          Live <span aria-hidden="true">↗</span>
        </a>
        <a
          v-if="project.source_url"
          :href="project.source_url"
          target="_blank"
          rel="noopener noreferrer"
          :aria-label="`Open ${project.name} source code in a new tab`"
        >
          Source <span aria-hidden="true">↗</span>
        </a>
      </div>
    </div>

    <p class="home-project-description">{{ project.introduction }}</p>

    <ul v-if="project.tags?.length" class="home-project-tags" aria-label="Technologies">
      <li v-for="tag in project.tags" :key="tag">{{ tag }}</li>
    </ul>
  </article>
</template>
