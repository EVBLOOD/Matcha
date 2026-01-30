<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
import { formatDistanceToNow } from 'date-fns';

import ChatService from '@/api/services/ChatService'
import type {ConversationsResponse} from '@/types/apiResponses'
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

const router = useRouter();
const route = useRoute();

const users = [
    { id: 1, name: 'Karim Id Bouhouch', date: 'Apr 15, 2025', avatar: '/img/profilePictureDemo.png', online: true, lastSeen: 'Online' },
    { id: 2, name: 'Saad Akllam', date: 'May 01, 2025', avatar: '/img/profilePictureDemo.png', online: false, lastSeen: '2 hours ago' },
    { id: 3, name: 'Sadio Mané', date: 'Jan 01, 2026', avatar: '/img/profilePictureDemo.png', online: true, lastSeen: 'Online' },
    { id: 4, name: 'Mohamed Salah', date: 'Apr 23, 2024', avatar: '/img/profilePictureDemo.png', online: false, lastSeen: '1 day ago' }
];

const chatOpen = computed(() => !!route.params.id)

function openChat(userId: number) {
    router.push(`/messages/${userId}`);
}

const isSelected = (conversationId: number) => {
    return Number(route.params.id) === conversationId
}


const conversationsData = ref<ConversationsResponse[] | null>(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);

const fetchConversations = async () => {
    isLoading.value = true;
    try {
        const { data } = await ChatService.getChat();

        if (data && data.data)
            conversationsData.value = [...data.data];
        else
            conversationsData.value = [] 
    } catch (err: unknown) {
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

// watch(() => route.params.id, fetchConversations);

onMounted(fetchConversations);

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

import Loading from '@/components/Loading.vue';

</script>

<template>
    <div class="contentx">
        <Loading :class="['sideBar', { hideOnMobile: chatOpen }]" v-if="isLoading" @finished="isLoading = false" />
        <div v-if="!isLoading && !isError && conversationsData"  :class="['sideBar', { hideOnMobile: chatOpen }]">
            <div class="user" v-if="conversationsData.length == 0">No conversations for you</div>
            <div class="user" v-for="user in conversationsData" :key="user.peer_id" @click="openChat(user.conversation_id)"
            :class="{ selected: isSelected(user.conversation_id) }">
                <div class="avatar">
                    <img :src="pictures_handler(user.profile_picture_url[0].url)" alt="avatar" />
                </div>
                <div class="infos">
                    <p class="name">{{ user.first_name + " " + user.last_name }}</p>
                    <p class="date">{{  formatDistanceToNow(new Date(user.last_active_at), {addSuffix: true}) }}</p>
                </div>
            </div>
        </div>
        <div :class="['chatWrapper', { showOnMobile: chatOpen }]">
            <RouterView />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.contentx {
    color: #FFFFFF;
    display: flex;
    align-items: center;
    height: 100%;
    width: 100%;
}

.sideBar {
    padding: 1%;
    height: 100%;
    width: 30%;
    gap: 2px;
    border-color: rgba(255, 255, 255, 0.25);
    display: flex;
    flex-direction: column;
    border-style: solid;
    border-width: 0px 1px 0px 0px;
}

.user {
    display: flex;
    transition: 0.3s;
    align-items: center;
    padding: 5px 10px;
    gap: 7px;
    user-select: none;
    overflow: hidden;
}

.selected {
    background-color: #ffffff1c;
    border-radius: 6px;
}

.sideBar .user:hover {
    cursor: pointer;
    background-color: #ffffff1c;
    transition: 0.3s;
    border-radius: 6px;
}


.user .avatar {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    overflow: hidden;
}

.user .avatar img {
    height: 100%;
    width: 100%;
    object-fit: cover;
}

.user .infos {}

.user .infos .name {
    font-weight: 500;
    font-size: 14px;
}

.user .infos .date {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
}

.chatWrapper {
    flex: 1;
    height: 100%;
}

@media (max-width: $breakpoint-md) {
    .contentx {
        flex-direction: column;
    }

    .sideBar {
        width: 100%;
    }

    .hideChat {
        display: none;
    }

    .chat {
        width: 100%;
        height: 100%;
    }

    .chatWrapper {
        display: none;
        width: 100%;
        height: 100%;
    }

    .hideOnMobile {
        display: none;
    }

    .showOnMobile {
        display: flex;
        flex-direction: column;
    }
}
</style>
