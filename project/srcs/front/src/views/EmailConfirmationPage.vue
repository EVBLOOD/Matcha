<script setup>
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="page">
        <div class="content">
            <h2>An email has been sent to your address.</h2>
            <Button to="nothing" text="Resend Email"></Button> <!-- to nothing means just a backend operation and a front text update -->
            <div>Went to the wrong place?  <Button to="login" text="Back to Log In"></Button></div>
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

