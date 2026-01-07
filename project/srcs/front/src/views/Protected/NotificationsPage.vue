<script setup lang="ts">
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import NotificationsService from '@/api/services/NotificationsService'
import type { NotificationsResponse } from '@/types/apiResponses'

import { ref, computed, onMounted } from 'vue';

import { useSocketStore } from '@/stores/socket';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

const previewProfile = ref(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);

const NotificationsData = ref<NotificationsResponse[] | null>(null);



const fetchNotifications = async () => {
  isLoading.value = true;
  try {
    const { data } = await NotificationsService.getNotifications();
    console.log(`data ${data.data}`)
    NotificationsData.value = data.data;
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


onMounted(fetchNotifications);

// const avatarStyle = computed(() => {
//     const image = previewProfile.value || "/img/avatar.svg";
//     return {
//         backgroundImage: `url(${image})`
//     };
// });
</script>

<template>
    <div v-if="!isLoading && !isError && !NotificationsData" class="contenty">
        No Notifications For You
    </div>
    <div v-if="!isLoading && !isError && NotificationsData" class="contenty">
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

    .contenty{
        padding: 2%;
        display: flex;
        flex-direction: column;
        gap: 0.5%;

    }
    .notif {
        width: 100%;
        display: flex;
        gap: 2%;
        align-items: center;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

