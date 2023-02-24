import { createRouter, createWebHistory } from 'vue-router'
import Map from './components/Map.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: Map,
    },
    {
      path: '/radar/:radarId',
      component: Map,
    },
    {
      path: '/explications',
      component: () => import('./components/About.vue'),
    },
  ],
})
