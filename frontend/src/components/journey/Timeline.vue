<script setup>
import { computed } from 'vue'
import {
  datePosition,
  eventFitsJourney,
} from '@/utils/journey/timelineMath'

defineOptions({ name: 'JourneyTimeline' })

const props = defineProps({
  journeyItems: {
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

const eventsByJourney = computed(() => {
  const groupedEvents = Object.fromEntries(
    props.journeyItems.map((journeyItem) => [journeyItem.slug, []]),
  )

  props.events.forEach((event) => {
    const startDate = event.type === 'point' ? event.date : event.start_date
    const endDate = event.type === 'point' ? event.date : event.end_date
    const journeyItem = props.journeyItems.find((item) =>
      eventFitsJourney(startDate, endDate, item, currentMonthIndex),
    )

    if (!journeyItem) {
      return
    }

    const placement =
      event.type === 'point'
        ? { top: `${datePosition(event.date, journeyItem, currentMonthIndex)}%` }
        : {
            top: `${datePosition(event.end_date, journeyItem, currentMonthIndex)}%`,
            bottom: `${100 - datePosition(event.start_date, journeyItem, currentMonthIndex)}%`,
          }

    groupedEvents[journeyItem.slug].push({ ...event, placement })
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

function eventLabel(journeyItem, boundary) {
  const date = formatTimelineDate(
    boundary === 'end' ? journeyItem.end_date : journeyItem.start_date,
    boundary,
  )
  const event = boundary === 'end' ? 'end' : 'start'
  return `${journeyItem.organization} ${event}: ${date}`
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
        v-for="(journeyItem, index) in journeyItems"
        :key="journeyItem.slug"
        class="journey-timeline__period"
        :class="{
          'has-detail-row': detailSlugs.includes(journeyItem.slug),
          'is-last': index === journeyItems.length - 1,
        }"
        :style="{ gridRow: rowBySlug[journeyItem.slug] }"
        @mouseenter="emit('activate', journeyItem.slug)"
        @mouseleave="handlePeriodMouseLeave($event, journeyItem.slug)"
        @focusin="emit('activate', journeyItem.slug)"
        @focusout="handlePeriodFocusOut($event, journeyItem.slug)"
      >
        <div
          class="journey-timeline__segment"
          :class="{ 'is-active': activeSlug === journeyItem.slug }"
          aria-hidden="true"
        ></div>
        <span
          class="journey-timeline__label journey-timeline__label--end"
          aria-hidden="true"
        >
          {{ formatTimelineDate(journeyItem.end_date, 'end') }}
        </span>
        <button
          type="button"
          class="journey-timeline__node journey-timeline__node--end"
          :class="{ 'is-active': activeSlug === journeyItem.slug }"
          :aria-label="eventLabel(journeyItem, 'end')"
        ></button>
        <span
          class="journey-timeline__label journey-timeline__label--start"
          aria-hidden="true"
        >
          {{ formatTimelineDate(journeyItem.start_date, 'start') }}
        </span>
        <button
          type="button"
          class="journey-timeline__node journey-timeline__node--start"
          :class="{ 'is-active': activeSlug === journeyItem.slug }"
          :aria-label="eventLabel(journeyItem, 'start')"
        ></button>

        <div class="journey-timeline-events">
          <div
            v-for="event in eventsByJourney[journeyItem.slug]"
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
