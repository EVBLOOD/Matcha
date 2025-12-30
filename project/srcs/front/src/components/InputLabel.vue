<script setup>

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
        @input="$emit('update:modelValue', $event.target.value)">
        <label :for="id"> {{ label }}</label>
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
}
div {
    display: flex;
    margin-bottom: 3%;
    align-items: center;
    gap: 2px;

}
</style>
