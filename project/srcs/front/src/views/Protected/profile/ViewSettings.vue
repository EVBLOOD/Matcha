<script setup lang="ts">
    import { RouterLink, RouterView, useRoute } from 'vue-router';

    const route = useRoute()


</script>

<template>
    <nav style="height: 5%;">
        <RouterLink class="link" to="/profile/:id/settings" :class="{ active: route.meta.subtitle == 'Personal details' }">Personal details</RouterLink>
        <RouterLink class="link" to="/profile/:id/settings/password" :class="{ active: route.meta.subtitle == 'Change password' }">Change password</RouterLink>
        <RouterLink class="link" to="/profile/:id/settings/details" :class="{ active: route.meta.subtitle == 'More details' }">More details</RouterLink>
    </nav>
    <div style="height: 95%;">
        <RouterView />
    </div>
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
        height: 80%;
        &:hover {
            border-style: solid;
            border-width: 0px 0px 5px 0px;
            border-color: $border-color-hover;
        }
        &.active {
            border-style: solid;
            border-width: 0px 0px 5px 0px;
            border-color: $border-color-active;
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

