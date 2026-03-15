<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('token')
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
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

      <v-btn variant="text" to="/">Inicio</v-btn>
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