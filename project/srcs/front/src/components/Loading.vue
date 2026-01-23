
<script setup lang="ts">
  import { ref, onMounted, onUnmounted, watch } from 'vue'

  const { size = 70, color = '#E2BDF6', duration = 3000, step = 100 } = defineProps<{size?: number, color?: string, duration?: number, step?: number}>()

  const emit = defineEmits<{
    (e: 'finished'): void
  }>()

  const elapsed = ref(0)
  let timer: number | undefined

  onMounted(() => {
    timer = window.setInterval(() => {
      elapsed.value += step ?? 100

      if (elapsed.value >= (duration ?? 3000)) {
        clearInterval(timer)
        emit('finished')
      }
    }, step ?? 100)
  })

  onUnmounted(() => {
    if (timer) clearInterval(timer)
  })

</script>

<template>
  <div class="loading-wrapper">
    <div class="spinner" :style="{ width: size + 'px', height: size + 'px', borderColor: color + ' transparent transparent transparent'}"></div>
    <!-- <p class="timer">{{ Math.ceil(elapsed / 1000) }}s</p> -->
  </div>
</template>


<style scoped lang="scss">
.loading-wrapper {
  position: relative;
  // background-color: #2121219c;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  // z-index: 9999;
}

.spinner {
  border: 4px solid;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg) }
  100% { transform: rotate(360deg) }
}
</style>
