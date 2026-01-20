<script setup lang="ts">
import Button from '@/components/Button.vue';

import InteractionService from '@/api/services/InteractionService'
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
    const { data } = await InteractionService.getBlockList();
    console.log(`data ${data.data}`)
    if (data.data)
        BlocksData.value = [...data.data];
    console.log(BlocksData.value)
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

const socket = useSocketStore();

const blockHandler = (user_id: number) => {
    socket.interactWithUser(user_id, 'block')
    if (BlocksData.value)
    BlocksData.value = BlocksData.value?.map((elem) => {
        if (elem.blocked_id == user_id) elem.unblock = false
        return elem
    })
}

const unblockHandler = (user_id: number) => {
    socket.interactWithUser(user_id, 'unblock')
    if (BlocksData.value)
    BlocksData.value = BlocksData.value?.map((elem) => {
        if (elem.blocked_id == user_id) elem.unblock = true
        return elem
    })
}

</script>

<template>
    <div v-if="!isLoading && !isError && !BlocksData" class="contenty">
        Block list is empty 
    </div>
    <div v-if="!isLoading && !isError && BlocksData" class="contenty">
        <div v-for="value in BlocksData" class="element_list">
            <div class="element_list">
                <img width="70px" height="70px" :src="pictures_handler(value.profile_picture_url[0].url)" alt="avatar">
                <div class="infos">
                    <span style="color: white; font-weight: 600;">{{value.first_name + " " + value.last_name}}</span>
                   <span>@{{value.username}}</span>
                </div>
            </div>
            <Button v-if="!value.unblock" style="mix-blend-mode: plus-lighter;" text="Unblock" @click="unblockHandler(value.blocked_id)"></Button>
            <Button v-if="value.unblock" style="mix-blend-mode: plus-lighter;" text="Block" @click="blockHandler(value.blocked_id)"></Button>
            
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

