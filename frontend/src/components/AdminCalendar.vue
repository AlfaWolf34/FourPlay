<template>
  <v-container fluid class="mt-6">

    <h1 class="text-h4 font-weight-bold mb-6">
      Calendario Administrativo
    </h1>

    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-select 
          v-model="selectedFields" 
          :items="fields" 
          item-title="name" 
          item-value="id" 
          label="Filtrar por cancha"
          multiple 
          chips 
          clearable />
      </v-col>
    </v-row>

    <v-card class="pa-4">
      <FullCalendar :options="calendarOptions" />
    </v-card>

  </v-container>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'

const router = useRouter()
const bookings = ref([])
const fields = ref([])
const selectedFields = ref([])

onMounted(async () => {
  const [bookingsRes, fieldsRes] = await Promise.all([
    api.get('bookings/'),
    api.get('fields/')
  ])

  bookings.value = bookingsRes.data
  fields.value = fieldsRes.data
  loadEvents()
})

watch(selectedFields, () => {
  loadEvents()
})

const getFieldName = (fieldId) => {
  const field = fields.value.find(f => f.id === fieldId)
  return field ? field.name : 'Cancha'
}

const loadEvents = () => {
  let filtered = bookings.value

  if (selectedFields.value.length > 0) {
    filtered = filtered.filter(b =>
      selectedFields.value.includes(b.field)
    )
  }

  calendarOptions.value.events = filtered.map(b => ({
    title: `${b.start_time?.slice(0, 5)} - ${getFieldName(b.field)}`,
    date: b.date,
    color: getFieldColor(b.field),
  }))
}

const getFieldColor = (fieldId) => {
  const colors = {
    1: '#2196f3',
    2: '#9c27b0',
    3: '#ff9800'
  }

  return colors[fieldId] || '#607d8b'
}

const getColor = (status) => {
  if (status === 'confirmed') return '#4caf50' // verde
  if (status === 'cancelled') return '#f44336' // rojo
  return '#ff9800' // pendiente
}

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  events: [],
  height: 'auto',

  eventClick: (info) => {
    const date = info.event.startStr

    router.push({
      name: 'MyBookingsFiltered',
      query: { date }
    })
  },

  eventDidMount: (info) => {
    info.el.title = info.event.title
  }
})
</script>