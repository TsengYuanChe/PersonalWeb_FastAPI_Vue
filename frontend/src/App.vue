<template>
  <div class="cursor-glow"></div>
  <div class="layout-container d-flex bg-dark text-light min-vh-100">

    <!-- Sidebar -->
    <aside class="sidebar d-flex flex-column justify-content-between p-4">

      <!-- Profile & Menu -->
      <div class="inner-content profile-part">
        <h1 class="display-6 fw-bold">Adam Tseng</h1>
        <h5 class="text-light">Software Developer</h5>

        <p class="mt-3 text-secondary" style="max-width: 250px;">
          I build intelligent, efficient digital experiences with Python, Flask, and modern tools.
        </p>

        <nav class="nav flex-column mt-4 nav-menu">
          <a href="#home" class="nav-link px-0 py-1">-- HOME</a>
          <a href="#about" class="nav-link px-0 py-1">-- ABOUT</a>
          <a href="#projects" class="nav-link px-0 py-1">-- PROJECTS</a>
        </nav>
      </div>

      <!-- Social icons -->
      <div class="inner-content social-icons d-flex justify-content-between align-items-center mt-5">
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
    </aside>

    <!-- Main content -->
    <main class="content-area flex-grow-1 p-5">

      <!-- HOME -->
      <section id="home" class="mb-5">
        <h2 class="fw-bold">{{ homeData.title }}</h2>
        <p class="mt-3">{{ homeData.intro }}</p>
        <p class="text-secondary">{{ homeData.desc }}</p>
      </section>

      <!-- ABOUT -->
      <section id="about" class="mb-5">
        <h2 class="fw-bold">About</h2>
        <p class="mt-3">{{ aboutData.description }}</p>

        <h5 class="mt-4 text-info">Skills</h5>
        <ul>
          <li v-for="skill in aboutData.skills" :key="skill">{{ skill }}</li>
        </ul>
      </section>

      <!-- PROJECTS -->
      <section id="projects">
        <h2 class="fw-bold">Projects</h2>

        <div 
          v-for="project in projectList" 
          :key="project.title" 
          class="mt-4"
        >
          <h4 class="text-info">{{ project.title }}</h4>
          <p class="text-secondary">{{ project.description }}</p>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { usePageData } from './composables/usePageData'
import { useScrollProxy } from './composables/useScrollProxy';
import { useMouseGlow } from './composables/useMouseGlow';

const { homeData, aboutData, projectList } = usePageData()

useScrollProxy();
useMouseGlow();
</script>