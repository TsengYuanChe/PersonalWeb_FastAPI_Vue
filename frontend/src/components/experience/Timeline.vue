<script setup>
import { computed } from 'vue'

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
    const experience = props.experiences.find((item) => eventFitsExperience(startDate, endDate, item))

    if (!experience) {
      return
    }

    const placement =
      event.type === 'point'
        ? { top: `${datePosition(event.date, experience)}%` }
        : {
            top: `${datePosition(event.end_date, experience)}%`,
            bottom: `${100 - datePosition(event.start_date, experience)}%`,
          }

    groupedEvents[experience.slug].push({ ...event, placement })
  })

  return groupedEvents
})

function monthIndex(date) {
  const match = /^(\d{4})-(\d{2})$/.exec(date ?? '')

  if (!match) {
    return null
  }

  return Number(match[1]) * 12 + Number(match[2]) - 1
}

function experienceBounds(experience) {
  return {
    start: monthIndex(experience.start_date),
    end: experience.end_date ? monthIndex(experience.end_date) : currentMonthIndex,
  }
}

function eventFitsExperience(startDate, endDate, experience) {
  const eventStart = monthIndex(startDate)
  const eventEnd = monthIndex(endDate)
  const bounds = experienceBounds(experience)

  return (
    eventStart !== null &&
    eventEnd !== null &&
    bounds.start !== null &&
    bounds.end !== null &&
    eventStart >= bounds.start &&
    eventEnd <= bounds.end
  )
}

function datePosition(date, experience) {
  const dateValue = monthIndex(date)
  const bounds = experienceBounds(experience)

  if (dateValue === null || bounds.start === null || bounds.end === null) {
    return 0
  }

  const duration = bounds.end - bounds.start

  if (duration <= 0) {
    return 0
  }

  return ((bounds.end - dateValue) / duration) * 100
}

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
