import { ref, onMounted } from 'vue'

export function usePageData() {
  const homeData = ref({})
  const aboutData = ref({})
  const projectList = ref([])

  onMounted(async () => {
    const homeRes = await fetch('http://127.0.0.1:8000/api/index')
    homeData.value = await homeRes.json()

    const aboutRes = await fetch('http://127.0.0.1:8000/api/about')
    aboutData.value = await aboutRes.json()

    const projectRes = await fetch('http://127.0.0.1:8000/api/projects')
    projectList.value = (await projectRes.json()).projects
  })

  return {
    homeData,
    aboutData,
    projectList,
  }
}