<script setup>
defineProps({
  section: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <section
    :id="section.id"
    class="about-page-section"
    :aria-labelledby="`${section.id}-heading`"
  >
    <h2 :id="`${section.id}-heading`">{{ section.title }}</h2>

    <div v-if="section.paragraphs?.length" class="about-page-section__paragraphs">
      <p v-for="(paragraph, index) in section.paragraphs" :key="index">
        {{ paragraph }}
      </p>
    </div>

    <ul v-if="section.items?.length" class="about-page-section__items">
      <li v-for="item in section.items" :key="item">{{ item }}</li>
    </ul>
  </section>
</template>
