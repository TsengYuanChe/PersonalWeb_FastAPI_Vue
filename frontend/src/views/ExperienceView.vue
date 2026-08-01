<script setup>
import { computed, onMounted, ref } from 'vue'
import { getExperience } from '@/api/contentApi'
import JourneyDetail from '@/components/experience/JourneyDetail.vue'
import JourneySection from '@/components/experience/JourneySection.vue'
import Timeline from '@/components/experience/Timeline.vue'
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'

const experiences = ref([])
const loading = ref(true)
const error = ref('')
const expandedExperienceSlug = ref(null)
const leavingDetailSlugs = ref([])
const activeExperienceSlug = ref(null)

const detailRowSlugs = computed(() => {
  const slugs = new Set(leavingDetailSlugs.value)

  if (expandedExperienceSlug.value) {
    slugs.add(expandedExperienceSlug.value)
  }

  return slugs
})

const journeyRows = computed(() => {
  let row = 1

  return experiences.value.map((experience) => {
    const entry = {
      experience,
      headerRow: row,
      detailRow: null,
    }

    row += 1

    if (detailRowSlugs.value.has(experience.slug)) {
      entry.detailRow = row
      row += 1
    }

    return entry
  })
})

const timelineRows = computed(() =>
  Object.fromEntries(journeyRows.value.map(({ experience, headerRow }) => [experience.slug, headerRow])),
)

function toggleExperience(slug) {
  const currentSlug = expandedExperienceSlug.value

  if (currentSlug === slug) {
    leavingDetailSlugs.value = [...new Set([...leavingDetailSlugs.value, slug])]
    expandedExperienceSlug.value = null
    return
  }

  if (currentSlug) {
    leavingDetailSlugs.value = [...new Set([...leavingDetailSlugs.value, currentSlug])]
  }

  leavingDetailSlugs.value = leavingDetailSlugs.value.filter((value) => value !== slug)
  expandedExperienceSlug.value = slug
}

function finishDetailLeave(slug) {
  leavingDetailSlugs.value = leavingDetailSlugs.value.filter((value) => value !== slug)
}

function activateExperience(slug) {
  activeExperienceSlug.value = slug
}

function deactivateExperience(slug) {
  if (activeExperienceSlug.value === slug) {
    activeExperienceSlug.value = null
  }
}

function handleExperienceFocusOut(event, slug) {
  if (event.currentTarget.contains(event.relatedTarget)) {
    return
  }

  deactivateExperience(slug)
}

function handleExperienceMouseLeave(event, slug) {
  if (event.currentTarget.contains(document.activeElement)) {
    return
  }

  deactivateExperience(slug)
}

function beforeDetailEnter(element) {
  element.style.height = '0'
  element.style.opacity = '0'
  element.style.transform = 'translateY(-4px)'
  element.inert = false
  element.removeAttribute('aria-hidden')
}

function enterDetail(element) {
  requestAnimationFrame(() => {
    element.style.height = `${element.scrollHeight}px`
    element.style.opacity = '1'
    element.style.transform = 'translateY(0)'
  })
}

function afterDetailEnter(element) {
  element.style.height = 'auto'
  element.style.opacity = ''
  element.style.transform = ''
}

function beforeDetailLeave(element) {
  element.style.height = `${element.scrollHeight}px`
  element.style.opacity = '1'
  element.style.transform = 'translateY(0)'
  element.inert = true
  element.setAttribute('aria-hidden', 'true')
}

function leaveDetail(element) {
  void element.offsetHeight

  requestAnimationFrame(() => {
    element.style.height = '0'
    element.style.opacity = '0'
    element.style.transform = 'translateY(-4px)'
  })
}

onMounted(async () => {
  try {
    const response = await getExperience()
    experiences.value = Array.isArray(response.content?.experience)
      ? response.content.experience
      : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load experiences.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section
    class="exp-section route-page detail-page-container"
    aria-labelledby="experience-heading"
  >
    <DetailPageHeader
      current="JOURNEY"
      heading-id="experience-heading"
      title="Journey"
      description="A detailed view of my professional and academic experience."
    />

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading experiences…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>Experiences could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="experiences.length === 0" class="page-state">
      No experience entries are available yet.
    </div>

    <div v-else class="journey-page-layout">
      <Timeline
        :experiences="experiences"
        :active-slug="activeExperienceSlug"
        :detail-slugs="[...detailRowSlugs]"
        :row-by-slug="timelineRows"
        @activate="activateExperience"
        @deactivate="deactivateExperience"
      />

      <div class="journey-section-list">
        <template v-for="(entry, index) in journeyRows" :key="entry.experience.slug">
          <div
            class="journey-section-list__item"
            :class="{
              'is-active': activeExperienceSlug === entry.experience.slug,
              'is-expanded': expandedExperienceSlug === entry.experience.slug,
              'is-last': index === journeyRows.length - 1,
            }"
            :style="{ gridRow: entry.headerRow }"
            @mouseenter="activateExperience(entry.experience.slug)"
            @mouseleave="handleExperienceMouseLeave($event, entry.experience.slug)"
            @focusin="activateExperience(entry.experience.slug)"
            @focusout="handleExperienceFocusOut($event, entry.experience.slug)"
          >
            <JourneySection
              :experience="entry.experience"
              :expanded="expandedExperienceSlug === entry.experience.slug"
              @toggle="toggleExperience"
            />
          </div>

          <Transition
            name="journey-details"
            @before-enter="beforeDetailEnter"
            @enter="enterDetail"
            @after-enter="afterDetailEnter"
            @before-leave="beforeDetailLeave"
            @leave="leaveDetail"
            @after-leave="finishDetailLeave(entry.experience.slug)"
          >
            <div
              v-if="expandedExperienceSlug === entry.experience.slug"
              class="journey-detail-row"
              :style="{ gridRow: entry.detailRow }"
            >
              <JourneyDetail :experience="entry.experience" />
            </div>
          </Transition>
        </template>
      </div>
    </div>
  </section>
</template>
