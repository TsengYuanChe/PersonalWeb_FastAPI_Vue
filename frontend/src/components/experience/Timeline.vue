<script setup>
defineOptions({ name: 'JourneyTimeline' })

defineProps({
  experiences: {
    type: Array,
    required: true,
  },
  activeSlug: {
    type: String,
    default: null,
  },
})

const emit = defineEmits(['activate', 'deactivate'])

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
    <div
      class="journey-timeline__line"
      :style="{ gridRow: `1 / span ${experiences.length}` }"
      aria-hidden="true"
    ></div>

    <ol class="journey-timeline__periods">
      <li
        v-for="(experience, index) in experiences"
        :key="experience.slug"
        class="journey-timeline__period"
        :style="{ gridRow: index + 1 }"
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
      </li>
    </ol>
  </aside>
</template>
