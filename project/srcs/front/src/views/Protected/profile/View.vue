<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
// import { inject, onMounted, type Ref } from 'vue';

import RenderPictures from '@/components/RenderPictures.vue';
import Button from '@/components/Button.vue';
import TagsList from '@/components/TagsList.vue';

import useUserStore from '@/stores/user';
import type { UserProfileResponse } from '@/types/apiResponses'
import { useSocketStore } from '@/stores/socket';

import { useSocialStore } from '@/stores/profile';
import { watch } from 'vue';
const profile = useSocialStore()


const route = useRoute();
const userStore = useUserStore();

const profileData = profile.activeProfile;

console.log(profileData)

const socketStore = useSocketStore()
const likeHandler = () => {
    if (!profileData) return
    if (profileData.interactions.is_connected) profileData.interactions.is_connected++
    else profileData.interactions.is_connected = 1
    profileData.interactions.likes_count++
    profileData.interactions.interaction_status = 'liked'
    socketStore.interactWithUser(profileData.user.user_id, 'like')
}

const dislikeHandler = () => {
    if (!profileData) return
    if (profileData.interactions.is_connected) profileData.interactions.is_connected--
    else profileData.interactions.is_connected = 0
    profileData.interactions.likes_count--
    profileData.interactions.interaction_status = undefined
    socketStore.interactWithUser(profileData.user.user_id, 'dislike')
}


if (profileData && route.params.id !== userStore.getUserID.toString()) {
    socketStore.interactWithUser(profileData.user.user_id, 'view')
}

const blockHandler = () => {
    if (!profileData) return
    socketStore.interactWithUser(profileData.user.user_id, 'block')
    profile.clearActiveProfile()
}

const unblockHandler = () => {
    if (!profileData) return
    socketStore.interactWithUser(profileData.user.user_id, 'unblock')
}

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

// watch(profileData, ()=> )

// watch(() => profile.activeProfile, () => {
//     console.log("upda")
//     // profile.fetchProfile(parseInt(route.params.id as string))

// });
</script>

<template>
    <div v-if="profileData" class="wraper">
        <div style="width: 100%;display: flex; justify-content: flex-end; flex-shrink: 0; gap: 2%;">
            <RouterLink v-if="route.params.id === userStore.getUserID.toString()" class="link"
                :to="`${route.params.id}/settings`"><img src="/img/editProfileIcon.svg" alt="" />
                <span>Edit Profile</span>
            </RouterLink>
            <Button
                v-if="route.params.id !== userStore.getUserID.toString() && profileData.interactions.is_connected && profileData.interactions.is_connected == 2"
                class="link" :to="`/messages/${profileData.interactions.conversation_id}`" text="Message">
            </Button>

            <Button
                v-if="route.params.id !== userStore.getUserID.toString() && (!profileData.interactions.is_connected || profileData.interactions.is_connected <= 1) && profileData.interactions.interaction_status !== 'liked'"
                class="link" @click="likeHandler" text="Like">
            </Button>
            <Button
                v-if="route.params.id !== userStore.getUserID.toString() && profileData.interactions.is_connected && profileData.interactions.interaction_status === 'liked'"
                class="link" @click="dislikeHandler" text="Dislike">
            </Button>

            <RouterLink v-if="route.params.id !== userStore.getUserID.toString()" class="link" to="`/more`"><img
                    src="/img/moreIcon.svg" alt="" /></RouterLink>

        </div>
        <div class="user_infos">
            <RenderPictures :readonly="true"
                :initialpictures="profileData.pictures.filter(obj => !obj.is_profile_picture).map(obj => { return { id: obj.url, url: pictures_handler(obj.url) } })" />
            <div class="gender_location">
                <div><img src="/img/maleIcon.svg" alt=""> {{ profileData.user.gender }}</div>
                <div><img src="/img/locationIcon.svg" alt=""> {{ profileData.user.location }}</div>
            </div>
            <div>
                {{ profileData.profile.biography }}
            </div>
            <TagsList :readonly="true" :initialtags="profileData.interests" />

        </div>
        <div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.wraper {
    display: flex;
    flex-direction: column;
    gap: 5%;
    height: 100%;
}

.user_infos {
    display: flex;
    flex-direction: column;
    gap: 2%;
    height: 100%;
}

.link {
    display: flex;
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
        justify-content: center;
        align-items: center;
        gap: 3%;

        div {
            display: flex;
            gap: 2px;
        }
    }
}
</style>
