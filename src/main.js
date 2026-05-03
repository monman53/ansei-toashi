import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import ViewPage from './pages/ViewPage.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: ViewPage },
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')
