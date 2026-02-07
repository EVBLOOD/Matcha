<script setup lang="ts">

const props = defineProps({
    id: String,
    label: String,
    modelValue: String,
    name: String,
    placeholder: String,
    type: {
        type: String,
        default: 'text'
    },
    variant: {
        type: String,
        default: 'default'
    }
})
defineEmits(['update:modelValue']);
</script>

<template>
    <div>
        <label :for="id"> {{ label }}</label>
        <input 
            :class="`input--${variant}`"
            :value="modelValue" 
            :name="name" 
            :type="type" 
            :placeholder="placeholder"
            @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)">
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
    outline: none;
    font-family: $font-main;
    border: 1px solid $border-color;
}

.input--popup {
    background: transparent;
    color: #592F6F;
    border-color: #BD82DD;
}

.input--popup::placeholder {
    color: #C2A6D2;
}

div {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-bottom: 3%;
    gap: 4px;
}
</style>
