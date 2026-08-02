<script setup>
import { RouterLink } from 'vue-router'
import aboutData from '@/data/home/about.json'
import homeJourney from '@/data/home/journey.json'
import homeProjects from '@/data/home/projects.json'
import HomeJourneyItem from '@/components/journey/HomeJourneyItem.vue'
import HomeProjectPreview from '@/components/projects/HomeProjectPreview.vue'
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

    <section id="journey" class="journey-page-section home-section">
      <div class="section-heading">
        <h2 class="fw-bold">Journey</h2>
        <RouterLink to="/journey" class="home-journey-link">
          View full journey <span aria-hidden="true">→</span>
        </RouterLink>
      </div>

      <div class="home-journey-list">
        <HomeJourneyItem
          v-for="journey in homeJourney.journey"
          :key="`${journey.name}-${journey.position}`"
          :journey="journey"
        />
      </div>
    </section>

    <section id="projects" class="projects-section home-section">
      <div class="section-heading">
        <h2 class="fw-bold">Projects</h2>
        <RouterLink to="/project" class="home-journey-link">
          View all projects <span aria-hidden="true">→</span>
        </RouterLink>
      </div>

      <div class="home-project-list">
        <HomeProjectPreview
          v-for="project in homeProjects.projects"
          :key="project.name"
          :project="project"
        />
      </div>
    </section>

  </div>
</template>
