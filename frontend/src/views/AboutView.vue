<script setup>
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
  <article class="about-page route-page" aria-labelledby="about-heading">
    <header class="route-page-header">
      <p class="route-eyebrow">About</p>
      <h1 id="about-heading" class="fw-bold">About Me</h1>
      <p class="text-secondary">
        A closer look at my background, engineering approach, and the work I care about.
      </p>
    </header>

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
