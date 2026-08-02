<script setup>
import SocialLinks from '@/components/layout/SocialLinks.vue'

defineProps({
  updatedTime: {
    type: String,
    default: '—',
  },
})
</script>

<template>
  <footer class="bottom-area mobile-footer">
    <SocialLinks variant="mobile" />
    <p class="last-updated mt-2 mb-0 text-secondary small">
      Last updated: {{ updatedTime }}
    </p>
  </footer>
</template>
