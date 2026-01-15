<script setup lang="ts">
import { ref, computed } from 'vue';
import Fame from '@/components/Fame.vue';

const props = defineProps({
    firstElem: {
        type: Boolean,
        default: false
    },
    elemName: String,
    inputType:{
        type: String,
        default: 'radio'
    }
});

const emit = defineEmits(['selected_choice']);

const handleClick = () => {
    const action = `${props.inputType}by${props.elemName}`
    emit('selected_choice', action);
};

</script>

<template>

    <div class="div_breaker">
        <div v-if="!firstElem" class="break_line"></div>
        <div class="search_type">
            <div class="label_input">
                <input v-if="inputType == 'radio'" type="radio" name="div_breaker_1"  @click="handleClick()" >
                <input  v-if="inputType != 'radio'" type="image" src="/img/arrowDownIcon.svg" @click="handleClick()" />
                <h3>{{ elemName || "evblood" }}</h3>
            </div>
        </div>
    </div>

</template>

<style lang="scss" scoped>
.div_breaker {
    position: relative;
    display: flex;
    overflow: visible;
    gap: 20px;
    height: 100%;
    align-items: center;
}

.search_type {
    display: flex;
    flex-direction: column;

}

.label_input {
    display: flex;
    gap: 10px;
    justify-content: space-between;
}

.break_line {
    height: 30px;
    border-style: solid;
    border-width: 0px 0px 0px 2px;
    border-radius: 10%;
    border-color: $border-color;
}

@media (max-width: $breakpoint-md) {
    .div_breaker {
        display: flex;
        flex-direction: column;
        width: 100%;
        align-items: flex-start;
    }

    .break_line {
        width: 100%;
        border-style: solid;
        height: 2px;
        border-width: 2px 0px 0px 0px;
    }
}
</style>
