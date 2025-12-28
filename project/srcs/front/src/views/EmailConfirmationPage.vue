<script setup>
import Card from '@/components/Card.vue';
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="page">
        <Card title="An email has been sent to your address.">
            <Button to="nothing" text="Resend Email"></Button> <!-- to nothing means just a backend operation and a front text update -->
            <div>Went to the wrong place?  <Button to="login" text="Back to Log In"></Button></div>
        </Card>
    </div>
</template>

<style lang="scss" scoped>

    .page {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

