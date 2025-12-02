import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 自己的全域 CSS
import './assets/css/main.css'
import './assets/css/main-rwd.css'
import './assets/css/projects.css'
import './assets/css/projects-rwd.css'
import './assets/css/about.css'
import './assets/css/about-rwd.css'
import './assets/css/exp.css'
import './assets/css/exp-rwd.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
