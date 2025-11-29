<template>
  <div class="cursor-glow"></div>
  <div class="app-wrapper">
    <div class="layout-container text-light min-vh-100">

      <!-- Sidebar -->
      <aside class="sidebar d-flex flex-column justify-content-between">

        <!-- Profile & Menu -->
        <div class="inner-content profile-part">
          <h1 class="display-6 fw-bold">Adam Tseng</h1>
          <h5 class="text-light">Software Developer</h5>

          <p class="mt-3 text-secondary" style="max-width: 250px;">
            I build intelligent, efficient digital experiences with Python, Flask, and modern tools.
          </p>

          <nav class="nav flex-column mt-4 nav-menu">
            <a @click.prevent="scrollToSection('#about')" class="nav-link px-0 py-1">-- ABOUT</a>
            <a @click.prevent="scrollToSection('#exp')" class="nav-link px-0 py-1">-- EXPERIENCES</a>
            <a @click.prevent="scrollToSection('#projects')" class="nav-link px-0 py-1">-- PROJECTS</a>
          </nav>
        </div>

        <div class="bottom-area">

          <!-- Social icons -->
          <div class="inner-content social-icons d-flex align-items-center mt-5">
            <a href="https://github.com/TsengYuanChe" target="_blank" class="text-secondary fs-2">
              <i class="bi bi-github"></i>
            </a>
            <a href="https://www.linkedin.com/in/adam-tseng-04838b237/" target="_blank" class="text-secondary fs-2">
              <i class="bi bi-linkedin"></i>
            </a>
            <a href="https://www.instagram.com/adam0614__/" target="_blank" class="text-secondary fs-2">
              <i class="bi bi-instagram"></i>
            </a>
            <a href="https://www.facebook.com/profile.php?id=100006659471037" target="_blank" class="text-secondary fs-2">
              <i class="bi bi-facebook"></i>
            </a>
          </div>

          <!-- Last Updated -->
          <p class="last-updated mt-3 text-secondary small">
            Last updated: {{ updatedTime }}
          </p>
          
        </div>
      </aside>

      <!-- Main content -->
      <main class="main-content">

        <!-- ABOUT -->
        <section id="about" class="mb-5 about-section">
          <div class="about-text mt-3">
            <p
              v-for="(p, index) in aboutData.paragraphs"
              :key="index"
              class="text-secondary mb-3"
            >
              {{ p }}
            </p>
          </div>
        </section>

        <!-- EXPERIENCES -->
        <section id="exp">
          <h2 class="fw-bold">Experiences</h2>
          <p class="mt-3">{{ expData.description }}</p>

          <h5 class="mt-4 text-info">Skills</h5>
          <ul>
            <li v-for="skill in expData.skills" :key="skill">{{ skill }}</li>
          </ul>
        </section>

        <!-- PROJECTS -->
        <section id="projects" class="projects-section">
          <h2 class="fw-bold mb-4">Projects</h2>

          <div v-for="project in projectList" :key="project.title" class="project-card">

            <!-- Title & Code Button -->
            <div class="d-flex justify-content-between align-items-center">
              <h4 class="text-info mb-0">{{ project.title }}</h4>

              <a :href="project.url" target="_blank" class="code-btn">
                <i class="bi bi-code-slash"></i> Code
              </a>
            </div>

            <!-- Description -->
            <p class="text-secondary mt-2 mb-2">{{ project.description }}</p>

            <!-- Languages -->
            <div class="tag-group">
              <span v-for="lang in project.languages" :key="lang" class="tag tag-lang">
                {{ lang }}
              </span>
            </div>

            <!-- Tools -->
            <div class="tag-group mt-2">
              <span v-for="tool in project.tools" :key="tool" class="tag tag-tool">
                {{ tool }}
              </span>
            </div>

          </div>
        </section>

      </main>
    </div>
  </div>
</template>

<script setup>
import { usePageData } from './composables/usePageData'
import { useScrollProxy } from './composables/useScrollProxy';
import { useMouseGlow } from './composables/useMouseGlow';
import { useSmoothScroll } from './composables/useSmoothScroll'

const { aboutData, expData, projectList, updatedTime } = usePageData()
const { scrollToSection } = useSmoothScroll()

useScrollProxy();
useMouseGlow();
</script>