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
    maxPicNumber : {
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
});
const emit = defineEmits(['files-selected']);

const inputId = `pictures-input-${Math.random().toString(36).slice(2, 9)}`;

const insertedPictures = ref<Array<insertedPictures>>(props.initialpictures);


const removeImage = (id: string) => {
    const index = insertedPictures.value.findIndex(f => f.id === id);
    if (index !== -1) {
        URL.revokeObjectURL(insertedPictures.value[index].url);
        insertedPictures.value.splice(index, 1);
    }
};

const onFileChange = (event: Event) => {
    const recent_pictures = Array.from((event.target as HTMLInputElement).files || []);

    const remainingSlots = 4 - insertedPictures.value.length;

    const newPics : Array<PicturesDisplying> = recent_pictures.slice(0, remainingSlots).map(file => ({
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
            <div class="image-box" :style="{ backgroundImage: `url(${img.url})` }">
                <button v-if="!readonly" class="remove-btn" @click="removeImage(img.id)">×</button>
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
    gap: 4%;
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
</style>
