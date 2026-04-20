<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const bookings = ref([])
const loading  = ref(true)
const cancellingId = ref(null)
const snackbar  = ref({ show: false, text: '', color: 'success' })
const fields = ref([])

const statusConfig = {
  pending:        { label: 'Pendiente de pago', color: 'warning',  icon: 'mdi-clock-outline' },
  confirmed:      { label: 'Confirmada',         color: 'success',  icon: 'mdi-check-circle-outline' },
  cancelled:      { label: 'Cancelada',          color: 'error',    icon: 'mdi-close-circle-outline' },
  payment_failed: { label: 'Pago fallido',       color: 'error',    icon: 'mdi-alert-circle-outline' },
}

const getStatus = (status) =>
  statusConfig[status] || { label: status, color: 'default', icon: 'mdi-help-circle-outline' }

const formatDate = (d) => {
  if (!d) return ''
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

const formatTime = (t) => (t ? t.slice(0, 5) : '')

const canCancel = (booking) =>
  ['pending', 'confirmed'].includes(booking.status)

const cancelBooking = async (booking) => {
  cancellingId.value = booking.id
  try {
    await api.post(`bookings/${booking.id}/cancel/`)
    booking.status = 'cancelled'
    snackbar.value = { show: true, text: 'Reservación cancelada.', color: 'success' }
  } catch (err) {
    const msg = err.response?.data?.detail || 'No se pudo cancelar la reservación.'
    snackbar.value = { show: true, text: msg, color: 'error' }
  } finally {
    cancellingId.value = null
  }
}

const getFieldName = (fieldId) => {
  const field = fields.value.find(f => f.id === fieldId)
  return field ? field.name : 'Cancha'
}

onMounted(async () => {
  try {
    const [bookingsRes, fieldsRes] = await Promise.all([
      api.get('bookings/'),
      api.get('fields/')
    ])

    bookings.value = bookingsRes.data
    fields.value = fieldsRes.data

  } catch {
    snackbar.value = { show: true, text: 'Error al cargar reservaciones.', color: 'error' }
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <v-container class="mt-6">

    <v-row class="mb-4" align="center">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Mis Reservaciones</h1>
        <p class="text-body-2 text-medium-emphasis">Historial de todas tus reservaciones</p>
      </v-col>
    </v-row>

    <!-- Loader -->
    <v-row v-if="loading">
      <v-col class="text-center mt-10">
        <v-progress-circular indeterminate color="primary" size="56" />
      </v-col>
    </v-row>

    <!-- Sin reservaciones -->
    <v-row v-else-if="!bookings.length">
      <v-col class="text-center mt-10">
        <v-icon size="80" color="grey-lighten-2">mdi-calendar-blank-outline</v-icon>
        <p class="text-h6 text-medium-emphasis mt-4">Aún no tienes reservaciones</p>
        <v-btn color="primary" class="mt-4" to="/">Ver canchas disponibles</v-btn>
      </v-col>
    </v-row>

    <!-- Lista -->
    <v-row v-else class="mt-2" style="row-gap: 16px;">
      <v-col
        v-for="booking in bookings"
        :key="booking.id"
        cols="12"
        sm="6"
        class="d-flex"
      >
        <v-card class="rounded-xl" elevation="2" width="100%">

          <!-- Franja de color según estado -->
          <v-sheet
            :color="getStatus(booking.status).color"
            height="6"
            class="rounded-t-xl"
          />

          <v-card-text class="pa-6">

            <!-- Encabezado: número + estado -->
            <div class="d-flex justify-space-between align-center mb-4">
              <span class="text-caption text-medium-emphasis font-weight-medium">
                Reservación #{{ booking.id }}
              </span>
              <v-chip
                :color="getStatus(booking.status).color"
                size="small"
                variant="tonal"
                :prepend-icon="getStatus(booking.status).icon"
              >
                {{ getStatus(booking.status).label }}
              </v-chip>
            </div>

            <!-- Datos -->
            <div class="d-flex align-center mb-3">
              <v-icon color="primary" class="mr-3">mdi-soccer-field</v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">CANCHA</div>
                <div class="text-body-1 font-weight-medium">
                  {{ getFieldName(booking.field) }}
                </div>
              </div>
            </div>

            <div class="d-flex align-center mb-3">
              <v-icon color="primary" class="mr-3">mdi-calendar</v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">FECHA</div>
                <div class="text-body-1 font-weight-medium">{{ formatDate(booking.date) }}</div>
              </div>
            </div>

            <div class="d-flex align-center">
              <v-icon color="primary" class="mr-3">mdi-clock-outline</v-icon>
              <div>
                <div class="text-caption text-medium-emphasis">HORARIO</div>
                <div class="text-body-1 font-weight-medium">
                  {{ formatTime(booking.start_time) }} – {{ formatTime(booking.end_time) }}
                </div>
              </div>
            </div>

          </v-card-text>

          <!-- Acción cancelar -->
          <v-card-actions v-if="canCancel(booking)" class="px-5 pb-5 pt-0">
            <v-btn
              color="error"
              variant="tonal"
              block
              :loading="cancellingId === booking.id"
              prepend-icon="mdi-close-circle-outline"
              @click="cancelBooking(booking)"
            >
              Cancelar reservación
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar de feedback -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      timeout="3000"
      location="bottom right"
    >
      {{ snackbar.text }}
    </v-snackbar>

  </v-container>
</template>