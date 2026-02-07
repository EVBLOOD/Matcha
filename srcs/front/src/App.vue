<script setup lang="ts">
import { RouterView } from 'vue-router';
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
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

</style>
