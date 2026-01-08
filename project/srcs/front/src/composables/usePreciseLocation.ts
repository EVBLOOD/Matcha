import { ref } from 'vue'

interface Coords {
  latitude: number | null
  longitude: number | null
}

export function usePreciseLocation() {
  const coords = ref<Coords>({ latitude: null, longitude: null })
  const error = ref<string | null>(null)
  const isLoading = ref(false)

  const getPreciseLocation = () => {
    isLoading.value = true
    
    if (!("geolocation" in navigator)) {
      error.value = "Geolocation service is not supported"
      isLoading.value = false
      return
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        coords.value = {
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude
        }
        isLoading.value = false
      },
      (err) => {
        error.value = err.message
        isLoading.value = false
      },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  return { coords, error, isLoading, getPreciseLocation }
}
