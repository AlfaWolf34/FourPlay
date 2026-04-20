<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from './services/api'

const router = useRouter()
const user = ref(null)
const token = ref(null)

const ADMIN = 1
const OWNER = 2
const USER = 3

const isAuthenticated = computed(() => !!token.value)

const isAdmin = computed(() => user.value?.role === ADMIN)

const isOwner = computed(() => user.value?.role === OWNER)

const isUser = computed(() => user.value?.role === USER)

// 🔥 este es el importante
const canViewAdminSections = computed(() => {
  return user.value?.role === ADMIN || user.value?.role === OWNER
})

const loadUser = async () => {
  try {
    const response = await api.get('users/me/')
    user.value = response.data
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
    logout()
  }
}

const logout = () => {
  localStorage.removeItem('token')
  token.value = null
  user.value = null
  router.push('/login')
}

onMounted(async () => {
  const savedToken = localStorage.getItem('token')
  if (savedToken) {
    token.value = savedToken
    loadUser()
  }

  // 🔥 ESCUCHAR LOGIN (SOLUCIÓN AL BUG)
  window.addEventListener('login', () => {
    token.value = localStorage.getItem('token')
    loadUser()
  })
})
</script>

<template>
  <v-app>

    <!-- Navbar solo si está logueado -->
    <v-app-bar
      v-if="isAuthenticated"
      color="primary"
      dark
    >
      <v-toolbar-title>4Play</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn v-if="canViewAdminSections" variant="text" to="/calendario">Calendario</v-btn>
      <v-btn variant="text" to="/">Inicio</v-btn>
      <v-btn v-if="canViewAdminSections" variant="text" to="/estadisticas">Estadísticas</v-btn>
      <v-btn variant="text" to="/mis-reservaciones">Mis Reservaciones</v-btn>
      <v-btn variant="text" to="/nosotros">Nosotros</v-btn>
      <v-btn variant="text" to="/contacto">Contacto</v-btn>

      <v-btn
        variant="text"
        @click="logout"
      >
        Cerrar sesión
      </v-btn>


    </v-app-bar>

    <router-view />

  </v-app>
</template>