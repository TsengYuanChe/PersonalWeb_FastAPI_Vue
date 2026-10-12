<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'

const props = defineProps({ images: { type: Array, required: true } })
const dialog = ref(null)
const closeButton = ref(null)
const activeIndex = ref(0)
const current = computed(() => props.images[activeIndex.value])
let restorePage = null

function open(index, trigger) {
  if (dialog.value.open || !props.images[index]) return
  activeIndex.value = index
  const { scrollX, scrollY } = window
  const body = document.body
  const styles = ['position', 'top', 'left', 'width', 'overflow'].map((name) => [
    name, body.style.getPropertyValue(name), body.style.getPropertyPriority(name),
  ])
  dialog.value.showModal()
  Object.assign(body.style, {
    position: 'fixed', top: `-${scrollY}px`, left: `-${scrollX}px`, width: '100%', overflow: 'hidden',
  })
  restorePage = () => {
    for (const [name, value, priority] of styles) {
      if (value) body.style.setProperty(name, value, priority)
      else body.style.removeProperty(name)
    }
    window.scrollTo({ left: scrollX, top: scrollY, behavior: 'instant' })
    if (trigger?.isConnected) trigger.focus({ preventScroll: true })
  }
  closeButton.value.focus({ preventScroll: true })
}

function cleanup() {
  restorePage?.()
  restorePage = null
}

function close() {
  dialog.value?.close()
  cleanup()
}

function navigate(offset) {
  if (props.images.length > 1) {
    activeIndex.value = (activeIndex.value + offset + props.images.length) % props.images.length
  }
}

function handleKeydown(event) {
  if (props.images.length < 2) return
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault()
    navigate(event.key === 'ArrowLeft' ? -1 : 1)
  }
}

onBeforeUnmount(close)
defineExpose({ open })
</script>

<template>
  <Teleport to="body">
    <dialog
      ref="dialog"
      class="showcase-lightbox"
      aria-label="Project showcase gallery"
      @cancel.prevent="close"
      @close="cleanup"
      @click.self="close"
      @keydown="handleKeydown"
    >
      <button ref="closeButton" type="button" class="showcase-lightbox__close" aria-label="Close gallery" @click="close">×</button>
      <div class="showcase-lightbox__stage" @click.self="close">
        <img v-if="current" :src="current.src" :alt="current.alt" />
      </div>
      <div class="showcase-lightbox__footer" @click.self="close">
        <button v-if="images.length > 1" type="button" aria-label="Previous image" @click="navigate(-1)">←</button>
        <div class="showcase-lightbox__info" aria-live="polite" aria-atomic="true">
          <div v-if="current?.caption">{{ current.caption }}</div>
          <div>{{ activeIndex + 1 }} / {{ images.length }}</div>
        </div>
        <button v-if="images.length > 1" type="button" aria-label="Next image" @click="navigate(1)">→</button>
      </div>
    </dialog>
  </Teleport>
</template>
