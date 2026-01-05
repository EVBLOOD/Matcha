<script setup lang="ts">

defineProps({
    id: String,
    label: String,
    modelValue: String,
    value: String,
    name: String,
    type: {
        type: String,
        default: 'text'
    }})
defineEmits(['update:modelValue']);
</script>

<template>
    <div>
        <input :id="value" :name="name" :type="type" :value="value"
       
        :checked="modelValue === id"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)">
        <label :for="id"> {{ label }}</label>
    </div>
</template>

<style lang="scss" scoped>
input {
    padding: 10px;
    border-color: $border-color;
    border-width: 1px;
    min-height: 36px;
    background: $components-background-color;
    color: $text-color;
    border-radius: 12px;
}
div {
    display: flex;
    margin-bottom: 3%;
    align-items: center;
    gap: 2px;

}
</style>
