<script setup>
    import Button from '@/components/Button.vue';
</script>

<template>
    <!-- <div class="page"> -->
        <div class="content">
            <p class="title">Welcome to Web Matcha Find Your Perfect Match.</p>
            <p class="description">Discover, connect, and chat with singles near you. Join our community today!</p>
            <Button class="button" to="/register" text="Get Started" />
        </div>
        <div class="image">
            <img src="/img/landing.png" alt="landing page" />
        </div>
    <!-- </div> -->
</template>

<style lang="scss" scoped>
    // .page{
    //     display: grid;
    //     grid-template-columns: 1fr 1fr;
    //     align-items: center;
    //     justify-content: center;
    //     height: 100vh;
    //     margin: 40px 20px;
    // }
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
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

