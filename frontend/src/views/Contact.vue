<script setup>
import { ref } from 'vue'
 
const name    = ref('')
const email   = ref('')
const message = ref('')
const sent    = ref(false)
 
const sendMessage = () => {
  if (!name.value || !email.value || !message.value) return
  // Aquí iría la llamada real a la API de contacto
  name.value    = ''
  email.value   = ''
  message.value = ''
  sent.value    = true
}
</script>
 
<template>
     <v-container class="py-10">
    <v-row justify="center">
      <v-col cols="12" md="8">
 
        <h1 class="text-h4 mb-4">Contactactanos!</h1>
 
        <p class="text-body-1 mb-4">
         Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium magnam suscipit rem temporibus omnis dolor deserunt ea, debitis dignissimos, tempora corrupti! Ipsam, mollitia quam provident autem eos et exercitationem atque!
        </p>
 
        <p class="text-body-1 mb-4">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium magnam suscipit rem temporibus omnis dolor deserunt ea, debitis dignissimos, tempora corrupti! Ipsam, mollitia quam provident autem eos et exercitationem atque!
        </p>
 
        <p class="text-body-1">
         Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis eum reiciendis impedit vel, laborum officia maiores, officiis adipisci culpa cupiditate nihil soluta voluptates unde? Sed molestias dolorem quisquam exercitationem. Provident!
        </p>
 
      </v-col>
    </v-row>
  </v-container>
 
  <v-container class="py-10">
    <v-row justify="center">
      <v-col cols="12" md="6">
 
        <v-card class="pa-6 rounded-xl">
          <h1 class="text-h5 mb-4">Contacto</h1>
 
          <v-text-field
            v-model="name"
            label="Nombre"
            variant="outlined"
            class="mb-3"
          />
 
          <v-text-field
            v-model="email"
            label="Correo"
            variant="outlined"
            class="mb-3"
          />
 
          <v-textarea
            v-model="message"
            label="Mensaje"
            variant="outlined"
            class="mb-4"
          />
 
          <v-btn color="primary" block @click="sendMessage">
            Enviar mensaje
          </v-btn>
 
        </v-card>
 
      </v-col>
    </v-row>
  </v-container>
 
  <!-- Snackbar ¡Enviado! -->
  <v-snackbar
    v-model="sent"
    color="success"
    timeout="3000"
    location="bottom right"
  >
    <v-icon class="mr-2">mdi-check-circle-outline</v-icon>
    ¡Contacto enviado!
  </v-snackbar>
</template>