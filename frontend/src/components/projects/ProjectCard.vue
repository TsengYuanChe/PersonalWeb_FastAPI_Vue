<script setup>
import { useProjectHelpers } from '@/composables/useProjectHelpers'
import ProjectAction from '@/components/projects/ProjectAction.vue'
import ProjectCover from '@/components/projects/ProjectCover.vue'

defineProps({
  project: {
    type: Object,
    required: true,
  },
})

const { safeArray } = useProjectHelpers()
</script>

<template>
  <article class="project-card">
    <div class="project-card-summary">
      <ProjectCover
        :image="project.cover"
        :image-alt="project.cover_alt || `${project.title} cover`"
        :image-ready="project.cover_ready"
      />

      <div class="project-card-summary-content">
        <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap">
          <div class="project-card-heading">
            <p v-if="project.category" class="project-category mb-1">{{ project.category }}</p>
            <h2 class="h4 text-info mb-0">{{ project.title }}</h2>
            <p v-if="project.subtitle" class="project-card-subtitle text-secondary mb-0 mt-1">
              {{ project.subtitle }}
            </p>
          </div>

          <ProjectAction :project="project" :name="project.title" />
        </div>

        <p class="text-secondary mt-2 mb-0 project-description">
          {{ project.summary || 'No summary provided.' }}
        </p>

        <p v-if="project.role || project.period" class="project-card-meta text-secondary mb-0 mt-2">
          <span v-if="project.role">{{ project.role }}</span>
          <span v-if="project.role && project.period" aria-hidden="true"> · </span>
          <span v-if="project.period">{{ project.period }}</span>
        </p>
      </div>
    </div>

    <section
      v-if="safeArray(project.overview?.paragraphs).length"
      class="project-detail-section mt-3"
    >
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
      class="project-detail-section mt-3"
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

    <section v-if="project.architecture" class="project-detail-section mt-3">
      <h3 class="text-light h6 mb-2">{{ project.architecture.title }}</h3>
      <p
        v-for="(paragraph, index) in safeArray(project.architecture.paragraphs)"
        :key="`architecture-paragraph-${index}`"
        class="text-secondary mb-2"
      >
        {{ paragraph }}
      </p>
      <ul v-if="safeArray(project.architecture.highlights).length" class="text-secondary mb-2">
        <li
          v-for="(item, index) in safeArray(project.architecture.highlights)"
          :key="`architecture-${index}`"
        >
          {{ item }}
        </li>
      </ul>
    </section>

    <section v-if="safeArray(project.challenges?.items).length" class="project-detail-section mt-3">
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

    <section v-if="project.deployment" class="project-detail-section mt-3">
      <h3 class="text-light h6 mb-2">{{ project.deployment.title }}</h3>
      <p
        v-for="(paragraph, index) in safeArray(project.deployment.paragraphs)"
        :key="`deployment-paragraph-${index}`"
        class="text-secondary mb-2"
      >
        {{ paragraph }}
      </p>
      <ul v-if="safeArray(project.deployment.highlights).length" class="text-secondary mb-2">
        <li
          v-for="(item, index) in safeArray(project.deployment.highlights)"
          :key="`deployment-${index}`"
        >
          {{ item }}
        </li>
      </ul>
    </section>

    <section
      v-if="safeArray(project.lessons_learned?.items).length"
      class="project-detail-section mt-3"
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
  </article>
</template>
