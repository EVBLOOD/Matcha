<script setup lang="ts">
import { ref, computed } from 'vue';
import type { PicturesDisplying, insertedPictures } from '@/types/helpers'

const props = defineProps({
    initialpictures: {
        type: Array<insertedPictures>,
        default: []
    },
    readonly: {
        type: Boolean,
        default: false
    },
    maxPicNumber: {
        type: Number,
        default: 4
    },
    width: {
        type: Number,
        default: 100
    },
    height: {
        type: Number,
        default: 100
    },
    updateMode: {
        type: Boolean,
        defaut: false
    }
});
const emit = defineEmits(['files-selected']);

const inputId = `pictures-input-${Math.random().toString(36).slice(2, 9)}`;

const insertedPictures = ref<Array<insertedPictures>>(props.initialpictures);

import ProfileService from '@/api/services/ProfileService';


import axios, { AxiosError } from 'axios';

interface BackendError {
    error?: string;
    errors?: any[];
}

interface ValidationErrors {
    [key: string]: string[];
}
import { toast } from '@/composables/useToast';

const error = ref<null | string | any[]>(null);

const removeImage = async (id: string) => {
    const index = insertedPictures.value.findIndex(f => f.url === id);
    if (index !== -1) {
        URL.revokeObjectURL(insertedPictures.value[index].url);
        insertedPictures.value.splice(index, 1);

        if (props.updateMode && id.indexOf('/') > 0) {
            try {
                let path = id.replace(`${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/`, '');
                await ProfileService.removeProfilePictues(path)
                toast('success', 'Picture delete', "Picture was deleted successfuly!");
            } catch (err: unknown) {
                if (axios.isAxiosError(err)) {
                    error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Picture delete failed for unknown reason';
                } else {
                    error.value = 'Picture delete failed for unknown reason'
                }
                if (axios.isAxiosError(err)) {
                    error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Picture delete failed for unknown reason';
                } else {
                    error.value = 'Picture delete failed for unknown reason'
                }
                if (Array.isArray(error.value)) {
                    error.value.map((err) => {
                        toast('error', 'Picture delete failed', err as string);
                    })
                } else if (typeof (error.value) === 'string') {
                    toast('error', 'Picture delete failed', error.value);
                } else if (error.value && typeof (error.value) === 'object') {
                    const errorData = error.value as ValidationErrors
                    Object.entries(errorData).map(([field, messages]) => {
                        messages.map((msg) => {
                            toast('error', 'Picture delete failed', msg);
                        })
                        return messages.map(msg => msg.toUpperCase());
                    });
                }
            }
        }
    }
};

const onFileChange = (event: Event) => {
    const recent_pictures = Array.from((event.target as HTMLInputElement).files || []);

    const remainingSlots = 4 - insertedPictures.value.length;

    const newPics: Array<PicturesDisplying> = recent_pictures.slice(0, remainingSlots).map(file => ({
        file,
        id: crypto.randomUUID(),
        url: URL.createObjectURL(file)
    }));

    insertedPictures.value = [...insertedPictures.value, ...newPics];

    emit('files-selected', insertedPictures.value);
    (event.target as HTMLInputElement).value = '';
};

</script>

<template>
    <div class="pictures_view">
        <div v-for="img in insertedPictures" :key="img.id">
            <div class="image-box"
                :style="{ backgroundImage: `url(${img.url})`, width: `${width}px`, height: `${height}px` }">
                <button v-if="!readonly" class="remove-btn" @click="removeImage(img.url)">×</button>
            </div>
        </div>

        <div>
            <div v-if="!readonly && insertedPictures.length < maxPicNumber" class="add_pictures">
                <input type="file" :id="inputId" class="hidden" multiple accept="image/*" @change="onFileChange" />
                <label style="display: flex; justify-content: center; align-items: center; cursor: pointer;"
                    :for="inputId"><img src="/img/add_picture.svg" alt=""></label>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.pictures_view {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}

.image-box {
    width: 100px;
    height: 100px;
    border-radius: 8px;
    background-size: cover;
    background-position: center;
    position: relative;
}

.remove-btn {
    position: absolute;
    top: 35px;
    left: 35px;
    background: $secondary-color;
    color: $text-color;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    width: 30px;
    height: 30px;
}


.add_pictures {
    width: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.hidden {
    display: none;
}

@media (max-width: $breakpoint-md) {
    .pictures_view {
        width: 100%;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 2px;
    }

}
</style>
