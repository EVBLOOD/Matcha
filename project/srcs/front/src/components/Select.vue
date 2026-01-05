<script setup lang="ts">
import type {OrientationSelectionType} from '@/types/helpers' 

defineProps({
  modelValue: [String, Number],
  options:  Array<OrientationSelectionType>
});


defineEmits(['update:modelValue']);
</script>

<template>
    <select
        :value="modelValue" 
        @change="$emit('update:modelValue', ($event.target as HTMLInputElement).value)">
        <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
</template>

<style lang="scss" scoped>
select {
    width: 70%;
    padding: 10px;
    border-color: $border-color;
    border-width: 1px;
    min-height: 36px;
    background: $components-background-color;
    color: $text-color;
    border-radius: 12px;
}

option {
    background-color: $select-option-background-color;
}
</style>
