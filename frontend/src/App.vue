<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from './services/api'

const router = useRouter()
const route = useRoute()
const user = ref(null)
const token = ref(null)
const dropdownOpen = ref(false)

const ADMIN = 1
const OWNER = 2
const USER = 3

const isAuthenticated = computed(() => !!token.value)

const canViewAdminSections = computed(() => {
  return user.value?.role === ADMIN || user.value?.role === OWNER
})

const userInitial = computed(() => {
  return user.value?.username?.charAt(0).toUpperCase() || '?'
})

const loadUser = async () => {
  try {
    const response = await api.get('users/me/')
    user.value = response.data
  } catch (error) {
    console.error('Error obteniendo usuario:', error)
    logout()
  }
}

const logout = () => {
  localStorage.removeItem('token')
  token.value = null
  user.value = null
  dropdownOpen.value = false
  router.push('/login')
}

const isActive = (path) => route.path === path

onMounted(async () => {
  const savedToken = localStorage.getItem('token')
  if (savedToken) {
    token.value = savedToken
    loadUser()
  }

  window.addEventListener('login', () => {
    token.value = localStorage.getItem('token')
    loadUser()
  })

  // Cerrar dropdown al hacer click fuera
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-menu')) {
      dropdownOpen.value = false
    }
  })
})
</script>

<template>
  <div class="app-wrapper">

    <!-- ── Navbar (solo si está logueado) ── -->
    <header v-if="isAuthenticated" class="site-header">


      <!-- Main navbar -->
      <nav class="navbar">

        <!-- Logo -->
        <router-link to="/" class="logo">
          <span class="logo-4">4</span><span class="logo-play">PLAY</span>
          <div class="logo-divider"></div>
          <div class="logo-sub">
            <span class="logo-tagline">RESERVA DE CANCHAS</span>
            <span class="logo-city">Monterrey</span>
          </div>
        </router-link>

        <!-- Nav links -->
        <div class="nav-links">
          <router-link to="/" class="nav-link" :class="{ active: isActive('/') }">
            INICIO
          </router-link>
          <router-link to="/mis-reservaciones" class="nav-link" :class="{ active: isActive('/mis-reservaciones') }">
            RESERVACIONES
          </router-link>
          <router-link v-if="canViewAdminSections" to="/calendario" class="nav-link" :class="{ active: isActive('/calendario') }">
            CALENDARIO
          </router-link>
          <router-link v-if="canViewAdminSections" to="/estadisticas" class="nav-link" :class="{ active: isActive('/estadisticas') }">
            ESTADÍSTICAS
          </router-link>
          <router-link to="/nosotros" class="nav-link" :class="{ active: isActive('/nosotros') }">
            NOSOTROS
          </router-link>
          <router-link to="/contacto" class="nav-link" :class="{ active: isActive('/contacto') }">
            CONTACTO
          </router-link>
        </div>

        <!-- User menu -->
        <div class="user-menu" @click="dropdownOpen = !dropdownOpen">
          <div class="user-pill">
            <div class="user-avatar">{{ userInitial }}</div>
            <span class="user-name">{{ user?.username || 'Usuario' }}</span>
            <svg class="chevron" :class="{ rotated: dropdownOpen }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"/>
            </svg>
          </div>

          <!-- Dropdown -->
          <div class="dropdown" :class="{ open: dropdownOpen }">
            <button class="dropdown-item logout" @click="logout">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                <polyline points="16 17 21 12 16 7"/>
                <line x1="21" y1="12" x2="9" y2="12"/>
              </svg>
              Cerrar sesión
            </button>
          </div>
        </div>

      </nav>
    </header>

    <!-- Page content -->
    <main :class="{ 'with-header': isAuthenticated }">
      <router-view />
    </main>

  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, #app {
  width: 100%;
  height: 100%;
  background: #f0efe9;
}

/* Quitar estilos de Vuetify */
.v-application {
  background: transparent !important;
  font-family: 'Barlow', sans-serif !important;
}
.v-application__wrap { background: transparent !important; min-height: unset !important; }
.v-main { padding: 0 !important; }
.v-main__scroller { padding: 0 !important; }
</style>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  background: #f0efe9;
  font-family: 'Barlow', sans-serif;
}

/* ── Header ── */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  box-shadow: 0 1px 0 #e8e7e1;
}

/* Ticker */
.ticker-bar {
  background-color: #1e5c2a;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.45rem 2.5rem;
  font-family: 'Barlow Condensed', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.ticker-left { display: flex; align-items: center; gap: 0.7rem; }

.ticker-dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: #6fcf7f;
  animation: pulse 2s infinite;
  display: inline-block;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.ticker-divider { color: rgba(255,255,255,0.3); }
.ticker-right { font-size: 0.7rem; opacity: 0.75; letter-spacing: 0.05em; }

/* Navbar */
.navbar {
  display: flex;
  align-items: center;
  padding: 0 2.5rem;
  height: 72px;
  gap: 2rem;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  flex-shrink: 0;
}

.logo-4 {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 2.8rem;
  color: #2d7a3a;
  line-height: 1;
}

.logo-play {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 900;
  font-size: 2.8rem;
  color: #111;
  line-height: 1;
}

.logo-divider {
  width: 1px;
  height: 36px;
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
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  color: #2d7a3a;
}

.logo-city {
  font-size: 0.78rem;
  color: #999;
}

/* Nav links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-left: auto;
}

.nav-link {
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 700;
  font-size: 0.82rem;
  letter-spacing: 0.1em;
  color: #555;
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  position: relative;
  transition: color 0.2s;
}

.nav-link:hover { color: #111; }

.nav-link.active {
  color: #111;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 2px;
  background: #2d7a3a;
  border-radius: 2px;
}

/* User menu */
.user-menu {
  position: relative;
  flex-shrink: 0;
  margin-left: 1rem;
  cursor: pointer;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #111;
  color: #fff;
  padding: 0.45rem 0.9rem 0.45rem 0.45rem;
  border-radius: 50px;
  transition: background 0.2s;
}

.user-pill:hover { background: #222; }

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #2d7a3a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Barlow Condensed', sans-serif;
  font-weight: 800;
  font-size: 0.85rem;
  color: #fff;
}

.user-name {
  font-family: 'Barlow', sans-serif;
  font-size: 0.85rem;
  font-weight: 500;
}

.chevron {
  transition: transform 0.2s;
  opacity: 0.6;
}
.chevron.rotated { transform: rotate(180deg); }

/* Dropdown */
.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: #fff;
  border: 1px solid #e8e7e1;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  min-width: 160px;
  overflow: hidden;
  opacity: 0;
  transform: translateY(-6px);
  pointer-events: none;
  transition: all 0.18s ease;
}

.dropdown.open {
  opacity: 1;
  transform: translateY(0);
  pointer-events: all;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  font-family: 'Barlow', sans-serif;
  font-size: 0.88rem;
  color: #333;
  cursor: pointer;
  transition: background 0.15s;
  text-align: left;
}

.dropdown-item:hover { background: #f5f5f3; }
.dropdown-item.logout { color: #e53e3e; }
.dropdown-item.logout:hover { background: #fff5f5; }

/* Main content */
main { width: 100%; }
main.with-header { min-height: calc(100vh - 108px); }

/* Responsive */
@media (max-width: 900px) {
  .navbar { padding: 0 1rem; gap: 1rem; }
  .ticker-bar { padding: 0.45rem 1rem; }
  .nav-links { gap: 0; }
  .nav-link { font-size: 0.75rem; padding: 0.4rem 0.5rem; }
  .logo-4, .logo-play { font-size: 2rem; }
  .logo-divider, .logo-sub { display: none; }
}
</style>