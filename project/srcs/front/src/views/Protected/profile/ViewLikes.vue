<script setup lang="ts">
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import NotificationsService from '@/api/services/NotificationsService'
import type { NotificationsResponse } from '@/types/apiResponses'

import { ref, computed, onMounted, watch } from 'vue';

import { useSocketStore } from '@/stores/socket';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

// const previewProfile = ref(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);

const NotificationsData = ref<NotificationsResponse[] | null>(null);



const fetchNotifications = async () => {
  isLoading.value = true;
  try {
    const { data } = await NotificationsService.getNotifications();
    console.log(`data ${data.data}`)
    NotificationsData.value = [...data.data];
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

const avatarStyle = computed(() => {
    const image = "/img/avatar.svg";
    return {
        backgroundImage: `url(${image})`
    };
});

const avatarStyleFun = (value: NotificationsResponse) => {
    let image = "/img/avatar.svg";
    if (value.type == "like") {
        image = "likeNotifIcon.svg"
    } else if (value.type == "view") {
        image = "/img/viewProfileNotifIcon.svg"

    } else if (value.type == "match") {
        image = "/img/likeNotifIcon.svg"

    } else if (value.type == "unmatch") {
        image = "/img/likeNotifIcon.svg" // TO UPDATE
    }
    return image;
};


const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

</script>

<template>
    <div v-if="!isLoading && !isError && !NotificationsData" class="contenty">
        No Notifications For You
    </div>
    <div v-if="!isLoading && !isError && NotificationsData" class="contenty">
        <div v-for="value in NotificationsData" class="notif">
            <PictureNdIcon :height="59" :width="59" :readonly="true" :initialImage="pictures_handler(value.picture_url[0].url)" :initialIcon="avatarStyleFun(value)" />
            <div>
               {{value.type[0].toUpperCase() + value.type.slice(1)}} from <span>@{{value.username}}</span>
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

