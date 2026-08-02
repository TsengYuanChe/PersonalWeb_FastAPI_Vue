export function useAutoHeightTransition() {
  function beforeEnter(element) {
    element.style.height = '0'
    element.style.opacity = '0'
    element.style.transform = 'translateY(-4px)'
    element.inert = false
    element.removeAttribute('aria-hidden')
  }

  function enter(element) {
    requestAnimationFrame(() => {
      element.style.height = `${element.scrollHeight}px`
      element.style.opacity = '1'
      element.style.transform = 'translateY(0)'
    })
  }

  function afterEnter(element) {
    element.style.height = 'auto'
    element.style.opacity = ''
    element.style.transform = ''
  }

  function beforeLeave(element) {
    element.style.height = `${element.scrollHeight}px`
    element.style.opacity = '1'
    element.style.transform = 'translateY(0)'
    element.inert = true
    element.setAttribute('aria-hidden', 'true')
  }

  function leave(element) {
    void element.offsetHeight

    requestAnimationFrame(() => {
      element.style.height = '0'
      element.style.opacity = '0'
      element.style.transform = 'translateY(-4px)'
    })
  }

  return { beforeEnter, enter, afterEnter, beforeLeave, leave }
}
