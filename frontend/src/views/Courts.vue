<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'

const route  = useRoute()
const router = useRouter()

const court   = ref(null)
const loading = ref(true)

// ── Reservación ──────────────────────────────────────────────────────────────
const selectedDate      = ref('')
const selectedStartTime = ref('')
const selectedEndTime   = ref('')
const bookingLoading    = ref(false)
const bookingSuccess    = ref(false)
const bookingError      = ref('')
const showDialog        = ref(false)

// ── Disponibilidad ───────────────────────────────────────────────────────────
const occupiedSlots    = ref([])   // slots ocupados para la fecha seleccionada
const loadingSlots     = ref(false)

// Consulta al backend qué slots están ocupados para esa fecha
const fetchAvailability = async (date) => {
  if (!date || !court.value) return
  loadingSlots.value = true
  try {
    const res = await api.get('bookings/availability/', {
      params: { field: court.value.id, date }
    })
    occupiedSlots.value = res.data.occupied_slots
    // Si el slot que tenía seleccionado ahora está ocupado, lo limpia
    if (isSlotOccupied({ start: selectedStartTime.value })) {
      selectedStartTime.value = ''
      selectedEndTime.value   = ''
    }
  } catch {
    occupiedSlots.value = []
  } finally {
    loadingSlots.value = false
  }
}

// Cada vez que el usuario cambia la fecha, recarga disponibilidad
watch(selectedDate, (newDate) => {
  selectedStartTime.value = ''
  selectedEndTime.value   = ''
  fetchAvailability(newDate)
})

// Genera slots de 1 hora entre open_time y close_time
const timeSlots = computed(() => {
  if (!court.value?.open_time || !court.value?.close_time) return []
  const slots = []
  const [openH]  = court.value.open_time.split(':').map(Number)
  const [closeH] = court.value.close_time.split(':').map(Number)
  for (let h = openH; h < closeH; h++) {
    const start = `${String(h).padStart(2, '0')}:00`
    const end   = `${String(h + 1).padStart(2, '0')}:00`
    slots.push({ label: `${start} - ${end}`, start, end })
  }
  return slots
})

const isSlotOccupied = (slot) =>
  occupiedSlots.value.some(o => o.start_time === slot.start)

const isSlotSelected = (slot) =>
  slot.start === selectedStartTime.value

const canBook = computed(() =>
  selectedDate.value && selectedStartTime.value && selectedEndTime.value
)

const selectSlot = (slot) => {
  if (isSlotOccupied(slot)) return   // bloquea click en slots ocupados
  selectedStartTime.value = slot.start
  selectedEndTime.value   = slot.end
}

const today = new Date().toISOString().split('T')[0]

const openDialog = () => {
  if (!canBook.value) return
  showDialog.value = true
}

const confirmBooking = async () => {
  bookingLoading.value = true
  bookingError.value   = ''
  try {
    const res = await api.post('bookings/', {
      field:      court.value.id,
      date:       selectedDate.value,
      start_time: selectedStartTime.value,
      end_time:   selectedEndTime.value,
    })
    await api.post(`bookings/${res.data.id}/confirm/`)

    bookingSuccess.value    = true
    showDialog.value        = false
    selectedDate.value      = ''
    selectedStartTime.value = ''
    selectedEndTime.value   = ''
    occupiedSlots.value     = []
  } catch (err) {
    const detail = err.response?.data
    if (typeof detail === 'object') {
      bookingError.value = Object.values(detail).flat().join(' ')
    } else {
      bookingError.value = 'Ocurrió un error al realizar la reservación.'
    }
  } finally {
    bookingLoading.value = false
  }
}

const formatTime = (t) => (t ? t.slice(0, 5) : '')

const sportIcon = (type) => ({
  football:   '⚽',
  basketball: '🏀',
  tennis:     '🎾',
  volleyball: '🏐',
  other:      '🏟️',
}[type] || '🏟️')

onMounted(async () => {
  try {
    const response = await api.get(`fields/${route.params.id}/`)
    court.value = response.data
  } catch {
    router.push('/')
  } finally {
    loading.value = false
  }
})
</script>

<template>

  <!-- Loader -->
  <v-container v-if="loading" class="text-center mt-16">
    <v-progress-circular indeterminate color="primary" size="56" />
  </v-container>

  <v-container v-else-if="court" class="mt-4">

    <!-- Imagen principal -->
    <v-img
      :src="court.image || `https://picsum.photos/seed/${court.id}/1200/400`"
      height="300"
      cover
      class="rounded-xl mb-6"
    />

    <v-row>

      <!-- ── Info de la cancha ── -->
      <v-col cols="12" md="7">
        <v-card class="rounded-xl pa-4" elevation="2">

          <div class="d-flex align-center mb-2">
            <span class="text-h3 mr-2">{{ sportIcon(court.sport_type) }}</span>
            <h1 class="text-h4 font-weight-bold">{{ court.name }}</h1>
          </div>

          <p class="text-body-1 text-medium-emphasis mb-3">
            📍 {{ court.location }}
          </p>

          <p class="text-body-1 mb-4">
            {{ court.description || 'Sin descripción disponible.' }}
          </p>

          <v-divider class="mb-4" />

          <v-row>
            <v-col cols="6">
              <div class="text-caption text-medium-emphasis">HORARIO</div>
              <div class="text-body-1 font-weight-medium">
                🕐 {{ formatTime(court.open_time) }} – {{ formatTime(court.close_time) }}
              </div>
            </v-col>
            <v-col cols="6">
              <div class="text-caption text-medium-emphasis">PRECIO POR HORA</div>
              <div class="text-body-1 font-weight-medium text-primary">
                💲{{ court.price_per_hour }} MXN
              </div>
            </v-col>
          </v-row>

        </v-card>
      </v-col>

      <!-- ── Panel de reservación ── -->
      <v-col cols="12" md="5">
        <v-card class="rounded-xl pa-4" elevation="3">

          <h2 class="text-h6 font-weight-bold mb-4">Reservar cancha</h2>

          <v-alert
            v-if="bookingSuccess"
            type="success"
            class="mb-4"
            closable
            @click:close="bookingSuccess = false"
          >
            ¡Reservación confirmada exitosamente!
          </v-alert>

          <v-alert
            v-if="bookingError"
            type="error"
            class="mb-4"
            closable
            @click:close="bookingError = ''"
          >
            {{ bookingError }}
          </v-alert>

          <!-- Fecha -->
          <v-text-field
            v-model="selectedDate"
            label="Fecha"
            type="date"
            :min="today"
            variant="outlined"
            class="mb-4"
          />

          <!-- Slots de horario -->
          <div class="mb-4">
            <div class="text-body-2 text-medium-emphasis mb-2">
              Selecciona un horario
              <v-progress-circular v-if="loadingSlots" indeterminate size="14" width="2" class="ml-2" />
            </div>
            <div v-if="!selectedDate" class="text-caption text-medium-emphasis">
              Selecciona primero una fecha para ver disponibilidad.
            </div>
            <div v-else-if="timeSlots.length" class="d-flex flex-wrap">
              <v-tooltip
                v-for="slot in timeSlots"
                :key="slot.start"
                :text="isSlotOccupied(slot) ? 'Horario no disponible' : ''"
                location="top"
              >
                <template #activator="{ props }">
                  <v-chip
                    v-bind="props"
                    :color="isSlotOccupied(slot) ? 'default' : isSlotSelected(slot) ? 'primary' : 'default'"
                    :variant="isSlotOccupied(slot) ? 'tonal' : isSlotSelected(slot) ? 'flat' : 'outlined'"
                    :disabled="isSlotOccupied(slot)"
                    class="ma-1"
                    :style="isSlotOccupied(slot) ? 'cursor:not-allowed; opacity:0.45;' : 'cursor:pointer'"
                    @click="selectSlot(slot)"
                  >
                    <v-icon v-if="isSlotOccupied(slot)" start size="14">mdi-lock</v-icon>
                    {{ slot.label }}
                  </v-chip>
                </template>
              </v-tooltip>
            </div>
            <p v-else class="text-caption text-medium-emphasis">
              No hay horarios configurados para esta cancha.
            </p>

            <!-- Leyenda -->
            <div v-if="selectedDate && timeSlots.length" class="d-flex align-center mt-3" style="gap:16px">
              <div class="d-flex align-center">
                <v-chip size="x-small" variant="outlined" color="default" class="mr-1">00:00</v-chip>
                <span class="text-caption text-medium-emphasis">Disponible</span>
              </div>
              <div class="d-flex align-center">
                <v-chip size="x-small" variant="flat" color="primary" class="mr-1">00:00</v-chip>
                <span class="text-caption text-medium-emphasis">Seleccionado</span>
              </div>
              <div class="d-flex align-center">
                <v-chip size="x-small" variant="tonal" color="default" class="mr-1" style="opacity:0.45">00:00</v-chip>
                <span class="text-caption text-medium-emphasis">Ocupado</span>
              </div>
            </div>
          </div>

          <!-- Resumen selección -->
          <v-alert v-if="canBook" type="info" variant="tonal" class="mb-4">
            📅 {{ selectedDate }} &nbsp;|&nbsp; 🕐 {{ selectedStartTime }} – {{ selectedEndTime }}
          </v-alert>

          <v-btn
            color="primary"
            block
            size="large"
            :disabled="!canBook"
            @click="openDialog"
          >
            Confirmar reservación
          </v-btn>

        </v-card>
      </v-col>
    </v-row>

    <!-- ── Diálogo de confirmación ── -->
    <v-dialog v-model="showDialog" max-width="420">
      <v-card class="rounded-xl pa-2">
        <v-card-title class="text-h6">Confirmar y pagar</v-card-title>
        <v-card-text>
          <p class="mb-3">Estás a punto de reservar:</p>
          <v-list density="compact">
            <v-list-item prepend-icon="mdi-soccer-field"   :title="court.name" />
            <v-list-item prepend-icon="mdi-calendar"       :title="selectedDate" />
            <v-list-item prepend-icon="mdi-clock-outline"  :title="`${selectedStartTime} – ${selectedEndTime}`" />
            <v-list-item prepend-icon="mdi-cash"           :title="`$${court.price_per_hour} MXN`" subtitle="(1 hora)" />
          </v-list>
        </v-card-text>
        <v-card-actions class="px-4 pb-4">
          <v-btn variant="text" @click="showDialog = false">Cancelar</v-btn>
          <v-spacer />
          <v-btn color="primary" :loading="bookingLoading" @click="confirmBooking">
            Pagar y reservar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>

</template>