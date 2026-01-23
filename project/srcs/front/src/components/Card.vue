<script setup lang="ts">
const props = defineProps({
    title: String
})
</script>

<template>
        <div class="content">
            <h2 class="title">{{ title }}</h2>
             <slot />
        </div>
</template>

<style lang="scss" scoped>
    .content {
        background-color: $components-background-color;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        padding: 4%;
        // min-height: 50%;
        max-width: 55%;
        min-width: 50%;

        .title {
            align-self: center;
            text-align: center;
            font-weight: 700;
            font-size: 32px;
            margin-bottom: 20px;
        }
    }

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
    }
    .content {
        max-width: 90%;
        min-width: 90%;
    }
    .title {
        font-size: 24px;
    }
}
</style>
