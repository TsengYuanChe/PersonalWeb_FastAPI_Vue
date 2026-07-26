<script setup>
import { RouterLink } from 'vue-router'
import aboutData from '@/data/home/about.json'
import homeExperiences from '@/data/home/experiences.json'
import homeProjects from '@/data/home/projects.json'
import HomeJourneyItem from '@/components/experience/HomeJourneyItem.vue'
</script>

<template>
  <div class="home-view">
    <section id="about" class="mb-5 about-section">
      <div class="section-heading">
        <h2 class="fw-bold">Profile</h2>
        <RouterLink to="/about" class="home-journey-link">
          View more about me <span aria-hidden="true">→</span>
        </RouterLink>
      </div>
      <div class="about-text">
        <p
          v-for="(paragraph, index) in aboutData.paragraphs"
          :key="index"
          class="text-secondary mb-3"
        >
          <span v-html="paragraph"></span>
        </p>
      </div>
    </section>

    <section id="experiences" class="exp-section home-section">
      <div class="section-heading">
        <h2 class="fw-bold">Journey</h2>
        <RouterLink to="/experience" class="home-journey-link">
          View full journey <span aria-hidden="true">→</span>
        </RouterLink>
      </div>

      <div class="home-journey-list">
        <HomeJourneyItem
          v-for="experience in homeExperiences.experiences"
          :key="`${experience.name}-${experience.position}`"
          :experience="experience"
        />
      </div>
    </section>

    <section id="projects" class="projects-section home-section">
      <div class="section-heading">
        <h2 class="fw-bold">Projects</h2>
        <RouterLink to="/project" class="see-more-btn">View more →</RouterLink>
      </div>

      <article v-for="project in homeProjects.projects" :key="project.name" class="project-card home-project-card">
        <img
          v-if="project.image"
          class="home-project-image"
          :src="project.image"
          :alt="`${project.name} preview`"
        />
        <div v-else class="home-project-image-fallback" aria-hidden="true">
          <i class="bi bi-window-stack"></i>
        </div>

        <div class="home-project-content">
          <h3 class="h4 text-info mb-2">{{ project.name }}</h3>
          <p class="text-secondary project-description">{{ project.introduction }}</p>
          <div class="tag-group mt-3">
            <span v-for="skill in project.skills" :key="skill" class="tag tag-tool">
              {{ skill }}
            </span>
          </div>
          <RouterLink :to="project.link" class="home-project-link">View project →</RouterLink>
        </div>
      </article>

      <RouterLink to="/project" class="see-more-btn section-footer-link">
        View more projects →
      </RouterLink>
    </section>

    <section id="stack" class="mt-3 text-secondary">
      <p>
        This website is built with <strong>Vue 3</strong> on the frontend and a lightweight
        <strong>FastAPI</strong> backend providing dynamic content via JSON-based APIs. The project
        is fully containerized using <strong>Docker</strong>, deployed on
        <strong>Google Cloud Run</strong>, and automated through a complete
        <strong>GitHub Actions CI/CD pipeline</strong>.
      </p>
    </section>
  </div>
</template>
