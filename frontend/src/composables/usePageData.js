import { ref, onMounted } from 'vue'

export function usePageData() {
  const aboutData = ref({})
  const expData = ref({})
  const projectList = ref([])
  const updatedTime = ref('—')

  function pickLatestTime(...time) {
    const validTimes = time.filter(Boolean)
    if (validTimes.length === 0) return '—'

    const latest = validTimes.sort(
      (a, b) => new Date(b).getTime() - new Date(a).getTime()
    )[0]

    return latest.split(" ")[0]
  }

  onMounted(async () => {
    const aboutRes = await fetch('http://127.0.0.1:8000/api/about')
    const aboutJson = await aboutRes.json()
    aboutData.value = aboutJson

    const expRes = await fetch('http://127.0.0.1:8000/api/experience')
    const expJson = await expRes.json()
    expData.value = expJson

    const projectRes = await fetch('http://127.0.0.1:8000/api/projects')
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