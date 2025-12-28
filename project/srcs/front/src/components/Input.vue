<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const props = defineProps({
    id: String,
    label: String,
    modelValue: String,
    name: String,
    type: {
        type: String,
        default: 'text'
    }
})
defineEmits(['update:modelValue']);
</script>

<template>
    <div>
        <label :for="id"> {{ label }}</label>
        <input :value="modelValue" :name="name" :type="type"
            @input="$emit('update:modelValue', $event.target.value)">
    </div>
</template>

<style lang="scss" scoped>
input {
    padding: 10px;
    border-color: #BD82DD;
    border-width: 1px;
    min-height: 36px;
    background: rgba(255, 255,255, 0.08);
    color: rgba(255, 255,255, 0.50);
    border-radius: 12px;
    margin-bottom: 5%;
}
div {
    display: flex;
    flex-direction: column;
    width: 100%;
}
</style>
