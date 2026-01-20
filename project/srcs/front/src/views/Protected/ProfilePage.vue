<script setup lang="ts">
import { onMounted, watch, computed } from 'vue';
import { RouterView, useRoute } from 'vue-router';
import Button from '@/components/Button.vue';

import Fame from '@/components/Fame.vue';

import useUserStore from '@/stores/user';

import { useSocialStore } from '@/stores/profile';
import { useSocketStore } from '@/stores/socket';

const route = useRoute();

const profile = useSocialStore()

watch(() => route.params.id, () => {
    profile.fetchProfile(parseInt(route.params.id as string))
});

const userStore = useUserStore();

const socket = useSocketStore();

const likeHandler = () => {
    if (!profile.activeProfile) return
    if (profile.activeProfile.interactions.is_connected) profile.activeProfile.interactions.is_connected++
    else profile.activeProfile.interactions.is_connected = 1
    profile.activeProfile.interactions.likes_count++
    profile.activeProfile.interactions.interaction_status = 'liked'
    socket.interactWithUser(profile.activeProfile.user.user_id, 'like')
}

const dislikeHandler = () => {
    if (!profile.activeProfile) return
    if (profile.activeProfile.interactions.is_connected) profile.activeProfile.interactions.is_connected--
    else profile.activeProfile.interactions.is_connected = 0
    profile.activeProfile.interactions.likes_count--
    profile.activeProfile.interactions.interaction_status = undefined
    socket.interactWithUser(profile.activeProfile.user.user_id, 'dislike')
}

const blockHandler = () => {
    if (!profile.activeProfile) return
    socket.interactWithUser(profile.activeProfile.user.user_id, 'block')
    profile.clearActiveProfile()
}
import InteractionService from '@/api/services/InteractionService'

const reportHandler = async () => {
    if (!profile.activeProfile) return
    try {
        await InteractionService.sendReport("I want to block him", profile.activeProfile.user.user_id);
        blockHandler()
    } catch(err : unknown) {
        console.info("GPS isn't active!") 
    }   
}

onMounted(() => {
    profile.fetchProfile(parseInt(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id))
    if (profile.activeProfile)
        socket.reachStausOneUser(profile.activeProfile.user.user_id.toString())
});


const statusColor = computed(() => {
    if (profile.activeProfile)
        return {
            background: socket.UserStatus(profile.activeProfile.user.user_id.toString()) == "Online" ? "rgb(6, 201, 6)" : "red"
        };
});

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

</script>

<template>
    <div v-if="!profile.loading && !profile.error && profile.activeProfile" class="contentz">
        <div class="sideBar">
            <div class="sideBar_personal_info">
                <img width="250px" height="250px" style="margin-bottom: 22px;"
                    :src="pictures_handler(profile.activeProfile.pictures.find(obj => obj.is_profile_picture == true)?.url as string)"
                    alt="">
                <div style="font-weight:500; font-size: 26px;">{{ profile.activeProfile.user.first_name + " " +
                    profile.activeProfile.user.last_name}}</div>
                <div class="status_bar">
                    <div class="status" :style="statusColor"></div>
                    {{ socket.UserStatus(profile.activeProfile.user.user_id.toString()) }}
                </div>
            </div>
            <div v-if="route.params.id !== userStore.getUserID.toString()" class="interaction_field">
                <div class="like_messages">
                    <Button
                        style="width: 182px;" v-if="(!profile.activeProfile.interactions.is_connected || profile.activeProfile.interactions.is_connected <= 1) && profile.activeProfile.interactions.interaction_status !== 'liked'"
                        @click="likeHandler" text="Like" img="/img/likeIcon@.svg" :color="'#592F6F'" :backgroundColor="'#FEA7FF'">
                    </Button>
                    <Button
                        style="width: 182px;" v-if="profile.activeProfile.interactions.is_connected && profile.activeProfile.interactions.interaction_status === 'liked'"
                        @click="dislikeHandler" text="Dislike" img="/img/likeIcon@.svg" :color="'#592F6F'" :backgroundColor="'#FEA7FF'">
                    </Button>
                    <Button
                        v-if="profile.activeProfile.interactions.is_connected == 2"
                        :to="`/messages/${profile.activeProfile.interactions.conversation_id}`"
                        img="/img/messageIcon.svg">
                    </Button>
                </div>
                <div class="like_messages">
                    <Button
                        style="width: 120px;" @click="blockHandler" text="Block">
                    </Button>
                    <Button
                        style="width: 120px;" @click="reportHandler" text="Report">
                    </Button>
                </div>

            </div>
            <div class="stats_holder">
                <div class="stats_count"> <img src="/img/viewIcon.svg" alt=""> Profile Views : <span
                        style="font-weight: bold;">{{ profile.activeProfile.interactions.views_count }}</span></div>
                <div class="stats_count"> <img src="/img/likesIcon.svg" alt=""> Likes Received : <span
                        style="font-weight: bold;">{{ profile.activeProfile.interactions.likes_count }}</span></div>
            </div>
            <div style="flex-shrink: 0;">
                <p>Fame Rating 🔥</p>
                <Fame :initialFameScore="profile.activeProfile.profile.fame_rating" />
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
    padding: 2%;
    height: 100%;
    gap: 5%;
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

.sideBar_personal_info {
    display: flex;
    flex-direction: column;
    // align-items: center;
    // justify-content: center;
    flex-shrink: 0;
}

.interaction_field {
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex-shrink: 0;
    width: 100%;
}

.like_messages {
    display: flex;
    justify-content: center;
    gap: 5px;
    flex-shrink: 0;
    width: 100%;
}

// .link {
//     width:inherit;
// }

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
    flex-shrink: 0;
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
    }

    .sideBar {
        padding: 2%;
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

    .status_bar {
        width: 100%;
        justify-content: center;
        align-items: center;
    }

}
</style>
