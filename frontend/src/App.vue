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
            I build full-stack systems and cloud-ready applications — from backend APIs to deployment automation.
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
          <h2 class="fw-bold">Profile</h2>

          <div class="about-text mt-3">
            <p
              v-for="(p, index) in aboutData.paragraphs"
              :key="index"
              class="text-secondary mb-3"
            >
              <span v-html="p"></span>
            </p>
          </div>
        </section>

        <!-- EXPERIENCES -->
        <section id="exp" class="exp-section">
          <h2 class="fw-bold">Experiences</h2>
          
          <div
            v-for="(exp, index) in expData.experience" 
            :key="index"
            class="exp-card mb-5"
          >
            <!-- Top Row -->
            <div class="d-flex align-items-center gap-3">

              <!-- LOGO -->
              <div class="exp-logo-wrapper">
                <img
                  v-if="exp.logo"
                  class="exp-logo"
                  :src="getLogoUrl(exp.logo)"
                  alt="logo"
                />
              </div>

              <!-- Title + Duration -->
              <div class="flex-grow-1">

                <div class="d-flex justify-content-between align-items-center flex-wrap">
                  <h4 class="text-info mb-1">{{ exp.position }}</h4>
                  <span class="text-secondary small">{{ exp.duration }}</span>
                </div>

                <div class="d-flex justify-content-between align-items-center flex-wrap mt-1">
                  <h5 class="text-light mb-0">{{ exp.location }}</h5>
                  <!-- GPA：只有大學會出現 -->
                  <span 
                    v-if="exp.gpa"
                    class="text-secondary small d-block mt-1"
                    style="opacity: 0.9;"
                  >
                    {{ exp.gpa }}
                  </span>
                </div>
              </div>

            </div>

            <!-- Details -->
            <ul class="text-secondary mt-3 mb-3 exp-detail-list">
              <li v-for="(d, i) in exp.details" :key="i" class="text-secondry mb-2" v-html="d"></li>
            </ul>

            <!-- Skills -->
            <div class="exp-tag-group">
              <span 
                v-for="skill in exp.skills" 
                :key="skill" 
                class="exp-skill-tag"
              >
                {{ skill }}
              </span>
            </div>

          </div>
        </section>

        <!-- PROJECTS -->
        <section id="projects" class="projects-section">
          <h2 class="fw-bold mb-4">Projects</h2>

          <div v-for="project in projectList" :key="project.title" class="project-card">

            <!-- Title & Code Button -->
            <div class="d-flex justify-content-between align-items-center">
              <h4 class="text-info mb-0">{{ project.title }}</h4>

              <a v-if="project.url" :href="project.url" target="_blank" class="code-btn">
                <i class="bi bi-code-slash"></i> Code
              </a>
            </div>

            <!-- Description -->
            <p class="text-secondary mt-2 mb-2 project-description">
              {{ project.description }}
            </p>

            <!-- Languages -->
            <div class="tag-group mt-2">
              <span v-for="lang in project.languages" :key="`lang-${lang}`" class="tag tag-lang">
                {{ lang }}
              </span>

              <span v-for="tool in project.tools" :key="`tool-${tool}`" class="tag tag-tool">
                {{ tool }}
              </span>
            </div>

          </div>

          <!-- ⭐ SEE MORE BUTTON -->
          <div class="see-more-wrapper mt-4">
            <a
              href="https://github.com/TsengYuanChe?tab=repositories"
              target="_blank"
              class="see-more-btn"
            >
              See more projects →
            </a>
          </div>
        </section>

        <!-- Tech Stack -->
        <section id="stack" class="mt-3 text-secondary">
          <p>
            This website is built with <strong>Vue 3</strong> on the frontend and a lightweight 
            <strong>FastAPI</strong> backend providing dynamic content via JSON-based APIs. 
            The project is fully containerized using <strong>Docker</strong>, deployed on 
            <strong>Google Cloud Run</strong>, and automated through a complete 
            <strong>GitHub Actions CI/CD pipeline</strong>.
          </p>
        </section>

      </main>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { usePageData } from './composables/usePageData'
import { useScrollProxy } from './composables/useScrollProxy';
import { useMouseGlow } from './composables/useMouseGlow';
import { useSmoothScroll } from './composables/useSmoothScroll'
import { useMobileFooter } from './composables/useMobileFooter';

const { aboutData, expData, projectList, updatedTime, getLogoUrl} = usePageData()
const { scrollToSection } = useSmoothScroll()

useScrollProxy();
useMouseGlow();
useMobileFooter(updatedTime);

// ---------------------------
//  手機版：自動取 sidebar 高度
// ---------------------------
onMounted(() => {
  function updateLayoutVars() {
    const header = document.querySelector('.profile-part');
    const footer = document.querySelector('.mobile-footer');

    const headerH = header?.offsetHeight || 140;
    const footerH = footer?.offsetHeight || 80;

    document.documentElement.style.setProperty('--header-height', `${headerH}px`);
    document.documentElement.style.setProperty('--footer-height', `${footerH}px`);
    document.documentElement.style.setProperty('--real-vh', `${window.innerHeight}px`);
  }

  updateLayoutVars();
  window.addEventListener('resize', updateLayoutVars);
});
</script>