<script setup lang="ts">
import Button from '@/components/Button.vue';

import InteractionService from '@/api/services/InteractionService'
import type { LikesResponse } from '@/types/apiResponses'

import { ref, computed, onMounted, watch } from 'vue';

import { useSocketStore } from '@/stores/socket';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error: string;
}

// const previewProfile = ref(null);

const isLoading = ref(true);
const isError = ref<string | null>(null);

const LikesData = ref<LikesResponse[] | null>(null);



const fetchBlocks = async () => {
  isLoading.value = true;
  try {
    const { data } = await InteractionService.getLikesList();
    if (data.data) LikesData.value = [...data.data];
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

import { useSocialStore } from '@/stores/profile';

const socket = useSocketStore();
const profile = useSocialStore()


const dislikeHandler = (user_id: number) => {
    socket.interactWithUser(user_id, 'dislike')
    if (LikesData.value)
    LikesData.value = LikesData.value?.map((elem) => {
        if (elem.liker_id == user_id) elem.unlike = true
        return elem
    })
}

const likeHandler = (user_id: number) => {
    socket.interactWithUser(user_id, 'like')
    if (LikesData.value)
    LikesData.value = LikesData.value?.map((elem) => {
        if (elem.liker_id == user_id) elem.unlike = false
        return elem
    })
}

import { useRouter } from 'vue-router';
const router = useRouter();

const OnclickOpenProfile = (user_id: number) => {
    router.push(`/profile/${user_id}`)
}

import Loading from '@/components/Loading.vue';


</script>

<template>
    <Loading v-if="isLoading" />
    <div v-if="!isLoading && !isError && (!LikesData || LikesData.length == 0)" class="contenty">
        Likes list is empty 
    </div>
    <div v-if="!isLoading && !isError && LikesData" class="contenty">
        <div v-for="value in LikesData" class="element_list">
            <div class="element_list">
                <img width="65px" height="65px"  @click="OnclickOpenProfile(value.liker_id)" :src="pictures_handler(value.profile_picture_url[0].url)" alt="avatar">
                <div class="infos">
                    <span style="color: white; font-weight: 600;">{{value.first_name + " " + value.last_name}}</span>
                   <span>@{{value.username}}</span>
                </div>
            </div>
            <Button v-if="!value.unlike" style="mix-blend-mode: plus-lighter;" text="Unlike" @click="dislikeHandler(value.liker_id)"></Button>
            <Button v-if="value.unlike" style="mix-blend-mode: plus-lighter;" text="Like" @click="likeHandler(value.liker_id)"></Button>
            
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
        cursor: pointer;
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

