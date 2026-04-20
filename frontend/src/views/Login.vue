<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')


const login = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await api.post('token/', {
      username: email.value, // aquí debe ser username
      password: password.value
    })

    // Guardar access token
    localStorage.setItem('token', response.data.access)
    //token.value = response.data.token
    window.dispatchEvent(new Event('login'))

    router.push('/')

  } catch (error) {
    console.log(error.response) // para ver qué devuelve
    errorMessage.value = 'Credenciales incorrectas'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="400" elevation="6" class="pa-6 rounded-xl">

      <v-card-title class="text-h5 text-center mb-4">
        Iniciar Sesión
      </v-card-title>

      <v-text-field
        v-model="email"
        label="Usuario"
        type="text"
        prepend-inner-icon="mdi-account"
        variant="outlined"
        class="mb-4"
      />

      <v-text-field
        v-model="password"
        label="Contraseña"
        type="password"
        prepend-inner-icon="mdi-lock"
        variant="outlined"
        class="mb-4"
      />

      <v-alert
        v-if="errorMessage"
        type="error"
        class="mb-4"
      >
        {{ errorMessage }}
      </v-alert>

      <v-btn
        color="primary"
        block
        :loading="loading"
        @click="login"
      >
        Entrar
      </v-btn>

    </v-card>
  </v-container>

  <v-btn
  variant="text"
  block
  class="mt-2"
  @click="$router.push('/register')"
>
  ¿No tienes cuenta? Regístrate
</v-btn>
</template>