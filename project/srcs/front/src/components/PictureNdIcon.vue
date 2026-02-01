<script setup lang="ts">

import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';

import { ref, computed } from 'vue';
import { toast } from '@/composables/useToast';

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

const avatarStyle = computed(() => {
    const image = previewUrl.value || props.initialImage;
    return {
        backgroundImage: `url('${image}')`,
        width: `${props.width}px`,
        height: `${props.height}px`
    };
});


const emit = defineEmits(['file-selected']);
const inputId = `avatar-input-${Math.random().toString(36).slice(2, 9)}`;
const previewUrl  = ref<null | string>(null);


const showEditor = ref(false);
const rawImageUrl = ref<string | null>(null);
const cropperRef = ref();


// const onFileChange = (e: Event) => {
//     const file = ((e.target as HTMLInputElement).files || [])[0];

//     if (!file) return;

//     if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
//     previewUrl.value = URL.createObjectURL(file);

//     emit('file-selected', file);
// };

const onFileChange = (e: Event | DragEvent) => {
    try {

        let file: File | undefined;
        
        if (e instanceof DragEvent) {
            file = e.dataTransfer?.files[0];
        } else {
            file = ((e.target as HTMLInputElement).files || [])[0];
        }
    
        if (!file) return;
    
        const reader = new FileReader();
        reader.onload = (event) => {
            rawImageUrl.value = event.target?.result as string;
            showEditor.value = true;
        };
        reader.readAsDataURL(file);
    } catch {
        toast('error', "Insert Image", "the file selected wasn't correct, please try another one!")
    }
};

const fileInput = ref<HTMLInputElement | null>(null);

const saveEdit = () => {
    try {

        const { canvas } = cropperRef.value.getResult();
        canvas.toBlob((blob: Blob) => {
            if (!blob) return;
            
            const editedFile = new File([blob], "avatar.jpg", { type: "image/jpeg" });
    
            if (previewUrl.value) URL.revokeObjectURL(previewUrl.value);
            previewUrl.value = URL.createObjectURL(editedFile);
    
            emit('file-selected', editedFile);
        }, 'image/jpeg');
        showEditor.value = false;
        if (fileInput.value) {
            fileInput.value.value = "";
        }
    } catch {
        toast('error', "Insert Image", "the file format isn't supported!")
    }
};

</script>

<template>
    <div class="avatar_upload" 
         @dragover.prevent 
         @drop.prevent="onFileChange"> <div class="avatar" :style="avatarStyle"></div>

        <div v-if="!readonly" class="add_avatar">
            <input 
                ref="fileInput"
                type="file" 
                :id="inputId" 
                class="hidden" 
                accept="image/*" 
                @change="onFileChange" 
            />
            <label :for="inputId" class="upload_label">
                <img height="100%" width="100%" :src="initialIcon" alt="Upload">
            </label>
        </div>

        <div v-if="showEditor" class="editor_modal">
            <div class="modal_content">
                <cropper
                    ref="cropperRef"
                    class="cropper"
                    :src="rawImageUrl"
                    :stencil-props="{ aspectRatio: 1/1 }"
                />
                <div class="modal_actions">
                    <button @click="showEditor = false">Cancel</button>
                    <button @click="saveEdit" class="save_btn">Apply & Upload</button>
                </div>
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
    // margin-bottom: 5px;
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



.editor_modal {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: rgba(0,0,0,0.8);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
    * {
        overflow: hidden !important;

    }
    .vue-bounding-box{   
        overflow: hidden !important;
        * {
             overflow: hidden !important;

         }
    }

    .modal_content {
        
        width: 100%;
        background: white;
        padding: 20px;
        border-radius: 8px;
        max-width: 90%;
        
        .cropper {
            
            padding: 0px;
            max-height: 400px;
            // background: #ddd;
        }
    }

    .modal_actions {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        
        .save_btn {
            background: $secondary-color;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        }
    }
}

</style>
