<script setup lang="ts">
import { formatDistanceToNow } from 'date-fns';
import InteractionService from '@/api/services/InteractionService'
import type { ViewsListResponse } from '@/types/apiResponses'

import { ref, computed, onMounted, watch } from 'vue';

import { useSocketStore } from '@/stores/socket';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

// const previewProfile = ref(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);

const ViewsData = ref<ViewsListResponse[] | null>(null);



const fetchBlocks = async () => {
  isLoading.value = true;
  try {
    const { data } = await InteractionService.getViewsList();
    console.log(data.data)
    ViewsData.value = [...data.data];
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


onMounted(fetchBlocks);


const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

const Onclick = (user_id: number) => {

}
</script>

<template>
    <div v-if="!isLoading && !isError && !ViewsData" class="contenty">
        Block list is empty 
    </div>
    <div v-if="!isLoading && !isError && ViewsData" class="contenty">
        <div v-for="value in ViewsData" class="element_list">
            <div class="element_list">
                <img width="70px" height="70px" :src="pictures_handler(value.profile_picture_url[0].url)" alt="avatar">
                <div class="infos">
                    <span style="color: white; font-weight: 600;">{{value.first_name + " " + value.last_name}}</span>
                   <span>@{{value.username}}</span>
                </div>
            </div>
            <div style="flex-shrink: 0;">
                {{ formatDistanceToNow(new Date(value.viewed_at)) }}
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
    .element_list {
        width: 100%;
        display: flex;
        gap: 2%;
        align-items: center;
        gap: 2%;
        margin-bottom: 10px;
    }
    img {
        border-radius: 50%;
    }
    .infos {
        display: flex;
        flex-direction: column;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

