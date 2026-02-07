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
    gap: 4px;

}
input[type="radio"] {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    width: 20px;
    height: 20px;
    min-height: 0;
    padding: 0;
    line-height: 1;
    box-sizing: border-box;
    border: 2px solid #BD82DD;
    border-radius: 50%;
    background: transparent;
    cursor: pointer;
    position: relative;
    padding: 0;
}

input[type="radio"]:checked::after {
    content: "";
    width: 10px;
    height: 10px;
    background: #BD82DD;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

input[type="radio"]:hover {
    border-color: #BD82DD;
}

input[type="radio"]:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.3);
}

</style>
