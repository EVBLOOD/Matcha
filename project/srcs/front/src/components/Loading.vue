
<script setup lang="ts">
    defineProps({
        size: {
            type: Number,
            default: 40,
        },
        color: {
            type: String,
            default: '#3498db',
        },
    })
</script>

<template>
  <div class="loading-wrapper">
    <div class="spinner" :style="{ width: size + 'px', height: size + 'px', borderColor: color + ' transparent transparent transparent'}"></div>
  </div>
</template>


<style scoped lang="scss">
.loading-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.spinner {
  border: 4px solid;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
