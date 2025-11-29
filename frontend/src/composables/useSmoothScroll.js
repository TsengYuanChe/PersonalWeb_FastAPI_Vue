export function useSmoothScroll() {
    const scrollToSection = (id) => {
      const container = document.querySelector('.content-area')
      const target = document.querySelector(id)
  
      if (!container || !target) return
  
      const top = target.offsetTop
  
      container.scrollTo({
        top: top,
        behavior: 'smooth'
      })
    }
  
    return { scrollToSection }
  }