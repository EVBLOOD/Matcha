import { ref } from 'vue'

interface Coords {
  latitude: number | null
  longitude: number | null
}

export function usePreciseLocation() {
  const coords = ref<Coords>({ latitude: null, longitude: null })

  const getPreciseLocation = () : Promise<Coords | null> => { return new Promise((resolve) =>
  {

      if (!("geolocation" in navigator)) {
        resolve(null);
        return
      }

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          coords.value = {
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude
          }
          resolve(coords.value);
        },
        (err) => {
          resolve(null);
        },
        { enableHighAccuracy: true }
      )
  })
  }

  return { coords, getPreciseLocation }
}

