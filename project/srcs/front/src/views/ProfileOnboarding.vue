<script setup>
import Card from '@/components/Card.vue';
import Button from '@/components/Button.vue';
import InputLabel from '@/components/InputLabel.vue';
import Select from '@/components/Select.vue';
import { ref, computed } from 'vue';
import useUserStore from '@/stores/user';
import PictureNdIcon from '@/components/PictureNdIcon.vue';
import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';


import AuthService from '@/api/services/AuthService'
import { useRouter } from 'vue-router'


const orientation = [{ value: 'straight', label: 'Straight' }, { value: 'gay', label: 'Gay' }, { value: 'bisexual', label: 'Bisexual' }]
const availableTags = ref(['art', 'music', 'coding']);


const selectedOrientation = ref('straight');
const selectedGender = ref('male');

const selectedProfile = ref(null);
const selectedIntersts = ref([]);
const insertedBio = ref('');
const insertedPictures = ref([]);

const router = useRouter()

const handleSubmit = async () => {
    // add protections
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

    formData.append('location_set_by_user', false);
    //   formData.append('latitude', bio.value);
    //   formData.append('longitude', bio.value);
    
    try {
        await AuthService.completeProfile(formData);
        const user = useUserStore();
        await user.fetchUser();

        router.push('/')
    } catch (error) {
        console.error("Upload failed", error);
    }
};

const handleAvatar = (file) => {
    selectedProfile.value = file;
};

const handlePicures = (files) => {
    insertedPictures.value = [...files];
};

const handleTags = (tags) => {
    selectedIntersts.value = [...tags];
};
</script>

<template>
        <Card title="Complete Your Profile">
            <div class="avatar_section">
                <div>
                    <PictureNdIcon :height="150" :width="150" :readonly="false" @file-selected="handleAvatar" />
                </div>
                <p class="full_name">Saad AKLLAM</p>
            </div>

            <div class="gender_div">
                <p>Gender</p>
                <div class="labels_list">
                    <InputLabel name="gender" label="Male" type="radio" id="male" value="male" v-model="selectedGender" />
                    <InputLabel name="gender" label="Female" type="radio" id="female" value="female" v-model="selectedGender" />
                    <InputLabel name="gender" label="Other" type="radio" id="other" value="other" v-model="selectedGender" />
                </div>
            </div>

            <div class="orientation_div">
                <p>Orientation</p>
                <Select :options="orientation" v-model="selectedOrientation"/>
            </div>

            <div class="interest_div">
                <p>Interest</p>
                <TagsList @tags-selected="handleTags" :initialtags="availableTags"/>
            </div>

            <div class="bio_div">
                <p>Bio</p>
                <textarea v-model="insertedBio" class="bio_erea" name="bio" id="bio" maxlength="500"></textarea>
            </div>

            <div class="bio_div">
                <p>Photos</p>
                <RenderPictures @files-selected="handlePicures"/>
            </div>
            <Button @click="handleSubmit" text="Save and Continue"></Button>
        </Card>
</template>

<style lang="scss" scoped>


// .image-box {
//     width: 100px;
//     height: 100px;
//     border-radius: 8px;
//     background-size: cover;
//     background-position: center;
//     position: relative;
// }

// .remove-btn {
//     position: absolute;
//     top: 35px;
//     left: 35px;
//     background: #BD82DD;
//     color: white;
//     border: none;
//     border-radius: 50%;
//     cursor: pointer;
//     width: 30px;
//     height: 30px;
// }

// .add_pictures {
//     width: 100px;
//     display: flex;
//     justify-content: center;
//     align-items: center;
// }



.bio_div {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 2%;
}

.bio_erea {
    padding: 10px;
    border-color: #BD82DD;
    border-width: 1px;
    min-height: 36px;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.50);
    border-radius: 12px;
    resize: vertical;
    width: 100%;
}

// .interest_span {
//     padding: 3px;
//     border-color: #BD82DD;
//     border-style: solid;
//     border-radius: 8px;
//     cursor: pointer;

//     &.active {
//         background: #9566B0;
//         border-color: #9566B0;
//         color: white;
//     }
// }

// .interest_div_spans {
//     display: flex;
//     flex-wrap: wrap;
//     gap: 3px;
// }

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
// .hidden {
//     display: none;
// }

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
