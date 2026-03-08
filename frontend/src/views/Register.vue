<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

const register = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    await api.post('users/', {
      username: username.value,
      email: email.value,
      password: password.value
    })

    router.push('/login')

  } catch (error) {
    console.log(error.response)
    errorMessage.value = 'Error al registrar usuario'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="400" elevation="6" class="pa-6 rounded-xl">

      <v-card-title class="text-h5 text-center mb-4">
        Crear Cuenta
      </v-card-title>

      <v-text-field
        v-model="username"
        label="Usuario"
        variant="outlined"
        class="mb-3"
      />

      <v-text-field
        v-model="email"
        label="Correo"
        type="email"
        variant="outlined"
        class="mb-3"
      />

      <v-text-field
        v-model="password"
        label="Contraseña"
        type="password"
        variant="outlined"
        class="mb-4"
      />

      <v-alert
        v-if="errorMessage"
        type="error"
        class="mb-3"
      >
        {{ errorMessage }}
      </v-alert>

      <v-btn
        color="primary"
        block
        :loading="loading"
        @click="register"
      >
        Registrarse
      </v-btn>

      <v-btn
        variant="text"
        block
        class="mt-2"
        @click="$router.push('/login')"
      >
        Ya tengo cuenta
      </v-btn>

    </v-card>
  </v-container>
</template>