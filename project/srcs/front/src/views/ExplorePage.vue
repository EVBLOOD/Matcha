<script setup>
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';

</script>

<template>
    <div class="page">
        <div class="content">
            Explore Page is this
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .page{
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 40px 20px;
        .content {
            overflow: hidden;
            p {
                margin-bottom: 30px;
            }
        }
        .title{
            font-weight: 700;
            font-size: 40px;
        }
        .description{
            font-size: 30px;
        }
        .image img{
            height: auto;
            width: 100%;
        }
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

