<script setup>
import { computed } from 'vue'

const props = defineProps({
  journey: {
    type: Object,
    required: true,
  },
})

const skillsAndTechnologies = computed(() =>
  [...(props.journey.skills ?? []), ...(props.journey.technologies ?? [])].filter(
    (value, index, values) => values.indexOf(value) === index,
  ),
)
</script>

<template>
  <div :id="`journey-details-${journey.slug}`" class="journey-detail">
    <section v-if="journey.description?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Description</h3>
      <p
        v-for="(paragraph, index) in journey.description"
        :key="`description-${index}`"
        class="text-secondary mb-2"
        v-html="paragraph"
      ></p>
    </section>

    <section v-if="journey.responsibilities?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Responsibilities</h3>
      <ul class="text-secondary mb-2">
        <li v-for="item in journey.responsibilities" :key="item">{{ item }}</li>
      </ul>
    </section>

    <section v-if="journey.highlights?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Highlights</h3>
      <ul class="text-secondary mb-2">
        <li v-for="item in journey.highlights" :key="item">{{ item }}</li>
      </ul>
    </section>

    <section v-if="journey.projects?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Projects</h3>
      <ul class="text-secondary mb-2">
        <li v-for="item in journey.projects" :key="item">{{ item }}</li>
      </ul>
    </section>

    <section v-if="skillsAndTechnologies.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Skills &amp; Technologies</h3>
      <div class="journey-detail__skills" aria-label="Skills and technologies">
        <span v-for="item in skillsAndTechnologies" :key="item" class="tag tag-tool">
          {{ item }}
        </span>
      </div>
    </section>

    <section v-if="journey.location || journey.gpa" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Additional Details</h3>
      <p v-if="journey.location" class="text-secondary mb-1">
        {{ journey.location }}
      </p>
      <p v-if="journey.gpa" class="text-secondary mb-0">{{ journey.gpa }}</p>
    </section>
  </div>
</template>
