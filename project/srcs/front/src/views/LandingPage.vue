<script setup>
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="page">
        <div>
            <p class="title">Welcome to Web Matcha Find Your Perfect Match.</p>
            <p class="description">Discover, connect, and chat with singles near you. Join our community today!</p>
            <Button text="Get Started" />
        </div>
        <div class="image">
            <img src="/img/landing.png" alt="landing page" />
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .page{
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
    }
    .title{
        font-weight: 700;
        font-size: 40px;
    }
    .description{
        font-size: 32px;
    }
    .image img{
        height: auto;
        width: 100%;
    }
</style>

