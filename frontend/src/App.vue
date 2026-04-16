<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from './services/api'

const router = useRouter()
const user = ref(null)
const token = ref(localStorage.getItem('token'))

const isAuthenticated = computed(() => {
  return !!token.value
})

const isAdmin = computed(() => {
  const u = user.value
  return !!u && (
    u.username === 'admin'
  )
})

const logout = () => {
  localStorage.removeItem('token')
  token.value = null
  user.value = null
  router.push('/login')
}

onMounted(async () => {
  if (!isAuthenticated.value) return

  try {
    const response = await api.get('users/me/')
    user.value = response.data
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
  }
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

      <v-btn v-if="isAdmin" variant="text" to="/calendario">Calendario</v-btn>
      <v-btn variant="text" to="/">Inicio</v-btn>
      <v-btn v-if="isAdmin" variant="text" to="/estadisticas">Estadísticas</v-btn>
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