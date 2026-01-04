<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
import { inject, type Ref } from 'vue';

import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';

import useUserStore from '@/stores/user';
import type { UserProfileResponse } from '@/types/apiResponses'

const route = useRoute();
const userStore = useUserStore();

const profileData = inject<Ref<UserProfileResponse>>('profileData');
</script>

<template>
    <div v-if="profileData" class="wraper">
        <div style="width: 100%;display: flex; justify-content: flex-end; flex-shrink: 0; gap: 2%;">
            <RouterLink v-if="route.params.id === userStore.getUserID.toString()" class="link"
                :to="`${route.params.id}/settings`"><img src="/img/editProfileIcon.svg" alt="" /> <span>Edit
                    Profile</span></RouterLink>
            <RouterLink v-if="route.params.id !== userStore.getUserID.toString()" class="link" :to="`/messages`">Message
            </RouterLink>
            <RouterLink v-if="route.params.id !== userStore.getUserID.toString()" class="link" to="`/more`"><img
                    src="/img/moreIcon.svg" alt="" /></RouterLink>

        </div>
        <div class="user_infos">
            <RenderPictures :readonly="true"
                :initialpictures="profileData.pictures.filter(obj => !obj.is_profile_picture).map(obj => { return { id: obj.url, url: `http://localhost:8081/profile/pictures/${obj.url}` } })" />

            <div><img src="/img/maleIcon.svg" alt=""> {{ profileData.user.gender }}</div>
            <div><img src="/img/locationIcon.svg" alt=""> California - USA </div>
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

.interest_span {
    padding: 3px;
    border-color: #9566B0;
    background: rgba(150, 104, 177, 1 - 0.24);
    border-style: solid;
    border-radius: 8px;
    padding: 0.5% 2% 0.5% 2%;
    flex-wrap: nowrap;
}

.interest_div_spans {
    display: flex;
    flex-wrap: wrap;
    gap: 2%;
}

.user_infos {
    display: flex;
    flex-direction: column;
    gap: 2%;
    height: 100%;
}

.pictures_list {
    display: flex;
    gap: 4%;
    flex-wrap: wrap;
}

.image-box {
    width: 100px;
    height: 100px;
    border-radius: 8px;
    background-size: cover;
    background-position: center;
    position: relative;
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
    background: rgba(255, 255, 255, 0.14);
    border-radius: 4px;
}

.link:hover {
    background: rgba(255, 255, 255, 0.12);

}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
