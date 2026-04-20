<template>
  <v-container fluid class="mt-6 mx-11" style="width: 100%; max-width: 100%;">

    <h1 class="text-h4 font-weight-bold mb-6 mt-3">Estadísticas</h1>
    
    <v-row class="mb-6 mx-6" justify="start">
      <v-col cols="12" sm="4">
        <v-card class="pa-4 text-center">
          <div class="text-h6">Total</div>
          <div class="text-h4 font-weight-bold">{{ total }}</div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card class="pa-4 text-center">
          <div class="text-h6">Confirmadas</div>
          <div class="text-h4 font-weight-bold text-green">
            {{ confirmed }}
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="4">
        <v-card class="pa-4 text-center">
          <div class="text-h6">Canceladas</div>
          <div class="text-h4 font-weight-bold text-red">
            {{ cancelled }}
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" sm="3">
        <v-card class="pa-4 text-center">
          <div class="text-h6">Ganancias</div>
          <div class="text-h4 font-weight-bold text-blue">
            ${{ income.toFixed(2) }}
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-card class="pa-4">
      <h2 class="text-h6 mb-4">Reservaciones por día</h2>

      <div v-for="(count, date) in bookingsByDate" :key="date" class="mb-2">
        <div class="d-flex justify-space-between">
          <span>{{ formatDate(date) }}</span>
          <span>{{ count }}</span>
        </div>

        <v-progress-linear
          :model-value="count"
          :max="maxCount"
          height="8"
        />
      </div>
    </v-card>

    <v-card class="pa-4">
      <h2 class="text-h6 mb-4">Ganancias por día</h2>

      <div v-for="item in chartData" :key="item.date" class="mb-2">
        <div class="d-flex justify-space-between">
          <span>{{ formatDate(item.date) }}</span>
          <span>${{ item.total.toFixed(2) }}</span>
        </div>

        <v-progress-linear
          :model-value="item.total"
          :max="maxIncome"
          height="8"
          color="blue"
        />
      </div>
    </v-card>

  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const bookings = ref([])

onMounted(async () => {
  try {
    const res = await api.get('bookings/')
    bookings.value = res.data
  } catch (error) {
    console.error('Error cargando estadísticas', error)
  }
})

const total = computed(() => bookings.value.length)

const confirmed = computed(() =>
  bookings.value.filter(b => b.status === 'confirmed').length
)

const cancelled = computed(() =>
  bookings.value.filter(b => b.status === 'cancelled').length
)

const income = computed(() => {
  return bookings.value
    .filter(b => b.status === 'confirmed')
    .reduce((total, b) => {
      return total + Number(b.field_price || 0)
    }, 0)
})

const bookingsByDate = computed(() => {
  const map = {}

  bookings.value.forEach(b => {
    if (!map[b.date]) {
      map[b.date] = 0
    }
    map[b.date]++
  })

  return map
})

const incomeByDate = computed(() => {
  const map = {}

  bookings.value.forEach(b => {
    if (b.status !== 'confirmed') return

    if (!map[b.date]) {
      map[b.date] = 0
    }

    map[b.date] += Number(b.field_price || 0)
  })

  return map
})

const chartData = computed(() => {
  return Object.entries(incomeByDate.value).map(([date, total]) => ({
    date,
    total
  }))
})

const maxIncome = computed(() => {
  return Math.max(...chartData.value.map(i => i.total), 1)
})

const maxCount = computed(() => {
  return Math.max(...Object.values(bookingsByDate.value), 1)
})

const formatDate = (d) => {
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}
</script>