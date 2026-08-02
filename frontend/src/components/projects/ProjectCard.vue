<script setup>
import { computed } from 'vue'
import ProjectAction from '@/components/projects/ProjectAction.vue'
import ProjectCover from '@/components/projects/ProjectCover.vue'
import ProjectDetail from '@/components/projects/ProjectDetail.vue'
import { useAutoHeightTransition } from '@/composables/useAutoHeightTransition'

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
const { beforeEnter, enter, afterEnter, beforeLeave, leave } = useAutoHeightTransition()

function toggleDetails() {
  emit('toggle', props.project.slug)
}

function handleHeaderClick(event) {
  if (event.target.closest('a, button, input, select, textarea, [role="button"]')) {
    return
  }

  toggleDetails()
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
        <ProjectDetail :project="project" />
      </div>
    </Transition>
  </article>
</template>
