import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

// 自己的全域 CSS
import './assets/main.css'
import './assets/main-rwd.css'
import './assets/projects.css'
import './assets/projects-rwd.css'
import './assets/about.css'
import './assets/about-rwd.css'
import './assets/exp.css'
import './assets/exp-rwd.css'

const app = createApp(App)

app.use(router)

app.mount('#app')
