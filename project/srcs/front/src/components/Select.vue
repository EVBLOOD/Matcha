<script setup>
defineProps({
  modelValue: [String, Number],
  options:  Array  // [{ value: 'a', label: 'A' }]
});


defineEmits(['update:modelValue']);
</script>

<template>
    <select
        :value="modelValue" 
        @change="$emit('update:modelValue', $event.target.value)">
        <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
</template>

<style lang="scss" scoped>
select {
    width: 70%;
    padding: 10px;
    border-color: #BD82DD;
    border-width: 1px;
    min-height: 36px;
    background: rgba(255, 255,255, 0.08);
    color: rgba(255, 255,255, 0.50);
    border-radius: 12px;
}
</style>
