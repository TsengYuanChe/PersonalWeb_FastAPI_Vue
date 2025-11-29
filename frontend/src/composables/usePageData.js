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

  onMounted(async () => {
    const aboutRes = await fetch(`${API_BASE}/api/about`)
    const aboutJson = await aboutRes.json()
    aboutData.value = aboutJson

    const expRes = await fetch(`${API_BASE}/api/experience`)
    const expJson = await expRes.json()
    expData.value = expJson

    const projectRes = await fetch(`${API_BASE}/api/projects`)
    const projectJson = await projectRes.json()
    projectList.value = projectJson.projects

    updatedTime.value = pickLatestTime(
      aboutJson.updated_at,
      expJson.updated_at,
      projectJson.updated_at
    )
  })

  return {
    aboutData,
    expData,
    projectList,
    updatedTime,
  }
}