<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

if (route.query.token) localStorage.setItem('auth_token', (route.query.token as string));
router.push('/')

</script>

<template>

</template>
