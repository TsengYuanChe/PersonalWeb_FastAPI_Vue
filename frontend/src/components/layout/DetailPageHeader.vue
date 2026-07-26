<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  current: {
    type: String,
    required: true,
  },
  headingId: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
})
</script>

<template>
  <header class="route-page-header">
    <nav class="detail-breadcrumb" aria-label="Breadcrumb">
      <ol>
        <li><RouterLink to="/">HOME</RouterLink></li>
        <li aria-hidden="true">&gt;</li>
        <li aria-current="page">{{ current }}</li>
      </ol>
    </nav>

    <h1 :id="headingId" class="fw-bold">{{ title }}</h1>
    <p class="text-secondary">{{ description }}</p>
  </header>
</template>
