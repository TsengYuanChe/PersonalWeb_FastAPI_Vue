<script setup>
import { computed } from 'vue'
import ProjectAction from '@/components/projects/ProjectAction.vue'
import ProjectCover from '@/components/projects/ProjectCover.vue'

const props = defineProps({
  project: {
    type: Object,
    required: true,
  },
  expanded: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle'])
const detailsId = computed(() => `project-details-${props.project.slug}`)

function safeArray(value) {
  return Array.isArray(value) ? value : []
}

function toggleDetails() {
  emit('toggle', props.project.slug)
}

function handleHeaderClick(event) {
  if (event.target.closest('a, button, input, select, textarea, [role="button"]')) {
    return
  }

  toggleDetails()
}

function beforeEnter(element) {
  element.style.height = '0'
  element.style.opacity = '0'
  element.style.transform = 'translateY(-4px)'
  element.inert = false
  element.removeAttribute('aria-hidden')
}

function enter(element) {
  requestAnimationFrame(() => {
    element.style.height = `${element.scrollHeight}px`
    element.style.opacity = '1'
    element.style.transform = 'translateY(0)'
  })
}

function afterEnter(element) {
  element.style.height = 'auto'
  element.style.opacity = ''
  element.style.transform = ''
}

function beforeLeave(element) {
  element.style.height = `${element.scrollHeight}px`
  element.style.opacity = '1'
  element.style.transform = 'translateY(0)'
  element.inert = true
  element.setAttribute('aria-hidden', 'true')
}

function leave(element) {
  void element.offsetHeight

  requestAnimationFrame(() => {
    element.style.height = '0'
    element.style.opacity = '0'
    element.style.transform = 'translateY(-4px)'
  })
}
</script>

<template>
  <article class="project-card">
    <header class="project-card__header" @click="handleHeaderClick">
      <div class="project-card__media">
        <p v-if="project.category" class="project-category project-card__category">
          {{ project.category }}
        </p>
        <ProjectCover
          :image="project.cover"
          :image-alt="project.cover_alt || `${project.title} cover`"
          :image-ready="project.cover_ready"
        />
      </div>

      <div class="project-card__main">
        <div class="project-card__heading">
          <h2 class="h4 text-info mb-0">{{ project.title }}</h2>
          <p v-if="project.subtitle" class="project-card-subtitle text-secondary mb-0 mt-1">
            {{ project.subtitle }}
          </p>
        </div>

        <p class="text-secondary mt-2 mb-0 project-description">
          {{ project.summary || 'No summary provided.' }}
        </p>
      </div>

      <aside class="project-card__meta" aria-label="Project metadata">
        <div class="project-card__meta-group">
          <ProjectAction :project="project" :name="project.title" />
          <p v-if="project.role" class="project-card__meta-item">{{ project.role }}</p>
          <p v-if="project.period" class="project-card__meta-item">{{ project.period }}</p>
        </div>

        <div class="project-card__toggle-group">
          <button
            type="button"
            class="project-card__toggle"
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

    <Transition
      name="project-details"
      @before-enter="beforeEnter"
      @enter="enter"
      @after-enter="afterEnter"
      @before-leave="beforeLeave"
      @leave="leave"
    >
      <div v-if="expanded" :id="detailsId" class="project-card__details">
        <section
          v-if="safeArray(project.overview?.paragraphs).length"
          class="project-detail-section"
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

        <section v-if="project.architecture" class="project-detail-section">
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

        <section v-if="project.deployment" class="project-detail-section">
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
      </div>
    </Transition>
  </article>
</template>
