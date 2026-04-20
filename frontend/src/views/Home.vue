<script setup>
import { ref, onMounted } from 'vue'
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

const canEdit = () => {
  return userRole.value === 1 || userRole.value === 2
}

const form = ref({
  id: null,
  name: '',
  location: '',
  sport_type: 'football',
  description: '',
  price_per_hour: '',
  is_available: true,
  open_time: '',
  close_time: ''
})

const openDialog = () => {
  isEdit.value = false

  form.value = {
    id: null,
    name: '',
    location: '',
    sport_type: 'football',
    price_per_hour: '',
    is_available: true,
    open_time: '',
    close_time: ''
  }

  imageFile.value = null
  imagePreview.value = null

  dialog.value = true
}

const editField = (field) => {
  isEdit.value = true

  form.value = {
    ...field
  }

  //muestra imagen actual (sea vieja URL o nueva)
  imagePreview.value = imageUrl(field.image)
  imageFile.value = null

  dialog.value = true
}

const handleImage = (event) => {
  console.log('event recibido:', event)

  const files = event.target.files
  console.log('files:', files)

  if (!files || files.length === 0) {
    console.log('No se seleccionó archivo')
    return
  }

  const selectedFile = files[0]
  console.log('Archivo seleccionado:', selectedFile)

  if (!selectedFile || !(selectedFile instanceof File)) {
    console.log('No es archivo válido', selectedFile)
    return
  }

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

  // SOLO si el usuario eligió nueva imagen
  if (imageFile.value) {
    formData.append('image', imageFile.value)
  }

  try {
    for (let pair of formData.entries()) {
      console.log(pair[0], pair[1])
    }
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
    console.log("ERROR:", error.response.data)
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

onMounted(async () => {
  try {
    await loadUser()
    await loadFields()
  } catch (error) {
    console.error("Error cargando canchas:", error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <v-container class="mt-8">

    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">Canchas Afiliadas</h1>
      </v-col>

      <v-btn v-if="canEdit()" color="primary" @click="openDialog">
        Nueva cancha
      </v-btn>
    </v-row>

    <!-- Loader -->
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary" />
      </v-col>
    </v-row>

    <!-- Listado -->
    <v-row v-else>
      <v-col v-for="field in fields" :key="field.id" cols="12" md="4">
        <v-card elevation="4" class="rounded-xl">

          <div class="d-flex justify-end" v-if="canEdit()">
            <v-btn icon @click="editField(field)">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <v-btn icon color="red" @click="deleteField(field.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </div>

          <v-img height="220" :src="imageUrl(field.image) || '/placeholder.jpg'" />

          <v-card-title>
            {{ field.name }}
          </v-card-title>

          <v-card-subtitle>
            {{ field.location }}
          </v-card-subtitle>

          <v-card-text>
            <div><strong>Horario:</strong> {{ field.open_time }} - {{ field.close_time }}</div>
            <div><strong>Precio:</strong> ${{ field.price_per_hour }}</div>
          </v-card-text>

          <v-card-actions>
            <v-btn color="primary" :to="`/courts/${field.id}`">
              Reservar
            </v-btn>
          </v-card-actions>

        </v-card>
      </v-col>
    </v-row>

    <!-- MODAL -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>

        <v-card-title>
          {{ isEdit ? 'Editar' : 'Nueva' }} Cancha
        </v-card-title>

        <v-card-text>

          <v-text-field v-model="form.name" label="Nombre" />
          <v-select v-model="form.sport_type" :items="[
            { title: 'Fútbol', value: 'football' },
            { title: 'Basquetbol', value: 'basketball' },
            { title: 'Tenis', value: 'tennis' },
            { title: 'Voleibol', value: 'volleyball' },
            { title: 'Otro', value: 'other' }
          ]" label="Tipo de cancha" />

          <v-textarea v-model="form.description" label="Descripción" rows="3" />
          <v-text-field v-model="form.location" label="Ubicación" />
          <v-text-field v-model="form.price_per_hour" label="Precio por hora" type="number" />

          <v-text-field v-model="form.open_time" label="Hora apertura" type="time" />
          <v-text-field v-model="form.close_time" label="Hora cierre" type="time" />

          <v-switch v-model="form.is_available" label="Disponible" />

          <v-file-input label="Imagen" accept="image/*" @change="handleImage" />

          <v-img v-if="imagePreview" :src="imagePreview" height="150" class="mt-3 rounded" />

        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="saveField">Guardar</v-btn>
        </v-card-actions>

      </v-card>
    </v-dialog>

  </v-container>
</template>