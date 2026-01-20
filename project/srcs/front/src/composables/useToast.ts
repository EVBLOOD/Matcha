import { ref } from 'vue'
import type { ToastItem, ToastType } from '@/types/toast'

const MAX_TOASTS = 7
const DURATION = 4000

const toasts = ref<ToastItem[]>([])
const queue = ref<Omit<ToastItem, 'id'>[]>([])

export function useToast() {
    const remove = (id: number) => {
        toasts.value = toasts.value.filter(t => t.id !== id)
        showNext()
    }

    const showNext = () => {
        if (queue.value.length === 0) return
        if (toasts.value.length >= MAX_TOASTS) return

        const next = queue.value.shift()
        if (!next) return

        addToast(next.type, next.title, next.description)
    }

    const addToast = ( type: ToastType, title: string, description: string ) => {
        const id = Date.now() + Math.random()
        toasts.value.push({ id, type, title, description })
        setTimeout(() => remove(id), DURATION)
    }

    const show = ( type: ToastType, title: string, description: string ) => {
        if (toasts.value.length < MAX_TOASTS) {
            addToast(type, title, description)
        } else {
            queue.value.push({ type, title, description })
        }
    }

    return { toasts, show, remove }
}

export const toast = ( type: ToastType, title: string, description: string) => {
    useToast().show(type, title, description)
}