<template>
  <div class="d-flex bg-dark text-light min-vh-100">
    <!-- Sidebar -->
    <aside class="sidebar d-flex flex-column justify-content-between p-4">
      <div class="inner-content profile-part">
        <h1 class="display-6 fw-bold">Adam Tseng</h1>
        <h5 class="text-light">Software Developer</h5>
        <p class="mt-3 text-secondary" style="max-width: 250px;">
          I build intelligent, efficient digital experiences with Python, Flask, and modern tools.
        </p>

        <nav class="nav flex-column mt-4 nav-menu">
          <RouterLink class="nav-link px-0 py-1" to="/">-HOME</RouterLink>
          <RouterLink class="nav-link px-0 py-1" to="/about">-ABOUT</RouterLink>
          <RouterLink class="nav-link px-0 py-1" to="/projects">-PROJECTS</RouterLink>
        </nav>
      </div>

      <!-- Social icons -->
      <div class="inner-content social-icons d-flex gap-3 mt-5">
        <a href="https://github.com/TsengYuanChe" target="_blank" class="text-secondary"><i class="bi bi-github"></i></a>
        <a href="https://www.linkedin.com/in/adam-tseng-04838b237/" target="_blank" class="text-secondary"><i class="bi bi-linkedin"></i></a>
        <a href="https://www.instagram.com/adam0614__/" target="_blank" class="text-secondary"><i class="bi bi-instagram"></i></a>
        <a href="https://www.facebook.com/profile.php?id=100006659471037" target="_blank" class="text-secondary"><i class="bi bi-facebook"></i></a>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-grow-1 p-5">
      <div class="inner-content">
        <RouterView /> <!-- 顯示各頁內容 -->
      </div>
    </main>
  </div>
</template>

<script setup>
// 無需特別 JS，除非你想加動畫或切換特效
</script>