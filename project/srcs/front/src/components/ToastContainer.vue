<script setup lang="ts">
    import { useToast } from '@/composables/useToast';
    import type { ToastType } from '@/types/toast';

    const { toasts, remove } = useToast();

    const icon = (type: ToastType): string => {
    const icons: Record<ToastType, string> = {
        error: '/img/toast/error.svg',
        warning: '/img/toast/error.svg',
        success: '/img/toast/success.svg',
        info: '/img/toast/info.svg',
        message: '/img/toast/message.svg',
        like: '/img/toast/like.svg',
        view: '/img/toast/view.svg'
    }
    return icons[type]
    }

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}

import { useRouter } from 'vue-router';
const router = useRouter()


const go_to = (id: number | null, type: string) => {
  if (!id) return
  if (type == 'view' || type == 'like') {
    router.push( `/profile/${id}`)
  } else if (type == 'message') {
    router.push( `/messages/${id}`)
  }
}

</script>

<template>
  <div class="toast-container">
    <div v-for="toast in toasts" :key="toast.id" class="toast" :class="toast.type">
      <div class="left">
        <div class="icon" :class="toast.type" >
            <img :src="icon(toast.type)" alt="" />
        </div>
        <div class="content">
            <h4 @click="go_to(toast.id_user, toast.type)">{{ toast.title }}</h4>
            <div style="display: flex; align-items: center; gap: 3px;">
              <img style="border-radius: 50%;" width="20px" height="20px" v-if="toast.avatar" :src="pictures_handler(toast.avatar)" alt="avatar">
              <h6 v-if="toast.username">{{ toast.username }}</h6>
              {{ toast.description }}
            </div>
        </div>
      </div>
      <button class="close" @click="remove(toast.id)">✕</button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toast {
  min-width: 320px;
  max-width: 380px;
  background: #f8f1ff;
  color: #592F6F;
  border-radius: 14px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow:
    0 10px 25px rgba(0, 0, 0, 0.08),
    0 4px 10px rgba(0, 0, 0, 0.05);
  animation: slideIn 0.25s ease-out;
}

.toast .left {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.toast .icon {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;

}

.icon.error { background-color: $toast-error; }
.icon.warning { background-color: $toast-warning; }
.icon.success { background-color: $toast-success; }
.icon.info { background-color: $toast-info; }
.icon.message,
.icon.like,
.icon.view { background-color: $toast-social; }

.toast .icon img {
    object-fit: contain;
    width: 50%;
    height: 50%;
}

.toast .content h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0;
  cursor: pointer;
  align-items: center;
}

.toast .content p {
  font-size: 13px;
  margin: 4px 0 0;
  color: #555;
}

.toast .close {
  background: transparent;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #888;
  padding: 4px;
}

.toast .close:hover {
  color: #000;
}

.toast.error { border-bottom: 4px solid $toast-error; }
.toast.warning { border-bottom: 4px solid $toast-warning; }
.toast.success { border-bottom: 4px solid $toast-success; }
.toast.info { border-bottom: 4px solid $toast-info; }
.toast.message,
.toast.like,
.toast.view { border-bottom: 4px solid $toast-social; }

@keyframes slideIn {
  from {
    transform: translateX(20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

</style>