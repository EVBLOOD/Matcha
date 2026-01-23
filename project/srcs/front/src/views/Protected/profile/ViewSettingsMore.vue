<script setup lang="ts">
import { ref } from 'vue';
import Button from '@/components/Button.vue';
import InputLabel from '@/components/InputLabel.vue';
import Select from '@/components/Select.vue';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';


import { useRouter } from 'vue-router'

import ProfileService from '@/api/services/ProfileService'
import useUserStore from '@/stores/user';
import type { PicturesDisplying } from '@/types/helpers'

import { useSocialStore } from '@/stores/profile';

const profile = useSocialStore()


const orientation = [{ value: 'straight', label: 'Straight' }, { value: 'gay', label: 'Gay' }, { value: 'bisexual', label: 'Bisexual' }]

const availableTags = ref(profile.activeProfile?.interests);


const selectedOrientation = ref(profile.activeProfile?.user.sexual_preference);
const selectedGender = ref(profile.activeProfile?.user.gender);

const pictures_handler = (link: string) => {
    console.log(link)
    if (link && link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

const initialImage = pictures_handler(profile.activeProfile?.pictures.filter(pic => pic.is_profile_picture)[0].url as string);
const initialpictures = profile.activeProfile?.pictures.filter(img => !img.is_profile_picture).map(img => {
    return {
        id: img.url,
        url: pictures_handler(img.url as string)
    }
})

const selectedProfile = ref<File | null>(null);
const selectedIntersts = ref<string[]>(profile.activeProfile?.interests || []);
const insertedBio = ref(profile.activeProfile?.profile.biography);
const insertedPictures = ref<PicturesDisplying[]>([]);


const router = useRouter()
import { usePreciseLocation } from '@/composables/usePreciseLocation'

const { getPreciseLocation, coords } = usePreciseLocation()
import { toast } from '@/composables/useToast';

interface ValidationErrors {
  [key: string]: string[];
}
const isLoading = ref(false);

const handleSubmit = async () => {

    try {
        isLoading.value = true;
        
        const locationResult = await getPreciseLocation();
        const formData = new FormData();

        formData.append('biography', insertedBio.value || "");
        formData.append('gender', selectedGender.value || "");
        formData.append('sexual_preference', selectedOrientation.value || "");



        formData.append('tags', selectedIntersts.value.join(';'));
        if (selectedProfile.value) {
            formData.append('profile', selectedProfile.value);
        }

        insertedPictures.value.forEach((img) => {
            if (img.file) {
                formData.append(img.id, img.file);
            }
        });

        if (coords.value.latitude !== null && coords.value.longitude !== null) {
            formData.append('latitude', coords.value.latitude.toString());
            formData.append('longitude', coords.value.longitude.toString());
            formData.append('location_set_by_user', String(true));
            console.log("locationResult is on")
        } else {
            formData.append('location_set_by_user', String(false));
            console.log("locationResult is off")

        }
        await ProfileService.updateProfile(formData);
        const user = useUserStore();
        await user.fetchUser();
        
        toast('success', 'Profile update', "Profile updated successfuly!");

        router.push('/')
    } catch (error: any) {

        const error_print = error?.response?.data?.errors || error?.response?.data?.error || 'Profile updated failed for unknown reason';

        if (Array.isArray(error_print)) {
            error_print.map((err) => {
                toast('error', 'Reset failed', err as string);
            })
        } else if (typeof (error_print) === 'string') {
            toast('error', 'Reset failed', error_print);
        } else if (error_print && typeof (error_print) === 'object') {
            const errorData = error_print as ValidationErrors
            Object.entries(errorData).map(([field, messages]) => {
                messages.map((msg) => {
                    toast('error', 'Reset failed', msg);
                })
                return messages.map(msg => msg.toUpperCase());
            });
        }
    } finally {
        isLoading.value = false;
    }
};

const handleAvatar = (file: File) => {
    selectedProfile.value = file;
};

const handlePicures = (files: PicturesDisplying[]) => {
    insertedPictures.value = [...files];
};

const handleTags = (tags: string[]) => {
    selectedIntersts.value = [...tags];
};

import Loading from '@/components/Loading.vue';

</script>

<template>
    <Loading v-if="isLoading" />
    <div  v-if="!isLoading" class="wraper">
        <div class="avatar_section">
            <div>
                <PictureNdIcon :initialImage="initialImage" :height="150" :width="150" :readonly="false"
                    @file-selected="handleAvatar" />
            </div>
            <p class="full_name">{{ profile.activeProfile?.user.first_name + " " +
                profile.activeProfile?.user.last_name}}</p>
        </div>

        <div class="gender_div">
            <p>Gender</p>
            <div class="labels_list">
                <InputLabel name="gender" label="Male" type="radio" id="male" value="male" v-model="selectedGender" />
                <InputLabel name="gender" label="Female" type="radio" id="female" value="female"
                    v-model="selectedGender" />
                <InputLabel name="gender" label="Other" type="radio" id="other" value="other"
                    v-model="selectedGender" />
            </div>
        </div>

        <div class="orientation_div">
            <p>Orientation</p>
            <Select :options="orientation" v-model="selectedOrientation"></Select>
        </div>

        <div class="interest_div">
            <p>Interest</p>
            <TagsList @tags-selected="handleTags" :initialtags="availableTags" :update-mode="true" />
        </div>

        <div class="bio_div">
            <p>Bio</p>
            <textarea v-model="insertedBio" class="bio_erea" name="bio" id="bio" maxlength="500"></textarea>
        </div>

        <div class="bio_div">
            <p>Photos</p>
            <RenderPictures :update-mode="true" :initialpictures="initialpictures" @files-selected="handlePicures" />
        </div>
        <Button @click="handleSubmit" text="Save and Continue"></Button>
    </div>

</template>

<style lang="scss" scoped>
.bio_div {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 2%;
}

.bio_erea {
    padding: 10px;
    border-color: $border-color;
    border-width: 1px;
    min-height: 36px;
    background: $components-background-color;
    color: $text-color;
    border-radius: 12px;
    resize: vertical;
    width: 100%;
    border: 1px solid $border-color;
    outline: none;
    resize: none;
}

.interest_div {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 2%;
}

.orientation_div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2%;

}

.gender_div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2%;

}

.labels_list {
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
}

.full_name {
    font-weight: 600;
    font-size: 18px;
}

.avatar_section {
    position: relative;
    width: 100%;
    display: flex;
    justify-items: center;
    align-items: center;
    flex-direction: column;
    margin-bottom: 2%;
}


@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
    }
}
</style>
