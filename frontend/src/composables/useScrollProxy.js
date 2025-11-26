import { onMounted, onBeforeUnmount } from 'vue'

export function useScrollProxy() {
  let contentArea = null

  const handleWheelOnSidebar = (e) => {
    if (!contentArea) return
    contentArea.scrollTop += e.deltaY
  }

  onMounted(() => {
    const sidebar = document.querySelector('.sidebar')
    contentArea = document.querySelector('.content-area')

    if (sidebar) {
      sidebar.addEventListener('wheel', handleWheelOnSidebar)
    }
  })

  onBeforeUnmount(() => {
    const sidebar = document.querySelector('.sidebar')
    if (sidebar) {
      sidebar.removeEventListener('wheel', handleWheelOnSidebar)
    }
  })
}