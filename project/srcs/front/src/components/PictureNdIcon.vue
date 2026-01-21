<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps({
    initialImage: {
        type: String,
        default: '/img/avatar.svg'
    },
    initialIcon: {
        type: String,
        default: '/img/vector.svg'
    },
    readonly: {
        type: Boolean,
        default: false
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
const emit = defineEmits(['file-selected']);
const inputId = `avatar-input-${Math.random().toString(36).slice(2, 9)}`;
const previewUrl  = ref<null | string>(null);

const avatarStyle = computed(() => {
    const image = previewUrl.value || props.initialImage;
    return {
        backgroundImage: `url('${image}')`,
        width: `${props.width}px`,
        height: `${props.height}px`
    };
});


const onFileChange = (e: Event) => {
    const file = ((e.target as HTMLInputElement).files || [])[0];

    if (!file) return;

    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
    previewUrl.value = URL.createObjectURL(file);

    emit('file-selected', file);
};

</script>

<template>
    <div class="avatar_upload">
        <div class="avatar" :style="avatarStyle"></div>

        <div v-if="!readonly" class="add_avatar">
            <input 
                type="file" 
                :id="inputId" 
                class="hidden" 
                accept="image/*" 
                @change="onFileChange" 
            />
            <label :for="inputId" class="upload_label">
                <img height="100%" width="100%"  :src="initialIcon" alt="Upload">
            </label>
        </div>
        <div v-if="readonly" class="add_avatar">
            <div :for="inputId" class="upload_label">
                <img height="100%" width="100%" :src="initialIcon" alt="Upload">
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
label {
    cursor: pointer;
}
.avatar_upload {
    position: relative;
    display: flex;
    justify-items: center;
    align-items: center;
    flex-direction: column;
    margin-bottom: 5px;
}

.avatar {
    border-radius: 50%;
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
}

.hidden {
    display: none;
}

.add_avatar {
    position: absolute;
    bottom: 5%;
    right: 5%;
    background-color: $secondary-color;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5%;
}

</style>
