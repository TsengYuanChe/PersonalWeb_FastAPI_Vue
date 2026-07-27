<script setup>
defineProps({
  project: {
    type: Object,
    required: true,
  },
  name: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <div class="home-project-links">
    <a
      v-if="project.website_url"
      class="home-project-action"
      :href="project.website_url"
      target="_blank"
      rel="noopener noreferrer"
      :aria-label="`Open ${name} live website in a new tab`"
    >
      Live <span aria-hidden="true">↗</span>
    </a>
    <a
      v-else-if="project.source_url"
      class="home-project-action"
      :href="project.source_url"
      target="_blank"
      rel="noopener noreferrer"
      :aria-label="`Open ${name} source code in a new tab`"
    >
      Source <span aria-hidden="true">↗</span>
    </a>
    <span v-else class="home-project-action">🔒 Internal</span>
  </div>
</template>
