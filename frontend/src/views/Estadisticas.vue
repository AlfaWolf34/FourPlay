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

const income = computed(() =>
  bookings.value
    .filter(b => b.status === 'confirmed')
    .reduce((total, b) => total + Number(b.field_price || 0), 0)
)

const bookingsByDate = computed(() => {
  const map = {}
  bookings.value.forEach(b => {
    if (!map[b.date]) map[b.date] = 0
    map[b.date]++
  })
  return map
})

const incomeByDate = computed(() => {
  const map = {}
  bookings.value.forEach(b => {
    if (b.status !== 'confirmed') return
    if (!map[b.date]) map[b.date] = 0
    map[b.date] += Number(b.field_price || 0)
  })
  return map
})

const chartData = computed(() =>
  Object.entries(incomeByDate.value).map(([date, total]) => ({ date, total }))
)

const maxIncome = computed(() => Math.max(...chartData.value.map(i => i.total), 1))
const maxCount = computed(() => Math.max(...Object.values(bookingsByDate.value), 1))

const formatDate = (d) => {
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}
</script>

<template>
  <div class="stats-page">

    <!-- Hero header -->
    <div class="page-hero">
      <div class="hero-label">
        <span class="dot"></span>
        ADMINISTRACIÓN
      </div>
      <h1 class="hero-title">
        Estadísticas
      </h1>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-label">TOTAL</span>
        <span class="kpi-value">{{ total }}</span>
        <span class="kpi-sub">reservaciones</span>
      </div>

      <div class="kpi-card confirmed">
        <span class="kpi-label">CONFIRMADAS</span>
        <span class="kpi-value green">{{ confirmed }}</span>
        <span class="kpi-sub">reservaciones activas</span>
      </div>

      <div class="kpi-card cancelled">
        <span class="kpi-label">CANCELADAS</span>
        <span class="kpi-value red">{{ cancelled }}</span>
        <span class="kpi-sub">reservaciones canceladas</span>
      </div>

      <div class="kpi-card income">
        <span class="kpi-label">GANANCIAS</span>
        <span class="kpi-value blue">${{ income.toFixed(2) }}</span>
        <span class="kpi-sub">ingresos confirmados</span>
      </div>
    </div>

    <!-- Charts section -->
    <div class="charts-section">

      <!-- Reservaciones por día -->
      <div class="chart-card">
        <div class="chart-header">
          <h2>Reservaciones por día</h2>
          <span class="chart-badge">{{ Object.keys(bookingsByDate).length }} días</span>
        </div>

        <div class="chart-rows">
          <div v-if="!Object.keys(bookingsByDate).length" class="empty-chart">
            Sin datos disponibles
          </div>
          <div
            v-for="(count, date) in bookingsByDate"
            :key="date"
            class="chart-row"
          >
            <span class="chart-date">{{ formatDate(date) }}</span>
            <div class="bar-wrapper">
              <div
                class="bar green-bar"
                :style="{ width: (count / maxCount * 100) + '%' }"
              ></div>
            </div>
            <span class="chart-count">{{ count }}</span>
          </div>
        </div>
      </div>

      <!-- Ganancias por día -->
      <div class="chart-card">
        <div class="chart-header">
          <h2>Ganancias por día</h2>
          <span class="chart-badge blue-badge">MXN</span>
        </div>

        <div class="chart-rows">
          <div v-if="!chartData.length" class="empty-chart">
            Sin datos disponibles
          </div>
          <div
            v-for="item in chartData"
            :key="item.date"
            class="chart-row"
          >
            <span class="chart-date">{{ formatDate(item.date) }}</span>
            <div class="bar-wrapper">
              <div
                class="bar blue-bar"
                :style="{ width: (item.total / maxIncome * 100) + '%' }"
              ></div>
            </div>
            <span class="chart-count">${{ item.total.toFixed(0) }}</span>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.stats-page {
  min-height: 100vh;
  background: #f0efe9;
  font-family: 'Barlow', sans-serif;
}

/* ── Hero ── */
.page-hero {
  padding: 2.5rem 2.5rem 1.5rem;
  max-width: 1300px;
  margin: 0 auto;
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
  font-size: clamp(2.8rem, 5vw, 4rem);
  line-height: 1;
  color: #2d7a3a;
  letter-spacing: -0.01em;
  text-align: left;
}

/* ── KPI Grid ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 0 2.5rem 2rem;
  max-width: 1300px;
  margin: 0 auto;
}

.kpi-card {
  background: #c5d9c8;
  border-radius: 12px;
  padding: 1.5rem 1.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.kpi-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #1e5c2a;
}

.kpi-value {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 2.4rem;
  line-height: 1;
  color: #111;
}

.kpi-value.green { color: #1e5c2a; }
.kpi-value.red   { color: #dc2626; }
.kpi-value.blue  { color: #1d4ed8; }

.kpi-sub {
  font-size: 0.78rem;
  color: #4a7a54;
  font-weight: 500;
}

/* ── Charts ── */
.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
  padding: 0 2.5rem 3rem;
  max-width: 1300px;
  margin: 0 auto;
}

.chart-card {
  background: #fff;
  border-radius: 14px;
  border: 1px solid #e8e7e1;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.4rem;
}

.chart-header h2 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.1rem;
  color: #111;
}

.chart-badge {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  background: #f0f9f2;
  color: #2d7a3a;
  border: 1px solid #d4edda;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
}

.chart-badge.blue-badge {
  background: #eff6ff;
  color: #1d4ed8;
  border-color: #bfdbfe;
}

.chart-rows {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.empty-chart {
  font-size: 0.88rem;
  color: #bbb;
  text-align: center;
  padding: 2rem;
}

.chart-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.chart-date {
  font-size: 0.78rem;
  color: #888;
  width: 70px;
  flex-shrink: 0;
  font-weight: 500;
}

.bar-wrapper {
  flex: 1;
  height: 8px;
  background: #f0efe9;
  border-radius: 4px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.green-bar { background: #2d7a3a; }
.blue-bar  { background: #1d4ed8; }

.chart-count {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.88rem;
  color: #111;
  width: 55px;
  text-align: right;
  flex-shrink: 0;
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .kpi-grid { grid-template-columns: 1fr 1fr; padding: 0 1rem 1.5rem; }
  .charts-section { grid-template-columns: 1fr; padding: 0 1rem 2rem; }
  .page-hero { padding: 1.5rem 1rem 1rem; }
}

@media (max-width: 500px) {
  .kpi-grid { grid-template-columns: 1fr; }
}
</style>