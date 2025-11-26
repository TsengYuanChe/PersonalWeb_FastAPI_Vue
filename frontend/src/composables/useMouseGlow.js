import { onMounted, onBeforeUnmount } from 'vue'

export function useMouseGlow() {

  const moveGlow = (e) => {
    const glow = document.querySelector('.cursor-glow')
    if (!glow) return

    glow.style.transform = `translate(${e.clientX - glow.offsetWidth/2}px, ${e.clientY - glow.offsetHeight/2}px)`
  }

  onMounted(() => {
    window.addEventListener('mousemove', moveGlow)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('mousemove', moveGlow)
  })
}