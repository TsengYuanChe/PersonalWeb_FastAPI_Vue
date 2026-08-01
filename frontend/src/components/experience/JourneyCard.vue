<script setup>
import { computed } from 'vue'
import { getExperienceLogo } from '@/utils/experienceLogos'

const props = defineProps({
  experience: {
    type: Object,
    required: true,
  },
  expanded: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['toggle'])
const logoUrl = computed(() => getExperienceLogo(props.experience.logo))
const detailsId = computed(() => `journey-details-${props.experience.slug}`)
const skillsAndTechnologies = computed(() =>
  [...(props.experience.skills ?? []), ...(props.experience.technologies ?? [])].filter(
    (value, index, values) => values.indexOf(value) === index,
  ),
)

function toggleDetails() {
  emit('toggle', props.experience.slug)
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
  <article class="journey-card">
    <header class="journey-card__header" @click="handleHeaderClick">
      <div class="journey-card__media">
        <div class="journey-card__logo-wrapper">
          <img
            v-if="logoUrl"
            class="journey-card__logo"
            :src="logoUrl"
            :alt="`${experience.organization} logo`"
          />
        </div>
      </div>

      <div class="journey-card__main">
        <div class="journey-card__heading">
          <h2 class="h4 text-info mb-0">{{ experience.title }}</h2>
          <p class="journey-card__organization text-light mb-0 mt-1">
            {{ experience.organization }}
          </p>
        </div>

        <p class="journey-card__summary text-secondary mt-2 mb-0">
          {{ experience.summary }}
        </p>
      </div>

      <aside class="journey-card__meta" aria-label="Journey metadata">
        <div class="journey-card__meta-group">
          <p v-if="experience.role" class="journey-card__meta-item">{{ experience.role }}</p>
          <p v-if="experience.period" class="journey-card__meta-item">{{ experience.period }}</p>
        </div>

        <div class="journey-card__toggle-group">
          <button
            type="button"
            class="journey-card__toggle"
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
      name="journey-details"
      @before-enter="beforeEnter"
      @enter="enter"
      @after-enter="afterEnter"
      @before-leave="beforeLeave"
      @leave="leave"
    >
      <div v-if="expanded" :id="detailsId" class="journey-card__details">
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
          <div class="journey-card__skills" aria-label="Skills and technologies">
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
    </Transition>
  </article>
</template>
