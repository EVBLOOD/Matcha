<script setup>
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';

</script>

<template>
    <div class="content">
        Messages Page is this
    </div>
</template>

<style lang="scss" scoped>
    .content{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        width: 100%;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

