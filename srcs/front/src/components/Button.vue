<script setup lang="ts">
    import { useRouter } from 'vue-router'
    const router = useRouter()

    const props = defineProps({
        text: String,
        color: { type: String, default: '#FFF' },
        backgroundColor: { type: String, default: '#9566B0' },
        to: { type: String, default: '' },
        img: { type: String, default: null }
    })

    const emit = defineEmits(['click'])

    const handleClick = () => {
        if (props.to) {
            router.push(props.to)
        } else {
            emit('click')
        }
    }
</script>

<template>
    <button class="button" @click="handleClick" :style="{color: color, backgroundColor: backgroundColor}">
        <img v-if="img" :src="img" alt="dsd">{{text}} 
    </button>
</template>

<style lang="scss" scoped>
    .button {
        flex-shrink: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 6px;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 500;
        font-size: 1rem;
        transition: transform 0.2s ease;
        font-family: $font-main;
        &:hover {
            transform: scale(0.95);
            opacity: 0.9;
        }
        &:active {
            transform: scale(0.97);
        }
    }
</style>
