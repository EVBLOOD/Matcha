<script setup lang="ts">
    import { RouterLink, RouterView, useRoute } from 'vue-router';
import useUserStore from '@/stores/user';

const userStore = useUserStore();
    const route = useRoute()


</script>

<template>
    <nav>
        <RouterLink class="link" :to="`/profile/${userStore.getUserID}/settings`" :class="{ active: route.meta.subtitle == 'Personal details' }">Personal details</RouterLink>
        <RouterLink class="link" :to="`/profile/${userStore.getUserID}/settings/password`" :class="{ active: route.meta.subtitle == 'Change password' }">Change password</RouterLink>
        <RouterLink class="link" :to="`/profile/${userStore.getUserID}/settings/details`" :class="{ active: route.meta.subtitle == 'More details' }">More details</RouterLink>
    </nav>
    <div>
        <RouterView />
    </div>
</template>

<style lang="scss" scoped>
    nav {
        display: flex;
        gap: 3%;
        margin-bottom: 10px;
    }
    .link {
        text-decoration: none;
        color: $text-color;
        cursor: pointer;
        height: 80%;
        padding-bottom: 5px;
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
        }
    }
</style>

