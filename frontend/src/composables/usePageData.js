import { ref, onMounted } from 'vue'
import {
  getAboutWithMeta,
  getExperienceWithMeta,
  getProjectsWithMeta,
} from '@/api/contentApi'

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

  function getLogoUrl(file) {
    return new URL(`/src/assets/images/exp/${file}`, import.meta.url).href
  }

  onMounted(async () => {
    const aboutJson = await getAboutWithMeta()
    aboutData.value = aboutJson.data

    const expJson = await getExperienceWithMeta()
    expData.value = expJson.data

    const projectJson = await getProjectsWithMeta()
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
