<script setup>
    import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
        Default
</template>

<style lang="scss" scoped>
    nav {
        display: flex;
        gap: 3%
    }
    
    .link {
        text-decoration: none;
        color: $text-color;
        cursor: pointer;
        &:hover {
            border-style: solid;
            border-width: 0px 0px 5px 0px;
            border-color: rgba(255, 255, 255, 0.12);
        }
        &:active {
            border-style: solid;
            border-width: 0px 0px 5px 0px;
            border-color: rgba(255, 255, 255, 1);
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

