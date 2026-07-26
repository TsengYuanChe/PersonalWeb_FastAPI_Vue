<script setup>
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'

const aboutSections = [
  { slug: 'introduction', title: 'Introduction' },
  { slug: 'what-i-do', title: 'What I Do' },
  { slug: 'current-role', title: 'Current Role' },
  { slug: 'engineering-approach', title: 'Engineering Approach' },
  { slug: 'technical-background', title: 'Technical Background' },
  { slug: 'current-focus', title: 'Current Focus' },
]
</script>

<template>
  <article
    class="about-page route-page detail-page-container"
    aria-labelledby="about-heading"
  >
    <DetailPageHeader
      current="ABOUT"
      heading-id="about-heading"
      title="About Me"
      description="A closer look at my background, engineering approach, and the work I care about."
    />

    <div class="about-page-sections">
      <section
        v-for="section in aboutSections"
        :id="section.slug"
        :key="section.slug"
        class="about-page-section"
        :aria-labelledby="`${section.slug}-heading`"
      >
        <h2 :id="`${section.slug}-heading`">{{ section.title }}</h2>
        <p class="about-page-placeholder">Coming soon.</p>
      </section>
    </div>
  </article>
</template>
