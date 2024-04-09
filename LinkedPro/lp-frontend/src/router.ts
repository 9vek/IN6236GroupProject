import { createRouter, createWebHistory } from "vue-router"
import Home from "./views/Home.vue"
import Login from "./views/Login.vue"
import SignUp from "./views/SignUp.vue"
import Me from "./views/Me.vue"

const webHistory = createWebHistory()

const router = createRouter({
  history: webHistory,
  routes: [
    {
      path: '/',
      component: Home,
    },
    {
      path: '/login',
      component: Login,
    },
    {
      path: '/signup',
      component: SignUp,
    }, 
    {
      path: '/me',
      component: Me,
    }, 
  ]
})

export default router