<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const focusedField = ref(null)

const register = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    await api.post('users/', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    router.push('/login')
  } catch (error) {
    console.log(error.response)
    errorMessage.value = 'Error al registrar usuario. Intenta con otro nombre de usuario.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">

    <!-- Mini navbar -->
    <div class="top-bar">
      <div class="logo">
        <span class="logo-4">4</span><span class="logo-play">PLAY</span>
        <div class="logo-divider"></div>
        <div class="logo-sub">
          <span class="logo-tagline">RESERVA DE CANCHAS</span>
          <span class="logo-city">Monterrey</span>
        </div>
      </div>
    </div>

    <!-- Form centered -->
    <div class="page-body">
      <div class="form-card">
        <h2 class="form-title">Crear una cuenta</h2>

        <div class="field-group">
          <div class="input-wrapper" :class="{ focused: focusedField === 'user' }">
            <input
              v-model="username"
              type="text"
              placeholder="Usuario"
              @focus="focusedField = 'user'"
              @blur="focusedField = null"
            />
          </div>
        </div>

        <div class="field-group">
          <div class="input-wrapper" :class="{ focused: focusedField === 'email' }">
            <input
              v-model="email"
              type="email"
              placeholder="Correo"
              @focus="focusedField = 'email'"
              @blur="focusedField = null"
            />
          </div>
        </div>

        <div class="field-group">
          <div class="input-wrapper" :class="{ focused: focusedField === 'pass' }">
            <input
              v-model="password"
              type="password"
              placeholder="Contraseña"
              @focus="focusedField = 'pass'"
              @blur="focusedField = null"
            />
          </div>
        </div>

        <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>

        <button class="btn-register" :class="{ loading }" @click="register" :disabled="loading">
          <span v-if="!loading">Registrarse</span>
          <span v-else class="spinner"></span>
        </button>

        <button class="btn-login-link" @click="router.push('/login')">
          Ya tengo cuenta
        </button>
      </div>
    </div>

  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

* { box-sizing: border-box; margin: 0; padding: 0; }

.register-page {
  min-height: 100vh;
  background: #f0efe9;
  font-family: 'Barlow', sans-serif;
  display: flex;
  flex-direction: column;
}

/* ── Top bar ── */
.top-bar {
  background: #fff;
  border-bottom: 1px solid #e8e7e1;
  padding: 0 2.5rem;
  height: 72px;
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
}

.logo-4 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 2.4rem;
  color: #2d7a3a;
  line-height: 1;
}

.logo-play {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 2.4rem;
  color: #111;
  line-height: 1;
}

.logo-divider {
  width: 1px;
  height: 32px;
  background: #ddd;
  margin: 0 0.5rem;
}

.logo-sub {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.logo-tagline {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.68rem;
  letter-spacing: 0.12em;
  color: #2d7a3a;
}

.logo-city {
  font-size: 0.76rem;
  color: #999;
}

/* ── Page body ── */
.page-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
}

/* ── Form card ── */
.form-card {
  background: #c5d9c8;
  border-radius: 16px;
  padding: 2.2rem 2rem;
  width: 100%;
  max-width: 460px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-title {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 1.6rem;
  color: #111;
  text-align: center;
  letter-spacing: -0.01em;
  margin-bottom: 0.3rem;
}

/* ── Inputs ── */
.field-group { width: 100%; }

.input-wrapper {
  background: #fff;
  border: 1.5px solid transparent;
  border-radius: 10px;
  height: 52px;
  display: flex;
  align-items: center;
  padding: 0 1.1rem;
  transition: border-color 0.2s;
}

.input-wrapper.focused { border-color: #1e5c2a; }

.input-wrapper input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-family: 'Barlow', sans-serif;
  font-size: 0.95rem;
  color: #111;
}

.input-wrapper input::placeholder { color: #aaa; }

/* ── Error ── */
.error-msg {
  font-size: 0.82rem;
  color: #dc2626;
  text-align: center;
  background: #fff5f5;
  border-radius: 8px;
  padding: 0.5rem 0.8rem;
}

/* ── Button ── */
.btn-register {
  height: 50px;
  background: #1e5c2a;
  color: #fff;
  border: none;
  border-radius: 10px;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 0.2rem;
}

.btn-register:hover { background: #2d7a3a; }
.btn-register.loading { opacity: 0.7; cursor: not-allowed; }

.spinner {
  width: 18px; height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Ya tengo cuenta ── */
.btn-login-link {
  background: none;
  border: none;
  font-family: 'Barlow', sans-serif;
  font-size: 0.9rem;
  color: #1e5c2a;
  text-decoration: underline;
  cursor: pointer;
  text-align: center;
  padding: 0.2rem;
  transition: color 0.2s;
}

.btn-login-link:hover { color: #111; }

/* ── Responsive ── */
@media (max-width: 500px) {
  .top-bar { padding: 0 1rem; }
  .form-card { padding: 1.6rem 1.2rem; }
}
</style>