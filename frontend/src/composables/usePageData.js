import { ref, onMounted } from 'vue'

export function usePageData() {
  const aboutData = ref({})
  const expData = ref({})
  const projectList = ref([])
  const updatedTime = ref('—')

  const API_BASE = import.meta.env.VITE_API_BASE

  function pickLatestTime(...time) {
    const validTimes = time.filter(Boolean)
    if (validTimes.length === 0) return '—'

    const latest = validTimes.sort(
      (a, b) => new Date(b).getTime() - new Date(a).getTime()
    )[0]

    return latest.split(" ")[0]
  }

  function getLogoUrl(file) {
    return new URL(`/src/assets/images/exp/${file}`, import.meta.url).href
  }

  onMounted(async () => {
    const aboutRes = await fetch(`${API_BASE}/api/v1/about`)
    const aboutJson = await aboutRes.json()
    aboutData.value = aboutJson.data

    const expRes = await fetch(`${API_BASE}/api/v1/experience`)
    const expJson = await expRes.json()
    expData.value = expJson.data

    const projectRes = await fetch(`${API_BASE}/api/v1/projects`)
    const projectJson = await projectRes.json()
    projectList.value = projectJson.data.projects

    updatedTime.value = pickLatestTime(
      aboutJson.meta?.updated_at,
      expJson.meta?.updated_at,
      projectJson.meta?.updated_at
    )
  })

  return {
    aboutData,
    expData,
    projectList,
    updatedTime,
    getLogoUrl,
  }
}
