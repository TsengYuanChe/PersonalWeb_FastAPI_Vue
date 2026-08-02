<script setup>
import { computed, onMounted, ref } from 'vue'
import { getJourney, getTimelineEvents } from '@/api/contentApi'
import JourneyDetail from '@/components/journey/JourneyDetail.vue'
import JourneySection from '@/components/journey/JourneySection.vue'
import Timeline from '@/components/journey/Timeline.vue'
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'
import { useAutoHeightTransition } from '@/composables/useAutoHeightTransition'

const journeyItems = ref([])
const timelineEvents = ref([])
const loading = ref(true)
const error = ref('')
const expandedJourneySlug = ref(null)
const leavingDetailSlugs = ref([])
const activeJourneySlug = ref(null)
const {
  beforeEnter: beforeDetailEnter,
  enter: enterDetail,
  afterEnter: afterDetailEnter,
  beforeLeave: beforeDetailLeave,
  leave: leaveDetail,
} = useAutoHeightTransition()

const detailRowSlugs = computed(() => {
  const slugs = new Set(leavingDetailSlugs.value)

  if (expandedJourneySlug.value) {
    slugs.add(expandedJourneySlug.value)
  }

  return slugs
})

const journeyRows = computed(() => {
  let row = 1

  return journeyItems.value.map((journeyItem) => {
    const entry = {
      journeyItem,
      headerRow: row,
      detailRow: null,
    }

    row += 1

    if (detailRowSlugs.value.has(journeyItem.slug)) {
      entry.detailRow = row
      row += 1
    }

    return entry
  })
})

const timelineRows = computed(() =>
  Object.fromEntries(
    journeyRows.value.map(({ journeyItem, headerRow }) => [journeyItem.slug, headerRow]),
  ),
)

function toggleJourney(slug) {
  const currentSlug = expandedJourneySlug.value

  if (currentSlug === slug) {
    leavingDetailSlugs.value = [...new Set([...leavingDetailSlugs.value, slug])]
    expandedJourneySlug.value = null
    return
  }

  if (currentSlug) {
    leavingDetailSlugs.value = [...new Set([...leavingDetailSlugs.value, currentSlug])]
  }

  leavingDetailSlugs.value = leavingDetailSlugs.value.filter((value) => value !== slug)
  expandedJourneySlug.value = slug
}

function finishDetailLeave(slug) {
  leavingDetailSlugs.value = leavingDetailSlugs.value.filter((value) => value !== slug)
}

function activateJourney(slug) {
  activeJourneySlug.value = slug
}

function deactivateJourney(slug) {
  if (activeJourneySlug.value === slug) {
    activeJourneySlug.value = null
  }
}

function handleJourneyFocusOut(event, slug) {
  if (event.currentTarget.contains(event.relatedTarget)) {
    return
  }

  deactivateJourney(slug)
}

function handleJourneyMouseLeave(event, slug) {
  if (event.currentTarget.contains(document.activeElement)) {
    return
  }

  deactivateJourney(slug)
}

onMounted(async () => {
  try {
    const [journeyResponse, timelineEventsResponse] = await Promise.all([
      getJourney(),
      getTimelineEvents(),
    ])
    journeyItems.value = Array.isArray(journeyResponse.content?.journey)
      ? journeyResponse.content.journey
      : []
    timelineEvents.value = Array.isArray(timelineEventsResponse.content?.timeline_events)
      ? timelineEventsResponse.content.timeline_events
      : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load journey.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section
    class="journey-page-section route-page detail-page-container"
    aria-labelledby="journey-heading"
  >
    <DetailPageHeader
      current="JOURNEY"
      heading-id="journey-heading"
      title="Journey"
      description="A detailed view of my professional and academic experience."
    />

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading journey…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>Journey could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="journeyItems.length === 0" class="page-state">
      No journey entries are available yet.
    </div>

    <div v-else class="journey-page-layout">
      <Timeline
        :journey-items="journeyItems"
        :events="timelineEvents"
        :active-slug="activeJourneySlug"
        :detail-slugs="[...detailRowSlugs]"
        :row-by-slug="timelineRows"
        @activate="activateJourney"
        @deactivate="deactivateJourney"
      />

      <div class="journey-section-list">
        <template v-for="(entry, index) in journeyRows" :key="entry.journeyItem.slug">
          <div
            class="journey-section-list__item"
            :class="{
              'is-active': activeJourneySlug === entry.journeyItem.slug,
              'is-expanded': expandedJourneySlug === entry.journeyItem.slug,
              'is-last': index === journeyRows.length - 1,
            }"
            :style="{ gridRow: entry.headerRow }"
            @mouseenter="activateJourney(entry.journeyItem.slug)"
            @mouseleave="handleJourneyMouseLeave($event, entry.journeyItem.slug)"
            @focusin="activateJourney(entry.journeyItem.slug)"
            @focusout="handleJourneyFocusOut($event, entry.journeyItem.slug)"
          >
            <JourneySection
              :journey="entry.journeyItem"
              :expanded="expandedJourneySlug === entry.journeyItem.slug"
              @toggle="toggleJourney"
            />
          </div>

          <Transition
            name="journey-details"
            @before-enter="beforeDetailEnter"
            @enter="enterDetail"
            @after-enter="afterDetailEnter"
            @before-leave="beforeDetailLeave"
            @leave="leaveDetail"
            @after-leave="finishDetailLeave(entry.journeyItem.slug)"
          >
            <div
              v-if="expandedJourneySlug === entry.journeyItem.slug"
              class="journey-detail-row"
              :style="{ gridRow: entry.detailRow }"
            >
              <JourneyDetail :journey="entry.journeyItem" />
            </div>
          </Transition>
        </template>
      </div>
    </div>
  </section>
</template>
