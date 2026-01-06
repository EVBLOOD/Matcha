<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
import { inject, onMounted, type Ref } from 'vue';

import RenderPictures from '@/components/RenderPictures.vue';
import Button from '@/components/Button.vue';
import TagsList from '@/components/TagsList.vue';

import useUserStore from '@/stores/user';
import type { UserProfileResponse } from '@/types/apiResponses'
import { useSocketStore } from '@/stores/socket';

const route = useRoute();
const userStore = useUserStore();

const profileData = inject<Ref<UserProfileResponse>>('profileData');

console.log(profileData?.value)

const socketStore = useSocketStore()
const likeHandler = () => {
    if (!profileData) return
    socketStore.interactWithUser(profileData.value.user.user_id, 'like')
}

const dislikeHandler = () => {
    if (!profileData) return
    socketStore.interactWithUser(profileData.value.user.user_id, 'dislike')
}
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
                class="link" :to="`/messages`" text="Message">
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
                :initialpictures="profileData.pictures.filter(obj => !obj.is_profile_picture).map(obj => { return { id: obj.url, url: `http://localhost:8081/profile/pictures/${obj.url}` } })" />
            <div class="gender_location">
                <div><img src="/img/maleIcon.svg" alt=""> {{ profileData.user.gender }}</div>
                <div><img src="/img/locationIcon.svg" alt=""> California - USA </div>
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
