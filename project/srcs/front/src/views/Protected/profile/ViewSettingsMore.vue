<script setup lang="ts">
import { ref } from 'vue';
import Button from '@/components/Button.vue';
import InputLabel from '@/components/InputLabel.vue';
import Select from '@/components/Select.vue';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';


import { useRouter } from 'vue-router'

import UserService from '@/api/services/UserService'
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

const initialImage =  pictures_handler(profile.activeProfile?.pictures.filter(pic => pic.is_profile_picture)[0].url as string);
const initialpictures = profile.activeProfile?.pictures.filter(img => !img.is_profile_picture).map(img => {
    return {
    id: img.url,
    url: pictures_handler(img.url as string)
}})

const selectedProfile = ref<File | null>(null);
const selectedIntersts = ref<string[]>(profile.activeProfile?.interests || []);
const insertedBio = ref(profile.activeProfile?.profile.biography);
const insertedPictures = ref<PicturesDisplying[]>([]);


const router = useRouter()

const handleSubmit = async () => {
    // add protections
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

    formData.append('location_set_by_user', `${false}`);

    try {
        await UserService.completeProfile(formData);
        const user = useUserStore();
        await user.fetchUser();

        router.push('/')
    } catch (error) {
        console.error("Upload failed", error);
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
</script>

<template>
    <div class="wraper">
        <div class="avatar_section">
            <div>
                <PictureNdIcon :initialImage="initialImage" :height="150" :width="150" :readonly="false" @file-selected="handleAvatar" />
            </div>
            <p class="full_name">{{profile.activeProfile?.user.first_name + " " + profile.activeProfile?.user.last_name}}</p>
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
            <Select :options="orientation" v-model="selectedOrientation" ></Select>
        </div>

        <div class="interest_div">
            <p>Interest</p>
            <TagsList @tags-selected="handleTags" :initialtags="availableTags" />
        </div>

        <div class="bio_div">
            <p>Bio</p>
            <textarea v-model="insertedBio" class="bio_erea" name="bio" id="bio" maxlength="500"></textarea>
        </div>

        <div class="bio_div">
            <p>Photos</p>
            <RenderPictures :initialpictures="initialpictures" @files-selected="handlePicures" />
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
