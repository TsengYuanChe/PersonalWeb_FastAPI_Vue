import { ref, onMounted } from 'vue'
import {
  getAbout,
  getExperience,
  getProjects,
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
    const about = await getAbout()
    aboutData.value = about.content

    const exp = await getExperience()
    expData.value = exp.content

    const project = await getProjects()
    projectList.value = project.content.projects

    updatedTime.value = pickLatestTime(
      about.updatedAt,
      exp.updatedAt,
      project.updatedAt
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
