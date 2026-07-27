<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  image: {
    type: String,
    default: '',
  },
  imageAlt: {
    type: String,
    default: 'Project cover',
  },
  imageReady: {
    type: Boolean,
    default: false,
  },
})

const imageFailed = ref(false)
const showImage = computed(() => props.imageReady && props.image && !imageFailed.value)

watch(
  () => [props.image, props.imageReady],
  () => {
    imageFailed.value = false
  },
)
</script>

<template>
  <div class="project-cover">
    <img
      v-if="showImage"
      class="project-cover-image"
      :src="image"
      :alt="imageAlt"
      @error="imageFailed = true"
    />
    <div v-else class="project-cover-placeholder">Coming soon</div>
  </div>
</template>
