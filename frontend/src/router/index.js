import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import About from '../views/About.vue'
import Contact from '../views/Contact.vue'
import Courts from '../views/Courts.vue'
import MyBookings from '../views/MyBookings.vue'
import Calendar from '../views/Calendar.vue'
import MyBookingsFiltered from '../views/MyBookingsFiltered.vue'
import Estadisticas from '../views/Estadisticas.vue'
import api from '../services/api'

const ADMIN = 1
const OWNER = 2
const USER = 3

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/calendario',
    name: 'Calendar',
    component: Calendar,
    meta: { requiresAuth: true, roles: [ADMIN, OWNER] }
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
  },
  {
    path: '/mis-reservaciones-filtrado',
    name: 'MyBookingsFiltered',
    component: MyBookingsFiltered,
    meta: { requiresAuth: true }
  },
  {
    path: '/estadisticas',
    name: 'Estadisticas',
    component: Estadisticas,
    meta: { requiresAuth: true, roles: [ADMIN, OWNER] }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/* 🔐 Guard de navegación */
router.beforeEach(async (to) => {
  const token = localStorage.getItem('token')

  // 🔒 No autenticado
  if (to.meta.requiresAuth && !token) {
    return { name: 'Login' }
  }

  // 🚫 Ya logueado
  if (to.meta.guestOnly && token) {
    return { name: 'Home' }
  }

  console.log("ROLES PERMITIDOS:", to.meta.roles)

  // 🔐 Validación de roles
  if (to.meta.roles) {
    try {
      const res = await api.get('users/me/')
      const user = res.data
      const role = Number(user.role)

      console.log("ROLE:", role)

      if (!to.meta.roles.includes(role)) {
        return { name: 'Home' }
      }

    } catch (error) {
      return { name: 'Login' }
    }
  }

  return true
})

export default router