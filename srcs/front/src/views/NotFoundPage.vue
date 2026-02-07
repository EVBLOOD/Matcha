<script setup lang="ts">
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="content">
        <h1>404</h1>
        <p class="subtitle">
            Sorry! We can't find the page you are looking for.
        </p>
        <Button text="Back to Home" to="/" />
    </div>
</template>

<style lang="scss" scoped>
.content {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    text-align: center;
}

h1 {
    font-size: 6rem;
    font-weight: 800;
}

.subtitle {
    font-size: 1.3rem;
    opacity: 0.7;
}

</style>
