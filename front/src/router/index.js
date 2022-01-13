import { createRouter, createWebHistory } from 'vue-router'
import FrontPage from "../views/FrontPage"
import About from "../views/About";
import MovieInfo from "../views/MovieInfo";

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
  },
  {
    path: '/movie/:id',
    name: 'Movie info',
    component: MovieInfo
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: routes
})

export default router
