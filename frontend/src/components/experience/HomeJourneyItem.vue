<script setup>
import { computed } from 'vue'
import { getExperienceLogo } from '@/utils/experienceLogos'

const props = defineProps({
  experience: {
    type: Object,
    required: true,
  },
})

const logoUrl = computed(() => getExperienceLogo(props.experience.logo))
</script>

<template>
  <article class="home-journey-row">
    <div class="home-journey-logo-wrapper">
      <img
        v-if="logoUrl"
        class="home-journey-logo"
        :src="logoUrl"
        :alt="`${experience.name} logo`"
      />
    </div>

    <div class="home-journey-content">
      <div class="home-journey-meta">
        <h3 class="home-journey-position">{{ experience.position }}</h3>
        <span class="home-journey-duration">{{ experience.duration }}</span>
      </div>
      <p class="home-journey-name">{{ experience.name }}</p>
      <p class="home-journey-description">{{ experience.short_description }}</p>
    </div>
  </article>
</template>
