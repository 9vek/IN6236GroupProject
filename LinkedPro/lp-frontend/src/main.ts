import { createApp } from 'vue'
import './main.css'
import router from './router'
import store from './store'
import App from './App.vue'
// import axios from 'axios'

// axios.defaults.baseURL = '/api'

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
