<script setup>
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';
import PictureNdIcon from '@/components/PictureNdIcon.vue';

import { ref, computed } from 'vue';
const previewProfile = ref(null);

const avatarStyle = computed(() => {
    const image = previewProfile.value || "/img/avatar.svg";
    return {
        backgroundImage: `url(${image})`
    };
});
</script>

<template>
    <div class="content">
        <div class="notif">
            <PictureNdIcon :height="59" :width="59" :readonly="true" initialImage='/img/avatar.svg' initialIcon="/img/viewProfileNotifIcon.svg" />
            <div>
               New message from <span>@evblood</span>
            </div>
        </div>
        <div class="notif">
            <PictureNdIcon :height="59" :width="59" :readonly="true" initialImage='/img/avatar.svg' initialIcon="/img/viewProfileNotifIcon.svg" />
            <div>
               New message from <span>@evblood</span>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>

    .content{
        padding: 2%;
        display: flex;
        flex-direction: column;
        gap: 0.5%;

    }
    .notif {
        // position: relative;
        width: 100%;
        display: flex;
        // justify-content: space-between;
        gap: 2%;
        align-items: center;
        // height: 15%;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

