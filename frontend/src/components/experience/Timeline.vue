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

function eventLabel(experience, boundary) {
  const date = boundary === 'end' ? experience.end_date || 'Present' : experience.start_date
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
        <button
          type="button"
          class="journey-timeline__node journey-timeline__node--end"
          :class="{ 'is-active': activeSlug === experience.slug }"
          :aria-label="eventLabel(experience, 'end')"
        ></button>
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
