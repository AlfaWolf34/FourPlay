import { createRouter, createWebHistory } from 'vue-router'
import Home       from '../views/Home.vue'
import Login      from '../views/Login.vue'
import Register   from '../views/Register.vue'
import About      from '../views/About.vue'
import Contact    from '../views/Contact.vue'
import Courts     from '../views/Courts.vue'
import MyBookings from '../views/MyBookings.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guestOnly: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guestOnly: true }
  },
  {
    path: '/nosotros',
    name: 'About',
    component: About
  },
  {
    path: '/contacto',
    name: 'Contact',
    component: Contact
  },
  {
    path: '/courts/:id',
    name: 'Courts',
    component: Courts,
    meta: { requiresAuth: true }
  },
  {
    path: '/mis-reservaciones',
    name: 'MyBookings',
    component: MyBookings,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/* 🔐 Guard de navegación */
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // 🔒 Si requiere auth y no hay token → login
  if (to.meta.requiresAuth && !token) {
    return next({ name: 'Login' })
  }

  // 🚫 Si ya está logueado y quiere ir a login → home
  if (to.meta.guestOnly && token) {
    return next({ name: 'Home' })
  }

  next()
})

export default router