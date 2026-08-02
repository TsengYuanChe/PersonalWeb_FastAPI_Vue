<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { getProjects } from '@/api/contentApi'
import ProjectCard from '@/components/projects/ProjectCard.vue'
import DetailPageHeader from '@/components/layout/DetailPageHeader.vue'
import { matchesExactValue, matchesProjectSearch, uniqueSortedValues } from '@/utils/projects/projectSearch'

const projects = ref([])
const loading = ref(true)
const error = ref('')
const expandedProjectSlug = ref(null)
const searchQuery = ref('')
const selectedCategory = ref('')
const selectedTechnology = ref('')

const categoryOptions = computed(() =>
  uniqueSortedValues(projects.value.map((project) => project.category)),
)

const technologyOptions = computed(() =>
  uniqueSortedValues(projects.value.flatMap((project) => project.technologies ?? [])),
)

const filteredProjects = computed(() =>
  projects.value.filter((project) => {
    const matchesCategory =
      !selectedCategory.value || matchesExactValue(project.category, selectedCategory.value)
    const matchesTechnology =
      !selectedTechnology.value ||
      (Array.isArray(project.technologies) &&
        project.technologies.some((technology) =>
          matchesExactValue(technology, selectedTechnology.value),
        ))

    return matchesProjectSearch(project, searchQuery.value) && matchesCategory && matchesTechnology
  }),
)

const hasActiveFilters = computed(() =>
  Boolean(searchQuery.value.trim() || selectedCategory.value || selectedTechnology.value),
)

watch(filteredProjects, (visibleProjects) => {
  if (
    expandedProjectSlug.value &&
    !visibleProjects.some((project) => project.slug === expandedProjectSlug.value)
  ) {
    expandedProjectSlug.value = null
  }
})

function toggleProject(slug) {
  expandedProjectSlug.value = expandedProjectSlug.value === slug ? null : slug
}

function clearFilters() {
  searchQuery.value = ''
  selectedCategory.value = ''
  selectedTechnology.value = ''
  expandedProjectSlug.value = null
}

onMounted(async () => {
  try {
    const response = await getProjects()
    projects.value = Array.isArray(response.content?.projects) ? response.content.projects : []
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Unable to load projects.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <section
    class="projects-section route-page detail-page-container"
    aria-labelledby="project-heading"
  >
    <DetailPageHeader
      current="PROJECTS"
      heading-id="project-heading"
      title="Projects"
      description="Architecture, implementation details, trade-offs, and future work."
    />

    <div v-if="loading" class="page-state" role="status">
      <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
      Loading projects…
    </div>

    <div v-else-if="error" class="page-state page-state-error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <div>
        <strong>Projects could not be loaded.</strong>
        <p class="mb-0">{{ error }} Please try again later.</p>
      </div>
    </div>

    <div v-else-if="projects.length === 0" class="page-state">
      No project entries are available yet.
    </div>

    <template v-else>
      <form class="project-tools" role="search" @submit.prevent>
        <div class="project-tools__field project-tools__field--category">
          <label class="project-tools__label" for="project-category-filter">Category</label>
          <select id="project-category-filter" v-model="selectedCategory">
            <option value="">All Categories</option>
            <option v-for="category in categoryOptions" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>

        <div class="project-tools__field project-tools__field--technology">
          <label class="project-tools__label" for="project-technology-filter">Technology</label>
          <select id="project-technology-filter" v-model="selectedTechnology">
            <option value="">All Technologies</option>
            <option v-for="technology in technologyOptions" :key="technology" :value="technology">
              {{ technology }}
            </option>
          </select>
        </div>

        <div class="project-tools__clear">
          <button v-if="hasActiveFilters" type="button" @click="clearFilters">Clear filters</button>
        </div>

        <div class="project-tools__field project-tools__field--search">
          <label class="project-tools__label" for="project-search">Search</label>
          <input
            id="project-search"
            v-model="searchQuery"
            type="search"
            placeholder="Search projects..."
            autocomplete="off"
          />
        </div>
      </form>

      <div v-if="filteredProjects.length === 0" class="project-filter-empty" role="status">
        <p>No projects match the current search and filters.</p>
        <button type="button" @click="clearFilters">Clear filters</button>
      </div>

      <div v-else>
        <ProjectCard
          v-for="project in filteredProjects"
          :key="project.slug"
          :project="project"
          :expanded="expandedProjectSlug === project.slug"
          @toggle="toggleProject"
        />
      </div>
    </template>
  </section>
</template>
