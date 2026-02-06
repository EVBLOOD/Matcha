<script setup lang="ts">
import { onMounted, watch, computed } from 'vue';
import { RouterView, useRoute, useRouter } from 'vue-router';
import Button from '@/components/Button.vue';
import { ref } from 'vue';
import Fame from '@/components/Fame.vue';
import useUserStore from '@/stores/user';
import { useSocialStore } from '@/stores/profile';
import { useSocketStore } from '@/stores/socket';
import Loading from '@/components/Loading.vue';
import Alert from '@/components/Alert.vue';
import InteractionService from '@/api/services/InteractionService'

const route = useRoute();
const router = useRouter();
const profile = useSocialStore()

const statusUser = computed(() => {
    const userId = profile.activeProfile?.user.user_id.toString();
    if (!userId) return 'Offline';

    return socket.UserStatus(userId);
});

const conversationId = computed(() => profile.activeProfile?.interactions?.conversation_id);

watch(() => route.params.id, async () => {
    await profile.fetchProfile(parseInt(route.params.id as string))

});

const userStore = useUserStore();

const socket = useSocketStore();

const likeHandler = () => {
    if (!profile.activeProfile) return
    socket.interactWithUser(profile.activeProfile.user.user_id, 'like')
}

const dislikeHandler = () => {
    if (!profile.activeProfile) return
    socket.interactWithUser(profile.activeProfile.user.user_id, 'dislike')
}

const blockHandler = () => {
    if (!profile.activeProfile) return
    socket.interactWithUser(profile.activeProfile.user.user_id, 'block')
    profile.clearActiveProfile()

}

watch (() => profile.activeProfile, (current) => {
    if (!current) {
        router.push({ name: 'not-found' });
    }
})
watch (() => profile.error, (current) => {
    if (current?.length) {
        router.push({ name: 'not-found' });
    }
})

const reportHandler = async () => {
    if (!profile.activeProfile) return
    try {
        await InteractionService.sendReport("I want to block him", profile.activeProfile.user.user_id);
        blockHandler()
    } catch (err: unknown) {
        console.info("GPS isn't active!")
    }
}

onMounted(async () => {
    await profile.fetchProfile(parseInt(Array.isArray(route.params.id) ? route.params.id[0] : route.params.id))
});


const statusColor = computed(() => {
    if (profile.activeProfile)
        return {
            background: statusUser.value === "Online" ? "rgb(6, 201, 6)" : "red"
        };
});

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

const showReportUser = ref(false)
const showBlockUser = ref(false)

</script>

<template>
    <Loading v-if="profile.loading" @finished="profile.loading = false" />
    <div v-if="!profile.loading && !profile.error && profile.activeProfile" class="contentz">
        <div class="sideBar">
            <div class="sideBar_personal_info">
                <img class="avatar"
                    :src="pictures_handler(profile.activeProfile.pictures.find(obj => obj.is_profile_picture == true)?.url as string)"
                    alt="">
                <div class="name">{{ profile.activeProfile.user.first_name + " " + profile.activeProfile.user.last_name }}</div>
                <div class="status_bar">
                    <div class="status" :style="statusColor"></div>
                    {{ statusUser }}
                </div>
            </div>
            <div v-if="route.params.id !== userStore.getUserID.toString()" class="interaction_field">
                <div class="btn-like-msg">
                    <Button class="btn-like"
                        v-if="(!profile.activeProfile.interactions.is_connected || profile.activeProfile.interactions.is_connected <= 1) && profile.activeProfile.interactions.interaction_status !== 'liked'"
                        @click="likeHandler" text="Like" img="/img/likeIcon@.svg" :color="'#592F6F'"
                        :backgroundColor="'#FEA7FF'">
                    </Button>
                    <Button class="btn-dislike"
                        v-if="profile.activeProfile.interactions.is_connected && profile.activeProfile.interactions.interaction_status === 'liked'"
                        @click="dislikeHandler" text="Dislike" img="/img/likeIcon@.svg" :color="'#592F6F'"
                        :backgroundColor="'#FEA7FF'">
                    </Button>
                    <Button class="btn-msg"
                        v-if="profile.activeProfile.interactions.is_connected == 2 && conversationId"
                        :to="`/messages/${conversationId}`"
                        img="/img/messageIcon.svg">
                    </Button>
                </div>
                <div class="btn-block-report">
                    <Button class="btn-block" @click="showBlockUser = !showBlockUser" text="Block"></Button>
                    <Button class="btn-report" @click="showReportUser = !showReportUser" text="Report"></Button>
                </div>
            </div>
            <div class="stats_holder">
                <div class="stats_count"> 
                    <img src="/img/viewIcon.svg" alt=""> Profile Views : 
                    <span style="font-weight: bold;">{{ profile.activeProfile.interactions.views_count }}
                    </span>
                </div>
                <div class="stats_count"> 
                    <img src="/img/likesIcon.svg" alt=""> Likes Received : 
                    <span style="font-weight: bold;">{{ profile.activeProfile.interactions.likes_count }}</span>
                </div>
            </div>
            <div class="fame">
                <p>Fame Rating 🔥</p>
                <Fame :initialFameScore="profile.activeProfile.profile.fame_rating" class="starts" />
            </div>
        </div>
        <div class="profile_vue">
            <RouterView />
        </div>
    </div>
    <Alert v-model="showBlockUser" title="Block User" confirmText="Block" confirmVariant="danger" size="small" @confirm="blockHandler">
        <div class="alert-block">
            <p>Are you sure you want to block this user?</p>
        </div>
    </Alert>
    <Alert v-model="showReportUser" title="Report User" confirmText="Report" confirmVariant="danger" size="small" @confirm="reportHandler" >
        <div class="alert-block">
            <p>Are you sure you want to report this user?</p>
        </div>
    </Alert>

</template>

<style lang="scss" scoped>
.contentz {
    color: $text-color;
    display: grid;
    grid-template-columns: 25% 75%;
    align-items: center;
    height: 100%;
    width: 100%;
}

.sideBar {
    padding: 25px;
    height: 100%;
    gap: 20px;
    border-color: $border-color;
    display: flex;
    flex-direction: column;
    border-style: solid;
    border-width: 0px 1px 0px 0px;
}

.profile_vue {
    height: 100%;
    padding: 2%;
}


.sideBar_personal_info {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: fit-content;
    .avatar{
        max-width: 250px;
        max-height: 250px;
        margin-bottom: 22px;
    }
    .name{
        font-weight: 500;
        font-size: 1.4rem; 
    }
    .status_bar {
        display: flex;
        align-items: center;
        gap: 4px;
        font-weight: normal;
        font-size: 13px;
        font-size: 0.85rem;

    }
    .status {
        height: 6px;
        width: 6px;
        border-radius: 50%;
        background-color: rgb(6, 201, 6);
        font-size: 0.95rem;
    }
}

.interaction_field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    min-height: fit-content;
    min-width: fit-content;
    width: 100%;
    .btn-block-report{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 5px;
        .btn-block, .btn-report {
            max-height: fit-content;
            min-width: fit-content;
        }
    }
    .btn-like-msg{
        display: grid;
        grid-template-columns: auto min-content;
        gap: 5px;
        .btn-like, .btn-dislike {
            min-width: fit-content;
            min-height: fit-content;
        }
    }
}

.like_messages {
    display: flex;
    align-items: center;
}

.stats_holder {
    display: flex;
    flex-direction: column;
    gap: 5px;
    flex-shrink: 0;
    font-size: 15px;
    min-height: fit-content;
    min-width: fit-content;
    .stats_count {
        width: auto;
        display: flex;
        white-space: nowrap;
        align-items: center;
        gap: 5px;
    }
}

.fame{
    width: max-content;
    .starts{
        min-height: fit-content;
        min-width: fit-content;
    }
}

.alert-block{
    display: grid;
    font-size: 18px;
    font-weight: 500;
    gap: 4px;
}


@media (max-width: $breakpoint-md) {
    .contentz {
        height: fit-content;
        grid-template-columns: 100%;
    }

    .sideBar {
        padding: 2%;
        width: 100%;
        height: fit-content;
        border-style: none;
        align-items: center;
        gap: 25px;
    }

    .interaction_field{
        width: 2em;
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
