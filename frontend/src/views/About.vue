<template>
<div class="about-page">
 
    <!-- Main layout -->
<div class="about-layout">
 
      <!-- Left: Text info -->
<div class="info-panel">
<div class="section-label">
<span class="dot green"></span>

          SOBRE NOSOTROS
</div>
 
        <h1 class="info-title">

          Conectamos<br />

          jugadores con<br />
<span class="green">canchas.</span>
</h1>
 
        <div class="info-paragraphs">
<p>

            4Play es una plataforma digital diseñada para facilitar la reserva de

            canchas deportivas de forma rápida y sencilla.
</p>
<p>

            Nuestro objetivo es conectar jugadores y espacios deportivos mediante

            una experiencia moderna, intuitiva y accesible desde cualquier dispositivo.
</p>
<p>

            Actualmente el proyecto se encuentra en desarrollo, incorporando nuevas

            funcionalidades para mejorar la gestión de reservas y la experiencia de los

            usuarios.
</p>
</div>
</div>
 
      <!-- Right: Feature cards -->
<div class="features-panel">
 
        <div class="feature-card">
<div class="feature-icon">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
<circle cx="12" cy="12" r="10"/>
<polyline points="12 6 12 12 16 14"/>
</svg>
</div>
<div class="feature-text">
<h3>Reserva en segundos</h3>
<p>Elige tu cancha, selecciona el horario y confirma tu reserva en menos de un minuto.</p>
</div>
</div>
 
        <div class="feature-card">
<div class="feature-icon">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
<circle cx="9" cy="7" r="4"/>
<path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
<path d="M16 3.13a4 4 0 0 1 0 7.75"/>
</svg>
</div>
<div class="feature-text">
<h3>Para jugadores reales</h3>
<p>Diseñado para jugadores que no pierden tiempo. Disponibilidad en tiempo real, sin llamadas.</p>
</div>
</div>
 
        <div class="feature-card">
<div class="feature-icon">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
<polyline points="9 22 9 12 15 12 15 22"/>
</svg>
</div>
<div class="feature-text">
<h3>Múltiples canchas</h3>
<p>Fútbol 5, 7 y 11 en Monterrey. Todas las modalidades disponibles en un solo lugar.</p>
</div>
</div>
 
      </div>
</div>
 
    <!-- Stats bar -->
<div class="stats-bar">
<div class="stat-item">
<span class="stat-number">3</span>
<span class="stat-label">CANCHAS ACTIVAS</span>
</div>
<div class="stat-divider"></div>
<div class="stat-item">
<span class="stat-number">$280</span>
<span class="stat-label">PRECIO DESDE / HR</span>
</div>
<div class="stat-divider"></div>
<div class="stat-item">
<span class="stat-number">MTY</span>
<span class="stat-label">MONTERREY, NL</span>
</div>
<div class="stat-divider"></div>
<div class="stat-item">
<span class="stat-number green">24/7</span>
<span class="stat-label">RESERVAS EN LÍNEA</span>
</div>
</div>
 
  </div>
</template>
 
<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800;900&family=Barlow:wght@400;500;600&display=swap%27');
 
* { box-sizing: border-box; margin: 0; padding: 0; }
 
.about-page {

  min-height: 100vh;

  background-color: #f0efe9;

  font-family: 'Barlow', sans-serif;

  display: flex;

  flex-direction: column;

  justify-content: space-between;

}
 
/* ── Main layout ── */

.about-layout {

  display: grid;

  grid-template-columns: 1fr 1.1fr;

  gap: 4rem;

  padding: 4rem 2.5rem 3rem;

  max-width: 1300px;

  margin: 0 auto;

  width: 100%;

  align-items: center;

  flex: 1;

}
 
/* ── Left panel ── */

.info-panel {}
 
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
 
.dot {

  width: 7px; height: 7px;

  border-radius: 50%;

  display: inline-block;

}

.dot.green {

  background: #2d7a3a;

  animation: pulse 2s infinite;

}
 
@keyframes pulse {

  0%, 100% { opacity: 1; }

  50% { opacity: 0.4; }

}
 
.info-title {

  font-family: 'Barlow Condensed', sans-serif;

  font-weight: 900;

  font-size: clamp(2.8rem, 4.5vw, 4rem);

  line-height: 1.0;

  color: #111;

  letter-spacing: -0.01em;

  margin-bottom: 2rem;

}
 
.info-title .green { color: #2d7a3a; }
 
.info-paragraphs {

  display: flex;

  flex-direction: column;

  gap: 1rem;

}
 
.info-paragraphs p {

  font-size: 0.95rem;

  color: #555;

  line-height: 1.7;

  max-width: 480px;

}
 
/* ── Right panel: feature cards ── */

.features-panel {

  display: flex;

  flex-direction: column;

  gap: 1rem;

}
 
.feature-card {

  background: #fff;

  border: 1px solid #e8e7e1;

  border-radius: 14px;

  padding: 1.4rem 1.5rem;

  display: flex;

  align-items: flex-start;

  gap: 1.2rem;

  transition: transform 0.2s, box-shadow 0.2s;

}
 
.feature-card:hover {

  transform: translateY(-2px);

  box-shadow: 0 8px 24px rgba(0,0,0,0.07);

}
 
.feature-icon {

  width: 42px;

  height: 42px;

  border-radius: 10px;

  background: #f0f9f2;

  border: 1px solid #d4edda;

  display: flex;

  align-items: center;

  justify-content: center;

  color: #2d7a3a;

  flex-shrink: 0;

}
 
.feature-text h3 {

  font-family: 'Barlow Condensed', sans-serif;

  font-weight: 800;

  font-size: 1.05rem;

  color: #111;

  letter-spacing: -0.01em;

  margin-bottom: 0.3rem;

}
 
.feature-text p {

  font-size: 0.88rem;

  color: #777;

  line-height: 1.6;

}
 
/* ── Stats bar ── */

.stats-bar {

  background-color: #1a3d24;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 2.2rem 2.5rem;

  gap: 0;

}
 
.stat-item {

  display: flex;

  flex-direction: column;

  align-items: center;

  gap: 0.4rem;

  flex: 1;

  text-align: center;

}
 
.stat-number {

  font-family: 'Barlow Condensed', sans-serif;

  font-weight: 900;

  font-size: clamp(2rem, 3.5vw, 2.8rem);

  color: #fff;

  letter-spacing: -0.01em;

  line-height: 1;

}
 
.stat-number.green { color: #4caf62; }
 
.stat-label {

  font-family: 'Barlow Condensed', sans-serif;

  font-weight: 700;

  font-size: 0.68rem;

  letter-spacing: 0.12em;

  color: rgba(255,255,255,0.5);

}
 
.stat-divider {

  width: 1px;

  height: 50px;

  background: rgba(255,255,255,0.15);

  flex-shrink: 0;

}
 
/* ── Responsive ── */

@media (max-width: 900px) {

  .about-layout {

    grid-template-columns: 1fr;

    padding: 2rem 1.2rem;

    gap: 2rem;

  }
 
  .stats-bar {

    flex-wrap: wrap;

    gap: 1.5rem;

    padding: 1.8rem 1rem;

  }
 
  .stat-divider { display: none; }

  .stat-item { flex: 0 0 45%; }

}
</style>
 