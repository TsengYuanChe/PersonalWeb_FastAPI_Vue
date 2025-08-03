<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const data = ref(null)
const error = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:5000/api/index')
    data.value = res.data
  } catch (err) {
    error.value = err.message
    console.error('❌ API error:', err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <p v-if="loading">Loading...</p>
    <div v-else-if="data">
      <h1 class="display-4 mb-4">{{ data.title }}</h1>
      <p class="lead">{{ data.intro }}</p>
      <p>{{ data.desc }}</p>
    </div>
    <p v-else style="color: red;">API Error: {{ error }}</p>
  </div>
</template>