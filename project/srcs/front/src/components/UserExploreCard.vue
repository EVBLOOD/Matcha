<script setup lang="ts">
import Fame from '@/components/Fame.vue';
import Button from '@/components/Button.vue';

const props = defineProps({
    fullName: {
        type: String,
        default: "Saad AKLLAM"
    },
    avatar: {
        type: String,
        default: "/img/avatar.svg"
    },
    age: {
        type: String,
        default: "18"
    },
    location: {
        type: String,
        default: "somewhere"
    },
    fameScore: {
        type: Number,
        default: 2
    },
    userID: Number
});

const emit = defineEmits(['AgeMin-selected', 'AgeMax-selected', 'location-selected', 'fame-selected', 'tags-selected']);

import { ref } from 'vue';
import { useSocketStore } from '@/stores/socket';

const socket = useSocketStore();
const isLiked = ref(false)
const clickLike = () => {
    if (!props.userID) return
    isLiked.value = true
    socket.interactWithUser(props.userID, 'like')
}
const clickUnike = () => {
    if (!props.userID) return
    isLiked.value = false
    socket.interactWithUser(props.userID, 'dislike')
}

</script>

<template>

    <div class="user_card">
        <img style="border-radius: 50%;" width="150px" height="150px" :src="avatar" alt="">
        <span>{{fullName}}</span>
        <div>
            <span>{{ age }}</span>
            -
            <span>{{ location }}</span>
        </div>
        <Fame :initialFameScore="fameScore"/>
        <Button  v-if="!isLiked" style="background-color: #BC80DC;color: #592F6F;mix-blend-mode: plus-lighter;" class="user_card_btn" text="Like" @click="clickLike"></Button>
        <Button  v-if="isLiked" style="background-color: #BC80DC;color: #592F6F;" class="user_card_btn" text="Unlike" @click="clickUnike"></Button>
        <Button  class="user_card_btn" text="View Profile" :to="`/profile/${userID}`"></Button>

    </div>

</template>

<style lang="scss" scoped>
.user_card {
    padding: 2%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-width: 260px;

    background-color: $components-background-color;
    border-radius: 12px;
    gap: 5px;
    margin-bottom: 2%;
}

.user_card_btn {
    width: 100%;
    min-width: 200px;

}

@media (max-width: $breakpoint-md) {
    .user_card {
        min-width: 150px;
    }
    img {
        width: 100px;
        height: 100px;
    }
}

.user_card_btn {
    width: 100%;
    min-width: fit-content;

}
</style>
