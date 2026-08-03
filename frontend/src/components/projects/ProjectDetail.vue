<script setup>
defineProps({
  project: {
    type: Object,
    required: true,
  },
})

function safeArray(value) {
  return Array.isArray(value) ? value : []
}
</script>

<template>
  <section v-if="safeArray(project.overview?.paragraphs).length" class="project-detail-section">
    <h3 class="text-light h6 mb-2">{{ project.overview.title }}</h3>
    <p
      v-for="(paragraph, index) in safeArray(project.overview.paragraphs)"
      :key="`overview-${index}`"
      class="text-secondary mb-2"
    >
      {{ paragraph }}
    </p>
  </section>

  <section
    v-if="safeArray(project.responsibilities?.items).length"
    class="project-detail-section"
  >
    <h3 class="text-light h6 mb-2">{{ project.responsibilities.title }}</h3>
    <ul class="text-secondary mb-2">
      <li
        v-for="(item, index) in safeArray(project.responsibilities.items)"
        :key="`responsibility-${index}`"
      >
        {{ item }}
      </li>
    </ul>
  </section>

  <section v-if="project.technical_highlights" class="project-detail-section">
    <h3 class="text-light h6 mb-2">{{ project.technical_highlights.title }}</h3>
    <p
      v-for="(paragraph, index) in safeArray(project.technical_highlights.paragraphs)"
      :key="`technical-highlight-paragraph-${index}`"
      class="text-secondary mb-2"
    >
      {{ paragraph }}
    </p>
    <ul
      v-if="safeArray(project.technical_highlights.highlights).length"
      class="text-secondary mb-2"
    >
      <li
        v-for="(item, index) in safeArray(project.technical_highlights.highlights)"
        :key="`technical-highlight-${index}`"
      >
        {{ item }}
      </li>
    </ul>
  </section>

  <section v-if="safeArray(project.challenges?.items).length" class="project-detail-section">
    <h3 class="text-light h6 mb-2">{{ project.challenges.title }}</h3>
    <div
      v-for="(challenge, index) in safeArray(project.challenges.items)"
      :key="`challenge-${index}`"
      class="mb-2"
    >
      <p class="text-light mb-1">
        <strong>{{ challenge.title }}</strong>
      </p>
      <p class="text-secondary mb-0">{{ challenge.description }}</p>
    </div>
  </section>

  <section v-if="project.outcome" class="project-detail-section">
    <h3 class="text-light h6 mb-2">{{ project.outcome.title }}</h3>
    <p
      v-for="(paragraph, index) in safeArray(project.outcome.paragraphs)"
      :key="`outcome-paragraph-${index}`"
      class="text-secondary mb-2"
    >
      {{ paragraph }}
    </p>
    <ul v-if="safeArray(project.outcome.highlights).length" class="text-secondary mb-2">
      <li
        v-for="(item, index) in safeArray(project.outcome.highlights)"
        :key="`outcome-${index}`"
      >
        {{ item }}
      </li>
    </ul>
  </section>

  <section
    v-if="safeArray(project.lessons_learned?.items).length"
    class="project-detail-section"
  >
    <h3 class="text-light h6 mb-2">{{ project.lessons_learned.title }}</h3>
    <ul class="text-secondary mb-2">
      <li
        v-for="(item, index) in safeArray(project.lessons_learned.items)"
        :key="`lesson-${index}`"
      >
        {{ item }}
      </li>
    </ul>
  </section>

  <div
    v-if="safeArray(project.technologies).length"
    class="tag-group mt-3"
    aria-label="Technologies"
  >
    <span v-for="item in safeArray(project.technologies)" :key="item" class="tag tag-tool">
      {{ item }}
    </span>
  </div>
</template>
