<script setup>
import { computed } from 'vue'
import { getJourneyLogo } from '@/utils/journey/journeyLogos'

const props = defineProps({
  journey: {
    type: Object,
    required: true,
  },
  expanded: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle'])
const logoUrl = computed(() => getJourneyLogo(props.journey.logo))
const detailsId = computed(() => `journey-details-${props.journey.slug}`)

function toggleDetails() {
  emit('toggle', props.journey.slug)
}

function handleHeaderClick(event) {
  if (event.target.closest('a, button, input, select, textarea, [role="button"]')) {
    return
  }

  toggleDetails()
}

</script>

<template>
  <article class="journey-section">
    <header class="journey-section__header" @click="handleHeaderClick">
      <div class="journey-section__media">
        <div class="journey-section__logo-wrapper">
          <img
            v-if="logoUrl"
            class="journey-section__logo"
            :src="logoUrl"
            :alt="`${journey.organization} logo`"
          />
        </div>
      </div>

      <div class="journey-section__main">
        <div class="journey-section__heading">
          <h2 class="h4 text-info mb-0">{{ journey.title }}</h2>
          <p class="journey-section__organization text-light mb-0 mt-1">
            {{ journey.organization }}
          </p>
        </div>

        <p class="journey-section__summary text-secondary mt-2 mb-0">
          {{ journey.summary }}
        </p>
      </div>

      <aside class="journey-section__meta" aria-label="Journey metadata">
        <div class="journey-section__meta-group">
          <p v-if="journey.role" class="journey-section__meta-item">{{ journey.role }}</p>
          <p v-if="journey.period" class="journey-section__meta-item">{{ journey.period }}</p>
        </div>

        <div class="journey-section__toggle-group">
          <button
            type="button"
            class="journey-section__toggle"
            :aria-expanded="expanded"
            :aria-controls="detailsId"
            @click="toggleDetails"
          >
            {{ expanded ? 'Less detail' : 'More detail' }}
            <span aria-hidden="true">{{ expanded ? '↑' : '↓' }}</span>
          </button>
        </div>
      </aside>
    </header>

  </article>
</template>
