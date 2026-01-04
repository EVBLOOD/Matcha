<script setup lang="ts">
import { ref } from 'vue';

const props = defineProps({
    initialtags: {
        type: Array<String>,
        default: []
    },
    readonly: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['tags-selected']);


const availableTags = ref<Array<string>>(props.initialtags as Array<string>);
const selectedIntersts = ref<Array<string>>([]);

const tagClick = (tag: string) => {
    if (selectedIntersts.value.includes(tag)) {
        selectedIntersts.value = selectedIntersts.value.filter(t => t !== tag);
    } else {
        selectedIntersts.value.push(tag);
    }
    emit('tags-selected', selectedIntersts.value);
};

const clickNewTag = () => {
    const newTag = prompt("Enter new interest:");
    if (newTag && !availableTags.value.includes(newTag)) {
        availableTags.value.push(newTag);
        tagClick(newTag)
    }
};

</script>

<template>
    <div class="interest_div_spans">
        <div class="interest_span" v-for="tag in availableTags" :key="tag" @click="tagClick(tag)"
            :class="{ active: selectedIntersts.includes(tag) && !readonly }"> #{{ tag }} </div>
        <div v-if="!readonly" class="interest_span" @click="clickNewTag">+ Add tag</div>
    </div>
</template>

<style lang="scss" scoped>
.interest_div_spans {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
}

.interest_span {
    padding: 3px;
    border-color: #BD82DD;
    border-style: solid;
    border-radius: 8px;
    cursor: pointer;

    &.active {
        background: #9566B0;
        border-color: #9566B0;
        color: white;
    }
}
</style>
