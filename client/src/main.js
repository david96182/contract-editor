import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import './assets/app.css'
import Vue3Signature from "vue3-signature"


createApp(App)
  .use(Vue3Signature)
  .use(router).mount('#app')
