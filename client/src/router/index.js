import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/employees',
    name: 'employees',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/EmployeesView.vue')
    }
  },
  {
    path: '/templates',
    name: 'templates',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/TemplatesView.vue')
    }
  },
  {
    path: '/contracts',
    name: 'contracts',
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/ContractsView.vue')
    }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
