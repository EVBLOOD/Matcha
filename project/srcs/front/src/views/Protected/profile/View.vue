<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
import Button from '@/components/Button.vue';

import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';

import useUserStore from '@/stores/user';
import { useSocketStore } from '@/stores/socket';
import { useSocialStore } from '@/stores/profile';
const profile = useSocialStore()


const route = useRoute();
const userStore = useUserStore();
const profileData = profile.activeProfile;
const socketStore = useSocketStore()


if (profileData && route.params.id !== userStore.getUserID.toString()) {
    socketStore.interactWithUser(profileData.user.user_id, 'view')
}

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

import { usePreciseLocation } from '@/composables/usePreciseLocation'
import UserService from '@/api/services/UserService';
const { getPreciseLocation, coords } = usePreciseLocation()


import { toast } from '@/composables/useToast';

interface ValidationErrors {
  [key: string]: string[];
}

// const isLoading = ref(true);

const isLoading = ref(false);

const OnclickUpdateLocal = async () => {
    isLoading.value = true
    try {
        const result = await getPreciseLocation();
        if (!result) toast('error', 'Update location failed', 'GPS wasn\'t activated.');

        await UserService.update_location_lt_lng((coords.value.latitude || "").toString(),
        (coords.value.longitude || "").toString())
        profile.fetchProfile(parseInt(route.params.id as string))
        toast('success', 'Update location success', 'Your location was updated.');
      } catch(err : any) {
        const error = err.response?.data?.errors || err.response?.data?.error || 'GPS wasn\'t activated.';
        if (Array.isArray(error.value)) {
            for (err in error.value) {
                toast('error', 'Update location failed', err as string);
            }
        } else if (typeof (error.value) === 'string') {
            toast('error', 'Update location failed', error.value);
        } else if (error.value && typeof (error.value) === 'object') {
            const errorData = error.value as ValidationErrors
            Object.entries(errorData).map(([field, messages]) => {
                messages.map((msg) => {
                    toast('error', 'Update location failed', msg);
                })
                return messages.map(msg => msg.toUpperCase());
            });
        }
      } finally {
        isLoading.value = false
      }
}
import Loading from '@/components/Loading.vue';
import { ref } from 'vue';

</script>

<template>
    <Loading v-if="isLoading" />
    
    <div  v-if="profileData && !isLoading" class="wraper">
        <div style="width: 100%;display: flex; justify-content: flex-end; flex-shrink: 0; gap: 2%;">
            <RouterLink v-if="route.params.id === userStore.getUserID.toString()" class="link"
                :to="`${route.params.id}/interactions`">
                <span>My Interactions</span>
            </RouterLink>
            <RouterLink v-if="route.params.id === userStore.getUserID.toString()" class="link"
                :to="`${route.params.id}/settings`"><img src="/img/editProfileIcon.svg" alt="" />
                <span>Edit Profile</span>
            </RouterLink>
        </div>
        <div class="user_infos">
            <div class="gender_location">
                <div class="textIcon">
                    <div><img src="/img/maleIcon.svg" alt="gender"></div>
                    <p>{{ profileData.user.gender.charAt(0).toUpperCase() + profileData.user.gender.slice(1) }}</p>
                </div>
                <div class="location">
                    <div class="textIcon">
                        <div><img src="/img/locationIcon.svg" alt="location"></div>
                        <p>{{ profileData.user.location }}</p>
                    </div>
                    <Button v-if="route.params.id === userStore.getUserID.toString()" style="font-size: 12px; font-weight: 700; padding: 6px; mix-blend-mode: plus-lighter; color: #1E1E1E;" text="Update" @click="OnclickUpdateLocal()"></Button>
                </div>
            </div>
            <div>
                {{ profileData.profile.biography }}
            </div>
            <TagsList :readonly="true" :initialtags="profileData.interests" />
            <RenderPictures :width="230" :height="230" :readonly="true"
                :initialpictures="profileData.pictures.filter(obj => !obj.is_profile_picture).map(obj => { return { id: obj.url, url: pictures_handler(obj.url) } })" />
        </div>
        <div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.wraper {
    display: flex;
    flex-shrink: 0;
    flex-direction: column;
    gap: 5%;
    height: 100%;
}

.user_infos {
    display: flex;
    flex-shrink: 0;
    flex-direction: column;
    gap: 20px;
    // height: 100%;
}

.link {
    display: flex;
    flex-shrink: 0;
    gap: 10px;
    text-decoration: none;
    color: $text-color;
    justify-content: flex-end;
    align-items: center;
    padding: 1% 2% 1% 2%;
    cursor: pointer;
    background: $components-background-color;
    border-radius: 10px;
}

.link:hover {
    background: $menu-background-color-hover;
}

.textIcon{
    display: flex;
    align-items: center;
    gap: 4px;
    div{
        height: 20px;
        width: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        img{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }
    }
}

.gender_location{
    display: flex;
    flex-direction: column;
    gap: 10px;
}

// .location{
//     display: flex; 
//     justify-content: space-between; 
//     flex-wrap: nowrap; 
//     align-items: center;
// }

.location{
    display: flex;
    gap: 12px;
}

@media (max-width: $breakpoint-md) {
    .wraper {
        height: fit-content;
        gap: 15px;
    }

    .user_infos {
        gap: 25px;
        align-items: center;
    }

    .gender_location {
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
</style>
