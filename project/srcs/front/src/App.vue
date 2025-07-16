<script setup lang="ts">
// import { RouterLink, RouterView } from 'vue-router';
  import LandingPage from './views/LandingPage.vue';
</script>

<template>
  <div class="container">
    <LandingPage />
  </div>
</template>

<style lang="scss" scoped>
  .container{
    margin: 0 auto;
    max-width: $breakpoint-lg;
  }
</style>
