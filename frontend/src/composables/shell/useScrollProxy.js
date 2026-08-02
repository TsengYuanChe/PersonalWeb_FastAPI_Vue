import { onBeforeUnmount, onMounted } from 'vue'

export function useScrollProxy({ container, enabled }) {
  const handleWheel = (e) => {
    const contentArea = container.value
    if (!contentArea || !enabled.value) return
    contentArea.scrollTop += e.deltaY // 滾動 right content
    e.preventDefault() // 禁止 body 捲動
  }

  onMounted(() => {
    // 全域監聽，不只 sidebar
    window.addEventListener('wheel', handleWheel, { passive: false })
  })

  onBeforeUnmount(() => {
    window.removeEventListener('wheel', handleWheel)
  })
}
