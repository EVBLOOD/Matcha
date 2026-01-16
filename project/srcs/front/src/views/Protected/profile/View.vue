<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';

import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';

import useUserStore from '@/stores/user';
import { useSocketStore } from '@/stores/socket';
import { useSocialStore } from '@/stores/profile';
const profile = useSocialStore()


const route = useRoute();
const userStore = useUserStore();

const profileData = profile.activeProfile;

console.log(profileData)

const socketStore = useSocketStore()


if (profileData && route.params.id !== userStore.getUserID.toString()) {
    socketStore.interactWithUser(profileData.user.user_id, 'view')
}

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

</script>

<template>
    <div v-if="profileData" class="wraper">
        <div style="width: 100%;display: flex; justify-content: flex-end; flex-shrink: 0; gap: 2%;">
            <RouterLink v-if="route.params.id === userStore.getUserID.toString()" class="link"
                :to="`${route.params.id}/settings`"><img src="/img/editProfileIcon.svg" alt="" />
                <span>Edit Profile</span>
            </RouterLink>
        </div>
        <div class="user_infos">

            <div class="gender_location">
                <div><img src="/img/maleIcon.svg" alt=""> {{ profileData.user.gender }}</div>
                <div><img src="/img/locationIcon.svg" alt=""> {{ profileData.user.location }}</div>
            </div>
            <div>
                {{ profileData.profile.biography }}
            </div>
            <TagsList :readonly="true" :initialtags="profileData.interests" />

            <RenderPictures :width="230" :height="230" :readonly="true"
                :initialpictures="profileData.pictures.filter(obj => !obj.is_profile_picture).map(obj => { return { id: obj.url, url: pictures_handler(obj.url) } })" />

        </div>
        <div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.wraper {
    display: flex;
    flex-shrink: 0;
    flex-direction: column;
    gap: 5%;
    height: 100%;
}

.user_infos {
    display: flex;
    flex-shrink: 0;
    flex-direction: column;
    gap: 20px;
    // height: 100%;
}

.link {
    display: flex;
    flex-shrink: 0;
    gap: 10px;
    text-decoration: none;
    color: $text-color;
    justify-content: flex-end;
    align-items: center;
    // width: 20%;
    // height: 20px;
    padding: 1% 2% 1% 2%;
    cursor: pointer;
    background: $components-background-color;
    border-radius: 10px;
}

.link:hover {
    background: $menu-background-color-hover;

}

@media (max-width: $breakpoint-md) {
    .wraper {
        height: fit-content;
        gap: 15px;
    }

    .user_infos {
        // width: 100%;
        // gap: 10px;
        gap: 25px;

        align-items: center;

    }

    .gender_location {
        width: 100%;
        display: flex;
    flex-shrink: 0;

        justify-content: center;
        align-items: center;
        gap: 3%;

        div {
            display: flex;
    flex-shrink: 0;

            gap: 2px;
        }
    }
}
</style>
