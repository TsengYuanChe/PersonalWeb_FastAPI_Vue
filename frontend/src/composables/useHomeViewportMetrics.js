import { onBeforeUnmount, onMounted } from 'vue'

export function useHomeViewportMetrics({ profilePart, mobileFooter }) {
  function updateLayoutVars() {
    const profileComponent = profilePart.value
    const footerComponent = mobileFooter.value
    // Component template refs expose their existing root DOM through `$el`.
    const header = profileComponent?.$el?.firstElementChild ?? profileComponent
    const footer = footerComponent?.$el ?? footerComponent

    document.documentElement.style.setProperty('--header-height', `${header?.offsetHeight || 140}px`)
    document.documentElement.style.setProperty('--footer-height', `${footer?.offsetHeight || 80}px`)
    document.documentElement.style.setProperty('--real-vh', `${window.innerHeight}px`)
  }

  onMounted(() => {
    updateLayoutVars()
    window.addEventListener('resize', updateLayoutVars)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('resize', updateLayoutVars)
  })

  return { updateLayoutVars }
}
