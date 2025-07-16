<script setup>
    import { useRouter } from 'vue-router'
    const router = useRouter()

    const props = defineProps({
        text: String,
        color: { type: String, default: '#FFF' },
        backgroundColor: { type: String, default: '#9566B0' },
        to: { type: String, default: '' },
        onClick: Function
    })

    function handleClick() {
        if (props.to) {
            router.push(props.to)
        } else if (props.onClick) {
            props.onClick()
        }
    }
</script>

<template>
    <button class="button" @click="handleClick" :style="{color: color, backgroundColor: backgroundColor}">
        {{text}}
    </button>
</template>

<style lang="scss" scoped>
    .button {
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 1rem;
        transition: transform 0.2s ease;
    &:hover {
        transform: scale(1.03);
    }
    &:active {
        transform: scale(0.97);
    }
    }
</style>
