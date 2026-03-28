import { computed } from 'vue'

export function useProjectView(projectList) {

  const displayProjects = computed(() => {
    const list = projectList.value || []

    const featured = list.find(p => p.type === 'featured')
    const normals = list.filter(p => p.type === 'normal').slice(0, 2)

    return [
      ...(featured ? [featured] : []),
      ...normals
    ]
  })

  return {
    displayProjects
  }
}