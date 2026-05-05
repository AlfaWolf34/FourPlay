<template>
  <div class="login-page">
    <!-- Panel izquierdo oscuro -->
    <div class="left-panel">
      <div class="brand">
        <div class="brand-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" stroke="white" stroke-width="2"/>
            <circle cx="12" cy="12" r="4" fill="white"/>
          </svg>
        </div>
        <span class="brand-name">4PLAY</span>
      </div>

      <div class="hero-text">
        <h1>
          <span class="white">RESERVA</span><br />
          <span class="white">TU</span><br />
          <span class="white">CANCHA.</span>
        </h1>
        <p class="tagline">
          La plataforma para jugadores que no pierden tiempo. Elige, reserva, juega.
        </p>
      </div>

      <!-- Decorative elements -->
      <div class="deco-circle deco-1"></div>
      <div class="deco-circle deco-2"></div>
    </div>

    <!-- Panel derecho claro -->
    <div class="right-panel">
      <div class="form-container">
        <div class="form-header">
          <h2>Bienvenido</h2>
          <p>Ingresa tus datos para acceder a tu cuenta</p>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="field-group">
            <label>USUARIO</label>
            <div class="input-wrapper" :class="{ focused: focusedField === 'user' }">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="1.5"/>
              </svg>
              <input
                v-model="form.username"
                type="text"
                placeholder="Ingresa tu usuario"
                @focus="focusedField = 'user'"
                @blur="focusedField = null"
              />
            </div>
          </div>

          <div class="field-group">
            <label>CONTRASEÑA</label>
            <div class="input-wrapper" :class="{ focused: focusedField === 'pass' }">
              <svg class="input-icon" width="16" height="16" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" stroke="currentColor" stroke-width="1.5"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Ingresa tu contraseña"
                @focus="focusedField = 'pass'"
                @blur="focusedField = null"
              />
              <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="1.5"/>
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.5"/>
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
          </div>

          <button type="submit" class="btn-submit" :class="{ loading }">
            <span v-if="!loading">ENTRAR →</span>
            <span v-else class="spinner"></span>
          </button>

          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

          <p class="register-link">
            ¿No tienes cuenta?
            <router-link to="/register">Regístrate</router-link>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const form = reactive({ username: '', password: '' })
const focusedField = ref(null)
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
  loading.value = true
  errorMessage.value = ''
  try {
    const response = await api.post('token/', form)
    const token = response.data.access
    localStorage.setItem('token', token)
    window.dispatchEvent(new Event('login'))
    router.push('/')
  } catch (err) {
    console.error('Error al iniciar sesión:', err)
    if (err.response && err.response.status === 401) {
      errorMessage.value = 'Usuario o contraseña incorrectos'
    } else {
      errorMessage.value = 'Error al iniciar sesión. Inténtalo de nuevo.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.login-page {
  display: flex;
  min-height: 100vh;
  width: 100vw;
}

/* ── Panel izquierdo ── */
.left-panel {
  width: 47%;
  background-color: #1a1a1a;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2rem 2.5rem 3rem;
  position: relative;
  overflow: hidden;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  z-index: 1;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background-color: #2d7a3a;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: 0.12em;
  color: #ffffff;
}

.hero-text {
  z-index: 1;
}

.hero-text h1 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: clamp(3.5rem, 6vw, 5.5rem);
  line-height: 0.95;
  color: #ffffff;
  letter-spacing: -0.01em;
  margin-bottom: 1.2rem;
}

.hero-text h1 span.white {
  color: #ffffff;
}

.tagline {
  color: #888;
  font-size: 0.9rem;
  line-height: 1.55;
  max-width: 280px;
}

/* Decoraciones */
.deco-circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.06;
  background: #4caf62;
}
.deco-1 {
  width: 400px;
  height: 400px;
  top: -100px;
  right: -150px;
}
.deco-2 {
  width: 250px;
  height: 250px;
  bottom: 60px;
  right: -80px;
}

/* ── Panel derecho ── */
.right-panel {
  flex: 1;
  background-color: #f5f4f0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
}

.form-container {
  width: 100%;
  max-width: 420px;
}

.form-header {
  margin-bottom: 2.5rem;
}

.form-header h2 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 2.2rem;
  color: #111;
  letter-spacing: -0.01em;
  margin-bottom: 0.4rem;
}

.form-header p {
  color: #888;
  font-size: 0.92rem;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.field-group label {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  color: #555;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #fff;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  padding: 0 1rem;
  height: 52px;
  gap: 0.65rem;
  transition: border-color 0.2s;
}

.input-wrapper.focused {
  border-color: #2d7a3a;
}

.input-icon {
  color: #aaa;
  flex-shrink: 0;
  transition: color 0.2s;
}

.input-wrapper.focused .input-icon {
  color: #2d7a3a;
}

.input-wrapper input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-family: 'Barlow', sans-serif;
  font-size: 0.95rem;
  color: #111;
}

.input-wrapper input::placeholder {
  color: #bbb;
}

.toggle-password {
  background: none;
  border: none;
  cursor: pointer;
  color: #aaa;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}

.toggle-password:hover {
  color: #555;
}

/* Botón submit */
.btn-submit {
  height: 52px;
  background-color: #2D7A3A;
  color: white;
  border: none;
  border-radius: 8px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.12em;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  margin-top: 0.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-submit:hover {
  background-color: #2D7A3A;
}

.btn-submit:active {
  transform: scale(0.99);
}

.btn-submit.loading {
  opacity: 0.75;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Registro link */
.register-link {
  text-align: center;
  font-size: 0.9rem;
  color: #666;
}

.register-link a {
  color: #2D7A3A;
  font-weight: 600;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Error message */
.error-message {
  color: #d32f2f;
  font-size: 0.9rem;
  text-align: center;
  margin-top: 1rem;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .login-page {
    flex-direction: column;
  }

  .left-panel {
    width: 100%;
    min-height: 240px;
    padding: 1.8rem;
    justify-content: flex-start;
    gap: 1.5rem;
  }

  .hero-text h1 {
    font-size: 3rem;
  }

  .right-panel {
    padding: 2.5rem 1.5rem;
  }
}
</style>