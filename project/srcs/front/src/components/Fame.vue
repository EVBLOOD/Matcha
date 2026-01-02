<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    initialFameScore: {
        type: Number,
        default: 4.5
    },
    readonly: {
        type: Boolean,
        default: false
    }
});

// const emit = defineEmits(['famescore-selected']);

const fameIntersts = ref([]);

// const tagClick = (fameValue) => {
//     fameIntersts.value.push(tag);

//     emit('famescore-selected', fameValue);
// };

const integerPart = computed(() => Math.floor(props.initialFameScore));

const decimalPart = computed(() => {
  const rest = props.initialFameScore % 1;
  return rest > 0 ? rest : null;
});

const stylePercent = computed(() => {
    return {
        background: `linear-gradient(90deg, orange ${decimalPart.value * 100}%, #FFFFFF 0%)`,
        backgroundClip: 'text',
        color: 'transparent',
    };
});

</script>

<template>
    <div>
        
        <span v-for="n in integerPart - 1" class="fa fa-star checked" ></span>
        <span v-if="decimalPart" class="fa fa-star partial" :style="stylePercent"></span>
        <span class="fa fa-star"></span>
    </div>
</template>

<style lang="scss" scoped>
.checked {
    color: orange;
}

.fa {
    font-size: 25px;
}

.partial {
    background-clip: text;
    color: transparent;
}

</style>
