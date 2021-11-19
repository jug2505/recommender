import { createRouter, createWebHistory } from 'vue-router'
import FrontPage from "../views/FrontPage"
import About from "../views/About";

const routes = [
  {
    path: '/',
    name: 'Front page',
    component: FrontPage
  },
  {
    path: '/about',
    name: 'About',
    component: About
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes
})

export default router
