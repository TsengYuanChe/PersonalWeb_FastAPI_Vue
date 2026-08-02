<script setup>
import { computed } from 'vue'
import { getJourneyLogo } from '@/utils/journey/journeyLogos'

const props = defineProps({
  journey: {
    type: Object,
    required: true,
  },
})

const logoUrl = computed(() => getJourneyLogo(props.journey.logo))
</script>

<template>
  <article class="home-journey-row">
    <div class="home-journey-logo-wrapper">
      <img
        v-if="logoUrl"
        class="home-journey-logo"
        :src="logoUrl"
        :alt="`${journey.name} logo`"
      />
    </div>

    <div class="home-journey-content">
      <div class="home-journey-meta">
        <h3 class="home-journey-position">{{ journey.position }}</h3>
        <span class="home-journey-duration">{{ journey.duration }}</span>
      </div>
      <p class="home-journey-name">{{ journey.name }}</p>
      <p class="home-journey-description">{{ journey.short_description }}</p>
    </div>
  </article>
</template>
