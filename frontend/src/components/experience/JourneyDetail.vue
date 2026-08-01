<script setup>
import { computed } from 'vue'

const props = defineProps({
  experience: {
    type: Object,
    required: true,
  },
})

const skillsAndTechnologies = computed(() =>
  [...(props.experience.skills ?? []), ...(props.experience.technologies ?? [])].filter(
    (value, index, values) => values.indexOf(value) === index,
  ),
)
</script>

<template>
  <div :id="`journey-details-${experience.slug}`" class="journey-detail">
    <section v-if="experience.description?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Description</h3>
      <p
        v-for="(paragraph, index) in experience.description"
        :key="`description-${index}`"
        class="text-secondary mb-2"
        v-html="paragraph"
      ></p>
    </section>

    <section v-if="experience.responsibilities?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Responsibilities</h3>
      <ul class="text-secondary mb-2">
        <li v-for="item in experience.responsibilities" :key="item">{{ item }}</li>
      </ul>
    </section>

    <section v-if="experience.highlights?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Highlights</h3>
      <ul class="text-secondary mb-2">
        <li v-for="item in experience.highlights" :key="item">{{ item }}</li>
      </ul>
    </section>

    <section v-if="experience.projects?.length" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Projects</h3>
      <ul class="text-secondary mb-2">
        <li v-for="item in experience.projects" :key="item">{{ item }}</li>
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

    <section v-if="experience.location || experience.gpa" class="journey-detail-section">
      <h3 class="text-light h6 mb-2">Additional Details</h3>
      <p v-if="experience.location" class="text-secondary mb-1">
        {{ experience.location }}
      </p>
      <p v-if="experience.gpa" class="text-secondary mb-0">{{ experience.gpa }}</p>
    </section>
  </div>
</template>
