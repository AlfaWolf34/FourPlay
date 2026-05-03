<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const bookings = ref([])
const loading  = ref(true)
const cancellingId = ref(null)
const toast = ref({ show: false, text: '', success: true })
const fields = ref([])

const statusConfig = {
  pending:        { label: 'Pendiente de pago', color: '#b45309', bg: '#fef3c7', dot: '#f59e0b' },
  confirmed:      { label: 'Confirmada',         color: '#166534', bg: '#dcfce7', dot: '#22c55e' },
  cancelled:      { label: 'Cancelada',          color: '#991b1b', bg: '#fee2e2', dot: '#ef4444' },
  payment_failed: { label: 'Pago fallido',       color: '#991b1b', bg: '#fee2e2', dot: '#ef4444' },
}

const getStatus = (status) =>
  statusConfig[status] || { label: status, color: '#555', bg: '#f0f0f0', dot: '#aaa' }

const formatDate = (d) => {
  if (!d) return ''
  const [y, m, day] = d.split('-')
  return `${day}/${m}/${y}`
}

const formatTime = (t) => (t ? t.slice(0, 5) : '')

const canCancel = (booking) => ['pending', 'confirmed'].includes(booking.status)

const cancelBooking = async (booking) => {
  cancellingId.value = booking.id
  try {
    await api.post(`bookings/${booking.id}/cancel/`)
    booking.status = 'cancelled'
    showToast('Reservación cancelada exitosamente.', true)
  } catch (err) {
    const msg = err.response?.data?.detail || 'No se pudo cancelar la reservación.'
    showToast(msg, false)
  } finally {
    cancellingId.value = null
  }
}

const showToast = (text, success) => {
  toast.value = { show: true, text, success }
  setTimeout(() => toast.value.show = false, 3000)
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
    showToast('Error al cargar reservaciones.', false)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="bookings-page">

    <!-- Hero header -->
    <div class="page-hero">
      <div class="hero-inner">
        <div class="hero-label">
          <span class="dot"></span>
          MIS RESERVACIONES
        </div>
        <div class="hero-title-row">
          <h1 class="hero-title">
            Historial de <span class="green">reservaciones</span>
          </h1>
          <div class="hero-meta" v-if="!loading">
            {{ bookings.length }} reservacion{{ bookings.length !== 1 ? 'es' : '' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-ring"></div>
    </div>

    <!-- Empty state -->
    <div v-else-if="!bookings.length" class="empty-state">
      <div class="empty-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
      </div>
      <h3>Aún no tienes reservaciones</h3>
      <p>Explora las canchas disponibles y haz tu primera reserva.</p>
      <router-link to="/" class="btn-primary">Ver canchas disponibles →</router-link>
    </div>

    <!-- Bookings grid -->
    <div v-else class="bookings-grid">
      <div
        v-for="booking in bookings"
        :key="booking.id"
        class="booking-card"
      >
        <!-- Status bar -->
        <div class="status-bar" :style="{ background: getStatus(booking.status).dot }"></div>

        <div class="card-inner">
          <!-- Header -->
          <div class="card-header">
            <span class="booking-id"># {{ String(booking.id).padStart(4, '0') }}</span>
            <span class="status-badge" :style="{ color: getStatus(booking.status).color, background: getStatus(booking.status).bg }">
              <span class="status-dot" :style="{ background: getStatus(booking.status).dot }"></span>
              {{ getStatus(booking.status).label }}
            </span>
          </div>

          <!-- Field name -->
          <h3 class="field-name">{{ getFieldName(booking.field) }}</h3>

          <!-- Details -->
          <div class="booking-details">
            <div class="detail-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <div>
                <span class="detail-label">FECHA</span>
                <span class="detail-value">{{ formatDate(booking.date) }}</span>
              </div>
            </div>

            <div class="detail-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
              <div>
                <span class="detail-label">HORARIO</span>
                <span class="detail-value">{{ formatTime(booking.start_time) }} – {{ formatTime(booking.end_time) }}</span>
              </div>
            </div>
          </div>

          <!-- Cancel button -->
          <button
            v-if="canCancel(booking)"
            class="btn-cancel"
            :class="{ loading: cancellingId === booking.id }"
            @click="cancelBooking(booking)"
            :disabled="cancellingId === booking.id"
          >
            <span v-if="cancellingId !== booking.id">Cancelar reservación</span>
            <span v-else class="spinner-sm"></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div class="toast" :class="{ show: toast.show, error: !toast.success }">
      <svg v-if="toast.success" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      <svg v-else width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      {{ toast.text }}
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.bookings-page {
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
  margin-bottom: 0.6rem;
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

.hero-title-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
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

.hero-meta {
  font-size: 0.85rem;
  color: #888;
  letter-spacing: 0.05em;
  padding-bottom: 0.3rem;
}

/* ── Loading ── */
.loading-state {
  display: flex;
  justify-content: center;
  padding: 5rem;
}

.spinner-ring {
  width: 36px; height: 36px;
  border: 3px solid #ddd;
  border-top-color: #2d7a3a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Empty state ── */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 5rem 2rem;
  text-align: center;
  gap: 0.8rem;
}

.empty-icon {
  width: 72px; height: 72px;
  background: #fff;
  border: 1px solid #e8e7e1;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  margin-bottom: 0.5rem;
}

.empty-state h3 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.4rem;
  color: #111;
}

.empty-state p { font-size: 0.9rem; color: #888; }

.btn-primary {
  margin-top: 0.5rem;
  background: #1e5c2a;
  color: #fff;
  text-decoration: none;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.08em;
  transition: background 0.2s;
}
.btn-primary:hover { background: #2d7a3a; }

/* ── Bookings grid ── */
.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.2rem;
  padding: 1rem 2.5rem 3rem;
  max-width: 1300px;
  margin: 0 auto;
}

/* ── Booking card ── */
.booking-card {
  background: #fff;
  border-radius: 14px;
  border: 1px solid #e8e7e1;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.booking-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}

.status-bar { height: 4px; width: 100%; }

.card-inner { padding: 1.3rem 1.4rem 1.4rem; }

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.9rem;
}

.booking-id {
  font-size: 0.75rem;
  font-weight: 600;
  color: #aaa;
  letter-spacing: 0.05em;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 0.25rem 0.7rem;
  border-radius: 20px;
}

.status-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
}

.field-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.25rem;
  color: #111;
  letter-spacing: -0.01em;
  margin-bottom: 1rem;
}

.booking-details {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.2rem;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  color: #aaa;
}

.detail-item > div {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.detail-label {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #aaa;
}

.detail-value {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.98rem;
  color: #111;
}

/* Cancel button */
.btn-cancel {
  width: 100%;
  padding: 0.7rem;
  border: 1.5px solid #fecaca;
  border-radius: 8px;
  background: #fff5f5;
  color: #dc2626;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.88rem;
  letter-spacing: 0.06em;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 40px;
}

.btn-cancel:hover { background: #fee2e2; border-color: #fca5a5; }
.btn-cancel.loading { opacity: 0.6; cursor: not-allowed; }

.spinner-sm {
  width: 16px; height: 16px;
  border: 2px solid rgba(220,38,38,0.3);
  border-top-color: #dc2626;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

/* ── Toast ── */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: #1e5c2a;
  color: #fff;
  padding: 0.8rem 1.3rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.88rem;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  transform: translateY(20px);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
  z-index: 999;
}

.toast.show { transform: translateY(0); opacity: 1; }
.toast.error { background: #dc2626; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .page-hero { padding: 1.5rem 1rem 1rem; }
  .bookings-grid { padding: 0.5rem 1rem 2rem; grid-template-columns: 1fr; }
}
</style>