<script setup lang="ts">
import Card from '@/components/Card.vue';
import Button from '@/components/Button.vue';
import InputLabel from '@/components/InputLabel.vue';
import Select from '@/components/Select.vue';
import { ref, onMounted, watch } from 'vue';
import useUserStore from '@/stores/user';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';


import { usePreciseLocation } from '@/composables/usePreciseLocation'
import UserService from '@/api/services/UserService'
import { useRouter } from 'vue-router'

import type { PicturesDisplying } from '@/types/helpers'
import { toast } from '@/composables/useToast';

interface ValidationErrors {
  [key: string]: string[];
}

const orientation = [{ value: 'straight', label: 'Straight' }, { value: 'gay', label: 'Gay' }, { value: 'bisexual', label: 'Bisexual' }]
const availableTags = ref(['art', 'music', 'coding']);


const selectedOrientation = ref('straight');
const selectedGender = ref('male');

const selectedProfile = ref<File | null>(null);
const selectedIntersts = ref<string[]>([]);
const insertedBio = ref('');
const insertedPictures = ref<PicturesDisplying[]>([]);

const router = useRouter()

const { getPreciseLocation, coords } = usePreciseLocation()


const handleSubmit = async () => {
    try {
        const locationResult = await getPreciseLocation();
        const formData = new FormData();

        formData.append('biography', insertedBio.value);
        formData.append('gender', selectedGender.value);
        formData.append('sexual_preference', selectedOrientation.value);



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
        } else {
            formData.append('location_set_by_user', String(false));

        }

        await UserService.completeProfile(formData);
        const user = useUserStore();
        await user.fetchUser();

        router.push('/')
    } catch (error: any) {

        const error_print = error?.response?.data?.errors || error?.response?.data?.error || 'Profile complete failed for unknown reason';

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


import AuthService from '@/api/services/AuthService'
const userStore = useUserStore();

const isLoading = ref(false);

const clickLogOut = async () => {
  isLoading.value = true;

    try {
        const response = await AuthService.logout();
        userStore.fetchUser()
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');

        userStore.setIsLoaded(false)

        router.push('login')
    } catch (err) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
    } finally {
        isLoading.value = false;
    }
}

import Loading from '@/components/Loading.vue';

</script>

<template>
    <Loading v-if="isLoading" @finished="isLoading = false" />
    <div v-if="!isLoading" v-on:click="clickLogOut" style="position: absolute; bottom: 10%; left: 5%;">
        <a class="link log_a"><img src="/img/logOut.svg" alt="" /> <span>Log
                out</span></a>
    </div>
    <Card v-if="!isLoading" title="Complete Your Profile">
        <div class="avatar_section">
            <div>
                <PictureNdIcon :height="150" :width="150" :readonly="false" @file-selected="handleAvatar" />
            </div>
            <p class="full_name">{{ userStore.getUserName }}</p>
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
            <TagsList @tags-selected="handleTags" :initialtags="availableTags" />
        </div>

        <div class="bio_div">
            <p>Bio</p>
            <textarea v-model="insertedBio" class="bio_erea" name="bio" id="bio" maxlength="500"></textarea>
        </div>

        <div class="bio_div">
            <p>Photos</p>
            <RenderPictures @files-selected="handlePicures" />
        </div>
        <Button @click="handleSubmit" text="Save and Continue"></Button>
    </Card>
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

.link {
    display: flex;
    gap: 10px;
    text-decoration: none;
    color: $text-color;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    padding: 6%;
    align-content: center;
    cursor: pointer;
    flex-wrap: wrap;
}

.link:hover {
    background: $components-hover-color;
    border-radius: 8px;

}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
    }
}
</style>
