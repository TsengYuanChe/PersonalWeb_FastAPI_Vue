<script setup>
import { computed } from 'vue'
import {
  datePosition,
  eventFitsExperience,
} from '@/utils/journey/timelineMath'

defineOptions({ name: 'JourneyTimeline' })

const props = defineProps({
  experiences: {
    type: Array,
    required: true,
  },
  events: {
    type: Array,
    default: () => [],
  },
  activeSlug: {
    type: String,
    default: null,
  },
  detailSlugs: {
    type: Array,
    default: () => [],
  },
  rowBySlug: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['activate', 'deactivate'])

const currentDate = new Date()
const currentMonthIndex = currentDate.getUTCFullYear() * 12 + currentDate.getUTCMonth()

const eventsByExperience = computed(() => {
  const groupedEvents = Object.fromEntries(
    props.experiences.map((experience) => [experience.slug, []]),
  )

  props.events.forEach((event) => {
    const startDate = event.type === 'point' ? event.date : event.start_date
    const endDate = event.type === 'point' ? event.date : event.end_date
    const experience = props.experiences.find((item) =>
      eventFitsExperience(startDate, endDate, item, currentMonthIndex),
    )

    if (!experience) {
      return
    }

    const placement =
      event.type === 'point'
        ? { top: `${datePosition(event.date, experience, currentMonthIndex)}%` }
        : {
            top: `${datePosition(event.end_date, experience, currentMonthIndex)}%`,
            bottom: `${100 - datePosition(event.start_date, experience, currentMonthIndex)}%`,
          }

    groupedEvents[experience.slug].push({ ...event, placement })
  })

  return groupedEvents
})

const monthFormatter = new Intl.DateTimeFormat('en', {
  month: 'short',
  year: 'numeric',
  timeZone: 'UTC',
})

function formatTimelineDate(date, boundary) {
  if (!date) {
    return boundary === 'end' ? 'Present' : ''
  }

  const match = /^(\d{4})-(\d{2})$/.exec(date)

  if (!match) {
    return date
  }

  const [, year, month] = match
  return monthFormatter.format(new Date(Date.UTC(Number(year), Number(month) - 1, 1)))
}

function eventLabel(experience, boundary) {
  const date = formatTimelineDate(
    boundary === 'end' ? experience.end_date : experience.start_date,
    boundary,
  )
  const event = boundary === 'end' ? 'end' : 'start'
  return `${experience.organization} ${event}: ${date}`
}

function handlePeriodFocusOut(event, slug) {
  if (event.currentTarget.contains(event.relatedTarget)) {
    return
  }

  emit('deactivate', slug)
}

function handlePeriodMouseLeave(event, slug) {
  if (event.currentTarget.contains(document.activeElement)) {
    return
  }

  emit('deactivate', slug)
}
</script>

<template>
  <aside class="journey-timeline" aria-label="Journey timeline">
    <ol class="journey-timeline__periods">
      <li
        v-for="(experience, index) in experiences"
        :key="experience.slug"
        class="journey-timeline__period"
        :class="{
          'has-detail-row': detailSlugs.includes(experience.slug),
          'is-last': index === experiences.length - 1,
        }"
        :style="{ gridRow: rowBySlug[experience.slug] }"
        @mouseenter="emit('activate', experience.slug)"
        @mouseleave="handlePeriodMouseLeave($event, experience.slug)"
        @focusin="emit('activate', experience.slug)"
        @focusout="handlePeriodFocusOut($event, experience.slug)"
      >
        <div
          class="journey-timeline__segment"
          :class="{ 'is-active': activeSlug === experience.slug }"
          aria-hidden="true"
        ></div>
        <span
          class="journey-timeline__label journey-timeline__label--end"
          aria-hidden="true"
        >
          {{ formatTimelineDate(experience.end_date, 'end') }}
        </span>
        <button
          type="button"
          class="journey-timeline__node journey-timeline__node--end"
          :class="{ 'is-active': activeSlug === experience.slug }"
          :aria-label="eventLabel(experience, 'end')"
        ></button>
        <span
          class="journey-timeline__label journey-timeline__label--start"
          aria-hidden="true"
        >
          {{ formatTimelineDate(experience.start_date, 'start') }}
        </span>
        <button
          type="button"
          class="journey-timeline__node journey-timeline__node--start"
          :class="{ 'is-active': activeSlug === experience.slug }"
          :aria-label="eventLabel(experience, 'start')"
        ></button>

        <div class="journey-timeline-events">
          <div
            v-for="event in eventsByExperience[experience.slug]"
            :key="event.id"
            class="journey-timeline-event"
            :class="`journey-timeline-event--${event.type}`"
            :style="event.placement"
          >
            <span class="journey-timeline-event__label">{{ event.label }}</span>
            <span
              v-if="event.type === 'duration'"
              class="journey-timeline-event__segment"
              aria-hidden="true"
            ></span>
            <span class="journey-timeline-event__node journey-timeline-event__node--first" aria-hidden="true"></span>
            <span
              v-if="event.type === 'duration'"
              class="journey-timeline-event__node journey-timeline-event__node--last"
              aria-hidden="true"
            ></span>
          </div>
        </div>
      </li>
    </ol>
  </aside>
</template>
