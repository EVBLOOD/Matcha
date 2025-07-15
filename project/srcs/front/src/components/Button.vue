<template>
    <button class="button">{{text}}</button>
</template>

<style lang="scss" scoped>
    .button{
        background-color: bisque;
        padding: 10px;
    }
</style>

<script setup>
    defineProps({
        text: String
    })
</script>