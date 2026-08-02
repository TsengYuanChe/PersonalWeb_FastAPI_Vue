<script setup>
import { siteLinks } from '@/config/siteLinks'

defineProps({
  variant: {
    type: String,
    default: 'desktop',
    validator: (value) => ['desktop', 'mobile'].includes(value),
  },
})
</script>

<template>
  <div
    class="inner-content social-icons d-flex align-items-center"
    :class="{ 'mt-5': variant === 'desktop' }"
  >
    <a
      v-for="link in siteLinks"
      :key="link.id"
      :href="link.href"
      :target="link.external ? '_blank' : undefined"
      :rel="link.external ? 'noopener noreferrer' : undefined"
      :class="variant === 'desktop' ? 'text-secondary fs-2' : undefined"
      :data-label="variant === 'desktop' ? link.label : undefined"
      :aria-label="link.label"
    >
      <i :class="link.icon"></i>
    </a>
  </div>
</template>
