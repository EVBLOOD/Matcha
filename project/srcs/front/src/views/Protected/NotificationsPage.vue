<script setup lang="ts">
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import NotificationsService from '@/api/services/NotificationsService'
import type { NotificationsResponse } from '@/types/apiResponses'
import { formatDistanceToNow } from 'date-fns';

import { ref, computed, onMounted, watch } from 'vue';

import { useSocketStore } from '@/stores/socket';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

const isLoading = ref(true);
const isError = ref<string | null>(null);

const NotificationsData = ref<NotificationsResponse[] | null>(null);


const socket = useSocketStore()

const fetchNotifications = async () => {
  isLoading.value = true;
  try {
    const { data } = await NotificationsService.getNotifications();
    NotificationsData.value = [...data.data];
    socket.setNotifsCount(0)
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
        image = "/img/likeNotifIcon.svg"
    } else if (value.type == "view") {
        image = "/img/viewProfileNotifIcon.svg"

    } else if (value.type == "match") {
        image = "/img/likeNotifIcon.svg"

    } else if (value.type == "unmatch") {
        image = "/img/likeNotifIcon.svg"
    }
    return image;
};


const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

import { useRouter } from 'vue-router';

const router = useRouter()
const go_to = (id: number) => {
    router.push(`/profile/${id}`)
}

const NotSeen = () => {
    return {
        backgroundClip: 'text',
        color: 'transparent',
    };
};

import Loading from '@/components/Loading.vue';

</script>

<template>
    <Loading v-if="isLoading" @finished="isLoading = false" />
    <div v-if="!isLoading && !isError && !NotificationsData" class="contenty">
        No Notifications For You
    </div>
    <div v-if="!isLoading && !isError && NotificationsData" class="contenty">
        <div class="notif" v-for="value in NotificationsData">
            <div class="content" @click="go_to(value.source_user_id)">
                <PictureNdIcon :height="50" :width="50" :readonly="true" :initialImage="pictures_handler(value.picture_url[0].url)" :initialIcon="avatarStyleFun(value)" />
                <div :style="!value.is_read ? {fontWeight: '600'} : {color: '#bdbdbd'}">
                    <div class="title">
                        {{value.type[0].toUpperCase() + value.type.slice(1)}} from <span :style="!value.is_read ? {color: '#BD82DD'} : {}">@{{value.username}}</span>
                    </div>
                    <div class="date" :style="!value.is_read ? {fontWeight: '500'} : {}">
                        {{  formatDistanceToNow(new Date(value.created_at), {addSuffix: true}) }}
                    </div>
                </div>
            </div>
            <div v-if="!value.is_read" style="background-color: #FEA7FF; height: 18px; width: 18px; border-radius: 50%;"></div>
        </div>
    </div>
</template>

<style lang="scss" scoped>

    .contenty{
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 0.5%;
        cursor: pointer;
    }
    .notif {
        display: flex;
        align-items: center;
        padding: 8px 16px;
        .content{
            display: flex;
            align-items: center;
            width: 100%;
            gap: 6px;
            .title{
                font-size: 0.9em;
            }
            .date{
                font-size: 0.7em;
                color: #bdbdbd;
            }
        }
    }
    .notif:hover{
        background: $components-hover-color;
        border-radius: 8px;
    }

    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
        }
    }
</style>

