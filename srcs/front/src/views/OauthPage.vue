<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

if (route.query.token) localStorage.setItem('auth_token', (route.query.token as string));

const authChannel = new BroadcastChannel('auth_status');
authChannel.postMessage({ type: 'AUTH_SUCCESS' });

window.close();

</script>

<template>

</template>
