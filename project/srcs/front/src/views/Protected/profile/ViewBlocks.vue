<script setup lang="ts">
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import BlocksService from '@/api/services/BlocksService'
import type { BlocksResponse } from '@/types/apiResponses'

import { ref, computed, onMounted, watch } from 'vue';

import { useSocketStore } from '@/stores/socket';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

// const previewProfile = ref(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);

const BlocksData = ref<BlocksResponse[] | null>(null);



const fetchBlocks = async () => {
  isLoading.value = true;
  try {
    const { data } = await BlocksService.getBlocks();
    console.log(`data ${data.data}`)
    BlocksData.value = [...data.data];
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

const avatarStyle = computed(() => {
    const image = "/img/avatar.svg";
    return {
        backgroundImage: `url(${image})`
    };
});

const avatarStyleFun = (value: BlocksResponse) => {
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
    <div v-if="!isLoading && !isError && !BlocksData" class="contenty">
        Block list is empty 
    </div>
    <div v-if="!isLoading && !isError && BlocksData" class="contenty">
        <div v-for="value in BlocksData" class="element_list">
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
    .element_list {
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

