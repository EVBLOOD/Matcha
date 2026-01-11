<script setup lang="ts">

// import { onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

console.log(route.params.token)

localStorage.setItem('auth_token', (route.params.token as string));
router.push('/')

// onMounted()
</script>

<template>

</template>
