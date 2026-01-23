<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
  // import LandingPage from './views/LandingPage.vue';
  import ToastContainer from './components/ToastContainer.vue';
</script>

<template>
  <div class="container">
    <RouterView />
    <ToastContainer />
  </div>
</template>

<style lang="scss" scoped>
  .container{
    margin: 0 auto;
    max-width: 1920px;
    // max-width: $breakpoint-lg;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
// @media (max-width: $breakpoint-md) {
//     .container{
//     margin: auto;
//   }
// }
</style>
