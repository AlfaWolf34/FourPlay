<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const message = ref('')
const sent = ref(false)
const focusedField = ref(null)

const sendMessage = () => {
  if (!name.value || !email.value || !message.value) return
  // Aquí iría la llamada real a la API de contacto
  name.value = ''
  email.value = ''
  message.value = ''
  sent.value = true
  setTimeout(() => sent.value = false, 3000)
}
</script>

<template>
  <div class="contact-page">

    <!-- Main layout -->
    <div class="contact-layout">

      <!-- Left: Info -->
      <div class="info-panel">
        <div class="section-label">
          <span class="dot green"></span>
          CONTÁCTANOS
        </div>

        <h1 class="info-title">
          Estamos aquí<br />
          <span class="green">para ayudarte.</span>
        </h1>

        <p class="info-desc">
          ¿Tienes dudas sobre una cancha, tu reservación o la plataforma?
          Escríbenos y te respondemos a la brevedad.
        </p>

        <div class="contact-items">
          <div class="contact-item">
            <div class="contact-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                <circle cx="12" cy="10" r="3"/>
              </svg>
            </div>
            <div>
              <span class="item-label">UBICACIÓN</span>
              <span class="item-value">Monterrey, Nuevo León · México</span>
            </div>
          </div>

          <div class="contact-item">
            <div class="contact-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
            </div>
            <div>
              <span class="item-label">CORREO</span>
              <span class="item-value">contacto@4play.mx</span>
            </div>
          </div>

          <div class="contact-item">
            <div class="contact-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div>
              <span class="item-label">HORARIO DE CANCHAS</span>
              <span class="item-value">08:00 – 22:00 · Todos los días</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Form -->
      <div class="form-panel">
        <div class="form-box">
          <div class="form-header">
            <h2>Envíanos un mensaje</h2>
            <p>Te respondemos en menos de 24 horas.</p>
          </div>

          <div class="form-fields">
            <div class="field-group">
              <label>NOMBRE</label>
              <div class="input-wrapper" :class="{ focused: focusedField === 'name' }">
                <svg class="input-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                <input
                  v-model="name"
                  type="text"
                  placeholder="Tu nombre completo"
                  @focus="focusedField = 'name'"
                  @blur="focusedField = null"
                />
              </div>
            </div>

            <div class="field-group">
              <label>CORREO</label>
              <div class="input-wrapper" :class="{ focused: focusedField === 'email' }">
                <svg class="input-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                  <polyline points="22,6 12,13 2,6"/>
                </svg>
                <input
                  v-model="email"
                  type="email"
                  placeholder="tu@correo.com"
                  @focus="focusedField = 'email'"
                  @blur="focusedField = null"
                />
              </div>
            </div>

            <div class="field-group">
              <label>MENSAJE</label>
              <div class="input-wrapper textarea-wrapper" :class="{ focused: focusedField === 'msg' }">
                <textarea
                  v-model="message"
                  placeholder="Hola, me gustaría saber más sobre..."
                  rows="5"
                  @focus="focusedField = 'msg'"
                  @blur="focusedField = null"
                ></textarea>
              </div>
            </div>

            <button class="btn-send" @click="sendMessage">
              ENVIAR MENSAJE →
            </button>
          </div>
        </div>
      </div>

    </div>

    <!-- Toast de éxito -->
    <div class="toast" :class="{ show: sent }">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="20 6 9 17 4 12"/>
      </svg>
      ¡Mensaje enviado con éxito!
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.contact-page {
  min-height: 100vh;
  background-color: #f0efe9;
  font-family: 'Barlow', sans-serif;
}

/* ── Ticker ── */
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

.ticker-left { display: flex; align-items: center; gap: 0.75rem; }

.dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #6fcf7f;
  animation: pulse 2s infinite;
  display: inline-block;
}
.dot.green { background: #2d7a3a; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.divider { color: rgba(255,255,255,0.35); }
.ticker-right { font-size: 0.72rem; opacity: 0.8; letter-spacing: 0.06em; }

/* ── Layout ── */
.contact-layout {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 0;
  min-height: calc(100vh - 36px);
  max-width: 1300px;
  margin: 0 auto;
  padding: 4rem 2.5rem;
  align-items: center;
}

/* ── Info panel ── */
.info-panel {
  padding-right: 4rem;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  color: #2d7a3a;
  margin-bottom: 1rem;
}

.info-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: clamp(2.8rem, 4.5vw, 4rem);
  line-height: 1.0;
  color: #111;
  letter-spacing: -0.01em;
  margin-bottom: 1.4rem;
}

.info-title .green { color: #2d7a3a; }

.info-desc {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.65;
  margin-bottom: 2.5rem;
  max-width: 380px;
}

.contact-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  background: #fff;
  border: 1px solid #e8e7e1;
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
}

.contact-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #f0f9f2;
  border: 1px solid #d4edda;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2d7a3a;
  flex-shrink: 0;
}

.contact-item > div:last-child {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.item-label {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #2d7a3a;
}

.item-value {
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
}

/* ── Form panel ── */
.form-panel {
  display: flex;
  justify-content: flex-end;
}

.form-box {
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e8e7e1;
  padding: 2.2rem 2rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.06);
}

.form-header {
  margin-bottom: 1.8rem;
}

.form-header h2 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.6rem;
  color: #111;
  letter-spacing: -0.01em;
  margin-bottom: 0.3rem;
}

.form-header p {
  font-size: 0.88rem;
  color: #888;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.field-group label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #555;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #fafaf8;
  border: 1.5px solid #e0dfda;
  border-radius: 8px;
  padding: 0 1rem;
  height: 50px;
  gap: 0.65rem;
  transition: border-color 0.2s;
}

.input-wrapper.focused { border-color: #2d7a3a; }

.textarea-wrapper {
  height: auto;
  padding: 0.8rem 1rem;
  align-items: flex-start;
}

.input-icon { color: #aaa; flex-shrink: 0; }
.input-wrapper.focused .input-icon { color: #2d7a3a; }

.input-wrapper input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-family: 'Barlow', sans-serif;
  font-size: 0.92rem;
  color: #111;
}

.input-wrapper input::placeholder,
.input-wrapper textarea::placeholder { color: #bbb; }

.input-wrapper textarea {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-family: 'Barlow', sans-serif;
  font-size: 0.92rem;
  color: #111;
  resize: none;
  width: 100%;
  line-height: 1.6;
}

.btn-send {
  height: 52px;
  background-color: #1e5c2a;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.12em;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
  margin-top: 0.3rem;
}

.btn-send:hover { background-color: #2d7a3a; }

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
}

.toast.show {
  transform: translateY(0);
  opacity: 1;
}

/* ── Responsive ── */
@media (max-width: 900px) {
  .contact-layout {
    grid-template-columns: 1fr;
    padding: 2rem 1.2rem;
    gap: 2.5rem;
  }
  .info-panel { padding-right: 0; }
  .form-panel { justify-content: stretch; }
  .form-box { max-width: 100%; }
}
</style>