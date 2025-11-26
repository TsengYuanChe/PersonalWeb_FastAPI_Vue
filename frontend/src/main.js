import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 自己的全域 CSS
import './assets/main.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
