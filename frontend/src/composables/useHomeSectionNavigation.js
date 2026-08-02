export function useHomeSectionNavigation({ route, mainContent }) {
  function scrollToCurrentSection() {
    const container = mainContent.value
    if (!container) return

    const target = route.hash ? document.querySelector(route.hash) : null
    const homeTopSpacing = document.querySelector('#about')?.offsetTop || 0
    container.scrollTo({
      top: target ? Math.max(target.offsetTop - homeTopSpacing, 0) : 0,
      behavior: route.hash ? 'smooth' : 'auto',
    })
  }

  return { scrollToCurrentSection }
}
