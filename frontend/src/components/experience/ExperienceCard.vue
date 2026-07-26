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
  <article class="exp-card mb-5">
    <div class="d-flex align-items-center gap-3">
      <div class="exp-logo-wrapper">
        <img
          v-if="logoUrl"
          class="exp-logo"
          :src="logoUrl"
          :alt="`${experience.location} logo`"
        />
      </div>

      <div class="flex-grow-1">
        <div class="d-flex justify-content-between align-items-center flex-wrap">
          <h2 class="h4 text-info mb-1">{{ experience.position }}</h2>
          <span class="text-secondary small">{{ experience.duration }}</span>
        </div>

        <div class="d-flex justify-content-between align-items-center flex-wrap mt-1">
          <h3 class="h5 text-light mb-0">{{ experience.location }}</h3>
          <span v-if="experience.gpa" class="text-secondary small d-block mt-1 exp-gpa">
            {{ experience.gpa }}
          </span>
        </div>
      </div>
    </div>

    <ul v-if="experience.details?.length" class="text-secondary mt-3 mb-3 exp-detail-list">
      <li
        v-for="(detail, index) in experience.details"
        :key="index"
        class="text-secondary mb-2"
        v-html="detail"
      ></li>
    </ul>

    <div v-if="experience.skills?.length" class="exp-tag-group">
      <span v-for="skill in experience.skills" :key="skill" class="exp-skill-tag">
        {{ skill }}
      </span>
    </div>
  </article>
</template>
