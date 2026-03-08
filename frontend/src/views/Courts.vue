<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

/* 🎠 Carousel */
import 'vue3-carousel/carousel.css'
import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel'

const route = useRoute()

const court = ref(null)
const loading = ref(true)

/* imágenes demo (luego vendrán del backend) */
const images = ref([])

const carouselConfig = {
  height: 300,
  itemsToShow: 1,
  gap: 10,
  wrapAround: true
}

onMounted(async () => {
  try {
    const response = await api.get(`fields/${route.params.id}/`)
    court.value = response.data

    // imágenes fake temporalmente
    images.value = Array.from({ length: 5 }, (_, index) => ({
      id: index,
      url: `https://picsum.photos/seed/${route.params.id}-${index}/900/500`
    }))

  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <v-container v-if="!loading">

    <v-card v-if="court" class="rounded-xl overflow-hidden">

      <Carousel v-bind="carouselConfig">
        <Slide v-for="image in images" :key="image.id">
          <img :src="image.url" class="carousel-img" />
        </Slide>

        <template #addons>
          <Navigation />
          <Pagination />
        </template>
      </Carousel>

      <!-- INFO -->
      <v-card-title class="text-h4">
        {{ court.name }}
      </v-card-title>

      <v-card-text>

        <p class="mb-2">
          📍 {{ court.location }}
        </p>

        <p class="mb-4">
          📝 {{ court.description || 'Sin descripción disponible' }}
        </p>

        <v-divider class="my-4" />

        <h3 class="text-h6 mb-3">Horarios disponibles</h3>

        <v-chip class="ma-1">16:00</v-chip>
        <v-chip class="ma-1">17:00</v-chip>
        <v-chip class="ma-1">18:00</v-chip>
        <v-chip class="ma-1">19:00</v-chip>

      </v-card-text>

      <v-card-actions>
        <v-btn color="primary">
          Reservar cancha
        </v-btn>
      </v-card-actions>

    </v-card>

  </v-container>

  <v-container v-else class="text-center">
    <v-progress-circular indeterminate />
  </v-container>
</template>