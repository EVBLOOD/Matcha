<script setup lang="ts">
import { ref, provide, onMounted, watch } from 'vue';
import { RouterView, useRoute } from 'vue-router';

import Fame from '@/components/Fame.vue';

import useUserStore from '@/stores/user';
import ProfileService from '@/api/services/ProfileService'
import type {UserProfileResponse} from '@/types/apiResponses'
import axios, { AxiosError } from 'axios';

const route = useRoute();
const userStore = useUserStore();
const profileData = ref<UserProfileResponse | null>(null);
const isLoading = ref(true);
const isError = ref<string | null>(null);

interface BackendError {
  error: string;
}

const fetchProfile = async () => {
  isLoading.value = true;
  try {
    const { data } = await ProfileService.getProfile(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id);
    profileData.value = data;
  } catch(err : unknown) {
    if (axios.isAxiosError(err)) {
        isError.value = (err.response?.data as BackendError)?.error;
    }
    else {
        isError.value = "Registration failed for unknown reason'";
    }
  } finally {
    isLoading.value = false;
  }
};

watch(() => route.params.id, fetchProfile);

onMounted(fetchProfile);

provide('profileData', profileData);
</script>

<template>
    <div v-if="!isLoading && !isError && profileData" class="contentz">
        <div class="sideBar">
            <div class="sideBar_personal_info">
                <img width="250px" height="250px" style="margin-bottom: 22px;" :src="`http://localhost:8081/profile/pictures/${profileData.pictures.find(obj => obj.is_profile_picture == true)?.url}`" alt="">
                <div style="font-weight:500; font-size: 26px;">{{profileData.user.first_name + " " + profileData.user.last_name}}</div>
                <div class="status_bar">
                    <div class="status"></div> Online
                </div>
            </div>
            <div class="stats_holder">
                <div class="stats_count"> <img src="/img/viewIcon.svg" alt=""> Profile Views : <span
                        style="font-weight: bold;">{{profileData.interactions.views_count}}</span></div>
                <div class="stats_count"> <img src="/img/likesIcon.svg" alt=""> Likes Received : <span
                        style="font-weight: bold;">{{profileData.interactions.likes_count}}</span></div>
            </div>
            <div>
                <p>Fame Rating 🔥</p>
                <Fame :initialFameScore="profileData.profile.fame_rating"/>
            </div>
        </div>
        <div class="profile_vue">
            <RouterView />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.contentz {
    color: $text-color;
    display: flex;
    align-items: center;

    height: 100%;
    width: 100%;
}

.sideBar {
    padding: 5%;
    height: 100%;
    gap: 10%;

    border-color: $border-color;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    border-style: solid;
    border-width: 0px 1px 0px 0px;
}

.status_bar {
    display: flex;
    align-items: center;
    gap: 3%;
    font-weight: normal;
}

.status {
    height: 8px;
    width: 8px;
    border-radius: 50%;
    background-color: rgb(6, 201, 6);
}

.stats_count {
    display: flex;
    gap: 5px;
    align-items: center;
    flex-wrap: wrap;
}

.stats_holder {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.profile_vue {
    height: 100%;
    width: 100%;
    padding: 2%;
}

@media (max-width: $breakpoint-md) {
    .contentz {
        flex-direction: column;
        height: fit-content;
        // align-items: center;
    }
    .sideBar {
        padding: 5%;
        width: 100%;
        height: fit-content;
        border-style: none;
        align-items: center;
        gap: 25px;
    }
    .sideBar_personal_info {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;

    }

}
</style>
