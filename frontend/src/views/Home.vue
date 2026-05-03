<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'

const BASE_URL = 'http://127.0.0.1:8000'

const fields = ref([])
const loading = ref(true)
const dialog = ref(false)
const isEdit = ref(false)
const imageFile = ref(null)
const imagePreview = ref(null)
const userRole = ref(null)

const loadUser = async () => {
  try {
    const res = await api.get('users/me/')
    userRole.value = Number(res.data.role)
  } catch (error) {
    console.error('Error cargando usuario', error)
  }
}

const canEdit = () => userRole.value === 1 || userRole.value === 2

const availableCount = computed(() => fields.value.filter(f => f.is_available).length)

const sportLabel = (type) => {
  const map = {
    football: 'FÚTBOL',
    basketball: 'BASQUETBOL',
    tennis: 'TENIS',
    volleyball: 'VOLEIBOL',
    other: 'OTRO'
  }
  return map[type] || type?.toUpperCase()
}

const sportSize = (field) => {
  // Intenta obtener número de jugadores del nombre o descripción
  const txt = (field.name + ' ' + (field.description || '')).toLowerCase()
  if (txt.includes('11')) return '11'
  if (txt.includes('7')) return '7'
  if (txt.includes('5')) return '5'
  return ''
}

const form = ref({
  id: null, name: '', location: '', sport_type: 'football',
  description: '', price_per_hour: '', is_available: true,
  open_time: '', close_time: ''
})

const openDialog = () => {
  isEdit.value = false
  form.value = { id: null, name: '', location: '', sport_type: 'football', description: '', price_per_hour: '', is_available: true, open_time: '', close_time: '' }
  imageFile.value = null
  imagePreview.value = null
  dialog.value = true
}

const editField = (field) => {
  isEdit.value = true
  form.value = { ...field }
  imagePreview.value = imageUrl(field.image)
  imageFile.value = null
  dialog.value = true
}

const handleImage = (event) => {
  const files = event.target.files
  if (!files || files.length === 0) return
  const selectedFile = files[0]
  if (!selectedFile || !(selectedFile instanceof File)) return
  imageFile.value = selectedFile
  imagePreview.value = URL.createObjectURL(selectedFile)
}

const saveField = async () => {
  const formData = new FormData()
  formData.append('name', form.value.name)
  formData.append('location', form.value.location)
  formData.append('sport_type', form.value.sport_type)
  formData.append('description', form.value.description)
  formData.append('price_per_hour', Number(form.value.price_per_hour))
  formData.append('is_available', form.value.is_available ? 'true' : 'false')
  formData.append('open_time', form.value.open_time)
  formData.append('close_time', form.value.close_time)
  if (imageFile.value) formData.append('image', imageFile.value)

  try {
    if (isEdit.value) {
      await api.put(`fields/${form.value.id}/`, formData)
    } else {
      await api.post('fields/', formData)
    }
    dialog.value = false
    imageFile.value = null
    imagePreview.value = null
    loadFields()
  } catch (error) {
    console.log('ERROR:', error.response?.data)
  }
}

const deleteField = async (id) => {
  if (!confirm('¿Eliminar cancha?')) return
  await api.delete(`fields/${id}/`)
  loadFields()
}

const loadFields = async () => {
  const response = await api.get('fields/')
  fields.value = response.data
}

const imageUrl = (imagePath) => {
  if (!imagePath) return null
  return imagePath.startsWith('http') ? imagePath : BASE_URL + imagePath
}

const formatTime = (t) => {
  if (!t) return ''
  return t.slice(0, 5)
}

onMounted(async () => {
  try {
    await loadUser()
    await loadFields()
  } catch (error) {
    console.error('Error cargando canchas:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="home-page">
    

    <!-- Top ticker bar -->
    <div class="ticker-bar">
      <div class="ticker-left">
        <span class="dot"></span>
        <span>{{ availableCount }} CANCHAS DISPONIBLES</span>
        <span class="divider">|</span>
        <span>MTY · DESDE $280 MXN / HR</span>
      </div>
      <div class="ticker-right">
        {{ new Date().toLocaleDateString('es-MX', { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase() }}
      </div>
    </div>

    <!-- Hero header -->
    <div class="hero-section">
      <div class="hero-label">
        <span class="dot green"></span>
        CANCHAS DISPONIBLES
      </div>
      <div class="hero-title-row">
        <h1 class="hero-title">
          Elige dónde <span class="green">jugar hoy</span>
        </h1>
        <div class="hero-meta">
          {{ fields.length }} canchas · MTY
        </div>
      </div>

      <button v-if="canEdit()" class="btn-add" @click="openDialog">
        + Nueva cancha
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-ring"></div>
    </div>

    <!-- Cards grid -->
    <div v-else class="cards-grid">
      <div
        v-for="(field, index) in fields"
        :key="field.id"
        class="court-card"
      >
        <!-- Image -->
        <div class="card-image-wrapper">
          <img
            :src="imageUrl(field.image) || '/placeholder.jpg'"
            :alt="field.name"
            class="card-image"
          />

          <!-- Sport badge -->
          <div class="sport-badge">
            {{ sportLabel(field.sport_type) }}
            <span v-if="sportSize(field)"> {{ sportSize(field) }}</span>
          </div>

          <!-- Card number -->
          <div class="card-number">{{ String(index + 1).padStart(2, '0') }}</div>

          <!-- Edit/Delete -->
          <div v-if="canEdit()" class="card-actions-overlay">
            <button class="icon-btn" @click="editField(field)" title="Editar">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button class="icon-btn danger" @click="deleteField(field.id)" title="Eliminar">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6l-1 14H6L5 6"/>
                <path d="M10 11v6M14 11v6"/>
                <path d="M9 6V4h6v2"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Card body -->
        <div class="card-body">
          <h3 class="court-name">{{ field.name }}</h3>
          <p class="court-location">{{ field.location }}</p>

          <div class="court-meta">
            <div class="meta-item">
              <span class="meta-label">HORARIO</span>
              <span class="meta-value">{{ formatTime(field.open_time) }} – {{ formatTime(field.close_time) }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">PRECIO / HORA</span>
              <span class="meta-value green">${{ Number(field.price_per_hour).toLocaleString('es-MX') }} MXN</span>
            </div>
          </div>

          <router-link :to="`/courts/${field.id}`" class="btn-reserve">
            RESERVAR →
          </router-link>
        </div>
      </div>
    </div>

    <!-- MODAL -->
    <div v-if="dialog" class="modal-overlay" @click.self="dialog = false">
      <div class="modal-box">
        <div class="modal-header">
          <h2>{{ isEdit ? 'Editar' : 'Nueva' }} Cancha</h2>
          <button class="modal-close" @click="dialog = false">✕</button>
        </div>

        <div class="modal-body">
          <div class="field-row">
            <div class="field-group">
              <label>Nombre</label>
              <input v-model="form.name" type="text" placeholder="Ej. Cancha Norte" />
            </div>
            <div class="field-group">
              <label>Tipo de cancha</label>
              <select v-model="form.sport_type">
                <option value="football">Fútbol</option>
                <option value="basketball">Basquetbol</option>
                <option value="tennis">Tenis</option>
                <option value="volleyball">Voleibol</option>
                <option value="other">Otro</option>
              </select>
            </div>
          </div>

          <div class="field-group">
            <label>Descripción</label>
            <textarea v-model="form.description" rows="2" placeholder="Descripción breve..."></textarea>
          </div>

          <div class="field-group">
            <label>Ubicación</label>
            <input v-model="form.location" type="text" placeholder="Dirección" />
          </div>

          <div class="field-row">
            <div class="field-group">
              <label>Precio por hora</label>
              <input v-model="form.price_per_hour" type="number" placeholder="350" />
            </div>
            <div class="field-group">
              <label>Disponible</label>
              <label class="toggle">
                <input type="checkbox" v-model="form.is_available" />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="field-row">
            <div class="field-group">
              <label>Hora apertura</label>
              <input v-model="form.open_time" type="time" />
            </div>
            <div class="field-group">
              <label>Hora cierre</label>
              <input v-model="form.close_time" type="time" />
            </div>
          </div>

          <div class="field-group">
            <label>Imagen</label>
            <input type="file" accept="image/*" @change="handleImage" class="file-input" />
            <img v-if="imagePreview" :src="imagePreview" class="image-preview" />
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="dialog = false">Cancelar</button>
          <button class="btn-save" @click="saveField">Guardar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.home-page {
  min-height: 100vh;
  background-color: #f0efe9;
  font-family: 'Barlow', sans-serif;
}

/* ── Ticker bar ── */
.ticker-bar {
  background-color: #1e5c2a;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.55rem 2.5rem;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.ticker-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #6fcf7f;
  animation: pulse 2s infinite;
  display: inline-block;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.divider {
  color: rgba(255,255,255,0.35);
}

.ticker-right {
  font-size: 0.72rem;
  opacity: 0.8;
  letter-spacing: 0.06em;
}

/* ── Hero section ── */
.hero-section {
  padding: 2.5rem 2.5rem 1.5rem;
  max-width: 1400px;
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

.dot.green { background: #2d7a3a; animation: pulse 2s infinite; }

.hero-title-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.2rem;
}

.hero-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: clamp(2.8rem, 5vw, 4rem);
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

.btn-add {
  background: #111;
  color: #fff;
  border: none;
  padding: 0.6rem 1.3rem;
  border-radius: 6px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 1rem;
}
.btn-add:hover { background: #2d7a3a; }

/* ── Loading ── */
.loading-state {
  display: flex;
  justify-content: center;
  padding: 5rem;
}

.spinner-ring {
  width: 36px;
  height: 36px;
  border: 3px solid #ddd;
  border-top-color: #2d7a3a;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Cards grid ── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
  padding: 0 2.5rem 3rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* ── Court card ── */
.court-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e8e7e1;
  transition: transform 0.2s, box-shadow 0.2s;
}

.court-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
}

.card-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s;
}

.court-card:hover .card-image { transform: scale(1.04); }

.sport-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  background: rgba(30,30,30,0.75);
  backdrop-filter: blur(6px);
  color: #fff;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.78rem;
  letter-spacing: 0.1em;
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
}

.card-number {
  position: absolute;
  bottom: 12px;
  right: 14px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.1rem;
  color: rgba(255,255,255,0.7);
  letter-spacing: 0.05em;
}

.card-actions-overlay {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 0.4rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.court-card:hover .card-actions-overlay { opacity: 1; }

.icon-btn {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: none;
  background: rgba(255,255,255,0.9);
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s;
}
.icon-btn:hover { background: #fff; }
.icon-btn.danger { color: #e53e3e; }
.icon-btn.danger:hover { background: #fff0f0; }

/* ── Card body ── */
.card-body {
  padding: 1.2rem 1.4rem 1.4rem;
}

.court-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.35rem;
  color: #111;
  letter-spacing: -0.01em;
  margin-bottom: 0.2rem;
}

.court-location {
  font-size: 0.82rem;
  color: #999;
  margin-bottom: 1rem;
}

.court-meta {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.2rem;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.meta-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #aaa;
}

.meta-value {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  color: #111;
}

.meta-value.green { color: #2d7a3a; }

.btn-reserve {
  display: block;
  width: 100%;
  text-align: center;
  background-color: #1e5c2a;
  color: #fff;
  text-decoration: none;
  padding: 0.8rem;
  border-radius: 8px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 0.12em;
  transition: background-color 0.2s;
}

.btn-reserve:hover { background-color: #2d7a3a; }

/* ── Modal ── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-box {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 24px 60px rgba(0,0,0,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.4rem 1.6rem 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h2 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.4rem;
  color: #111;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1rem;
  color: #999;
  cursor: pointer;
  padding: 0.2rem;
}
.modal-close:hover { color: #111; }

.modal-body {
  padding: 1.2rem 1.6rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.field-group label {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #555;
}

.field-group input,
.field-group select,
.field-group textarea {
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  padding: 0.6rem 0.85rem;
  font-family: 'Barlow', sans-serif;
  font-size: 0.9rem;
  color: #111;
  outline: none;
  transition: border-color 0.2s;
  background: #fafafa;
}

.field-group input:focus,
.field-group select:focus,
.field-group textarea:focus {
  border-color: #2d7a3a;
  background: #fff;
}

.file-input {
  padding: 0.5rem !important;
  cursor: pointer;
}

.image-preview {
  width: 100%;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
  margin-top: 0.4rem;
}

/* Toggle switch */
.toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  margin-top: 0.3rem;
}

.toggle input { display: none; }

.toggle-slider {
  width: 44px;
  height: 24px;
  background: #ddd;
  border-radius: 12px;
  position: relative;
  transition: background 0.2s;
}

.toggle-slider::after {
  content: '';
  position: absolute;
  width: 18px;
  height: 18px;
  background: #fff;
  border-radius: 50%;
  top: 3px;
  left: 3px;
  transition: transform 0.2s;
}

.toggle input:checked + .toggle-slider { background: #2d7a3a; }
.toggle input:checked + .toggle-slider::after { transform: translateX(20px); }

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.6rem 1.4rem;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel {
  background: none;
  border: 1.5px solid #ddd;
  color: #555;
  padding: 0.6rem 1.3rem;
  border-radius: 8px;
  font-family: 'Barlow', sans-serif;
  font-size: 0.9rem;
  cursor: pointer;
  transition: border-color 0.2s;
}
.btn-cancel:hover { border-color: #999; }

.btn-save {
  background: #1e5c2a;
  color: #fff;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 8px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-save:hover { background: #2d7a3a; }

/* ── Responsive ── */
@media (max-width: 768px) {
  .ticker-bar { padding: 0.5rem 1rem; }
  .hero-section { padding: 1.5rem 1rem 1rem; }
  .cards-grid { padding: 0 1rem 2rem; grid-template-columns: 1fr; }
  .field-row { grid-template-columns: 1fr; }
}
</style>