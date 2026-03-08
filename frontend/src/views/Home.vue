<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const fields = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await api.get('fields/')
    fields.value = response.data
  } catch (error) {
    console.error("Error cargando canchas:", error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <v-container class="mt-8">

    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Canchas Afiliadas</h1>
      </v-col>
    </v-row>

    <!-- Loader -->
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary" />
      </v-col>
    </v-row>

    <!-- Listado -->
    <v-row v-else>
      <v-col
        v-for="field in fields"
        :key="field.id"
        cols="12"
        md="4"
      >
        <v-card elevation="4" class="rounded-xl">

          <v-img
            height="220"
            width="500"
            :src="field.image || '/placeholder.jpg'"
          >
        </v-img>

          <v-card-title>
            {{ field.name }}
          </v-card-title>

          <v-card-subtitle>
            {{ field.location }}
          </v-card-subtitle>

          <v-card-text>
            <div><strong>Horario:</strong> {{ field.open_time }} - {{ field.close_time }}</div>
            <div><strong>Precio por hora:</strong> ${{ field.price_per_hour }}</div>
          </v-card-text>

          <v-card-actions>
          <v-btn
  color="primary"
  :to="`/courts/${field.id}`"
>
  Reservar
</v-btn>
          </v-card-actions>

        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>