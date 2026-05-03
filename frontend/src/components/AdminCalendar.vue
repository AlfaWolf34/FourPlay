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
const filterOpen = ref(false)

onMounted(async () => {
  const [bookingsRes, fieldsRes] = await Promise.all([
    api.get('bookings/'),
    api.get('fields/')
  ])
  bookings.value = bookingsRes.data
  fields.value = fieldsRes.data
  loadEvents()

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.filter-dropdown')) filterOpen.value = false
  })
})

watch(selectedFields, () => loadEvents())

const toggleField = (id) => {
  const idx = selectedFields.value.indexOf(id)
  if (idx === -1) selectedFields.value.push(id)
  else selectedFields.value.splice(idx, 1)
}

const isSelected = (id) => selectedFields.value.includes(id)

const getFieldName = (fieldId) => {
  const field = fields.value.find(f => f.id === fieldId)
  return field ? field.name : 'Cancha'
}

const getFieldColor = (fieldId) => {
  const colors = { 1: '#2196f3', 2: '#9c27b0', 3: '#ff9800' }
  return colors[fieldId] || '#607d8b'
}

const loadEvents = () => {
  let filtered = bookings.value
  if (selectedFields.value.length > 0) {
    filtered = filtered.filter(b => selectedFields.value.includes(b.field))
  }
  calendarOptions.value.events = filtered.map(b => ({
    title: `${b.start_time?.slice(0, 5)} - ${getFieldName(b.field)}`,
    date: b.date,
    color: getFieldColor(b.field),
  }))
}

const calendarOptions = ref({
  plugins: [dayGridPlugin],
  initialView: 'dayGridMonth',
  events: [],
  height: 'auto',
  eventClick: (info) => {
    router.push({ name: 'MyBookingsFiltered', query: { date: info.event.startStr } })
  },
  eventDidMount: (info) => {
    info.el.title = info.event.title
  }
})
</script>

<template>
  <div class="calendar-page">

    <!-- Hero header -->
    <div class="page-hero">
      <div class="hero-label">
        <span class="dot"></span>
        ADMINISTRACIÓN
      </div>
      <div class="hero-title-row">
        <h1 class="hero-title">
          Calendario <span class="green">Administrativo</span>
        </h1>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <!-- Filter dropdown -->
      <div class="filter-dropdown" @click.stop>
        <button class="filter-btn" @click="filterOpen = !filterOpen">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
          </svg>
          Filtrar por Cancha
          <span v-if="selectedFields.length" class="filter-count">{{ selectedFields.length }}</span>
          <svg class="chevron" :class="{ rotated: filterOpen }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </button>

        <!-- Dropdown list -->
        <div class="dropdown-list" :class="{ open: filterOpen }">
          <label
            v-for="field in fields"
            :key="field.id"
            class="field-option"
            @click="toggleField(field.id)"
          >
            <span class="custom-checkbox" :class="{ checked: isSelected(field.id) }">
              <svg v-if="isSelected(field.id)" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
            </span>
            {{ field.name }}
          </label>

          <button v-if="selectedFields.length" class="clear-btn" @click="selectedFields = []">
            Limpiar filtro
          </button>
        </div>
      </div>
    </div>

    <!-- Calendar -->
    <div class="calendar-wrapper">
      <FullCalendar :options="calendarOptions" />
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.calendar-page {
  min-height: 100vh;
  background: #f0efe9;
  font-family: 'Barlow', sans-serif;
}

/* ── Hero ── */
.page-hero {
  padding: 2.5rem 2.5rem 1.2rem;
  max-width: 1300px;
  margin: 0 auto;
  text-align: left;
}

.hero-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #2d7a3a;
  margin-bottom: 0.5rem;
}

.dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #2d7a3a;
  animation: pulse 2s infinite;
  display: inline-block;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.hero-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: clamp(2.4rem, 4vw, 3.5rem);
  line-height: 1;
  color: #111;
  letter-spacing: -0.01em;
}

.hero-title .green { color: #2d7a3a; }

/* ── Toolbar ── */
.toolbar {
  padding: 0 2.5rem 1.2rem;
  max-width: 1300px;
  margin: 0 auto;
  display: flex;
  justify-content: flex;
}

/* Filter dropdown */
.filter-dropdown {
  position: relative;
  display: inline-block;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #c5d9c8;
  border: none;
  border-radius: 8px;
  padding: 0.65rem 1.1rem;
  font-family: 'Barlow', sans-serif;
  font-size: 0.88rem;
  font-weight: 600;
  color: #1e5c2a;
  cursor: pointer;
  transition: background 0.2s;
  min-width: 200px;
  justify-content: space-between;
}

.filter-btn:hover { background: #b5cdb9; }

.filter-count {
  background: #1e5c2a;
  color: #fff;
  border-radius: 10px;
  padding: 0.1rem;
  font-size: 0.72rem;
  font-weight: 700;
}

.chevron { transition: transform 0.2s; opacity: 0.7; }
.chevron.rotated { transform: rotate(180deg); }

.dropdown-list {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  background: #fff;
  border: 1px solid #e8e7e1;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  min-width: 240px;
  max-height: 320px;
  overflow-y: auto;
  z-index: 100;
  opacity: 0;
  transform: translateY(-6px);
  pointer-events: none;
  transition: all 0.18s ease;
}

.dropdown-list.open {
  opacity: 1;
  transform: translateY(0);
  pointer-events: all;
}

.field-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.7rem 1rem;
  cursor: pointer;
  font-size: 0.88rem;
  color: #333;
  transition: background 0.15s;
  user-select: none;
}

.field-option:hover { background: #f5f5f3; }

.custom-checkbox {
  width: 18px; height: 18px;
  border-radius: 4px;
  border: 1.5px solid #ccc;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}

.custom-checkbox.checked {
  background: #2d7a3a;
  border-color: #2d7a3a;
}

.clear-btn {
  width: 100%;
  padding: 0.65rem 1rem;
  background: none;
  border: none;
  border-top: 1px solid #f0f0f0;
  color: #e53e3e;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}
.clear-btn:hover { background: #fff5f5; }

/* ── Calendar ── */
.calendar-wrapper {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e8e7e1;
  padding: 1.5rem;
  margin: 0 2.5rem 3rem;
  max-width: calc(1300px - 5rem);
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

/* FullCalendar overrides */
:deep(.fc-toolbar-title) {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 800 !important;
  font-size: 1.4rem !important;
  color: #111 !important;
}

:deep(.fc-button) {
  background: #1e5c2a !important;
  border-color: #1e5c2a !important;
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 700 !important;
  letter-spacing: 0.05em !important;
  border-radius: 6px !important;
}

:deep(.fc-button:hover) {
  background: #2d7a3a !important;
  border-color: #2d7a3a !important;
}

:deep(.fc-day-today) {
  background: #f0f9f2 !important;
}

:deep(.fc-col-header-cell) {
  font-family: 'Barlow Condensed', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.08em !important;
  color: #888 !important;
}

:deep(.fc-event) {
  border-radius: 4px !important;
  font-family: 'Barlow', sans-serif !important;
  font-size: 0.78rem !important;
  cursor: pointer !important;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .page-hero { padding: 1.5rem 1rem 1rem; }
  .toolbar { padding: 0 1rem 1rem; }
  .calendar-wrapper { margin: 0 1rem 2rem; padding: 1rem; }
}
</style>