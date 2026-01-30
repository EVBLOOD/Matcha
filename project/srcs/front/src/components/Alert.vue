<script setup lang="ts">
    const props = defineProps<{
        modelValue: boolean
        title?: string
        confirmText?: string
        cancelText?: string
        confirmVariant?: 'primary' | 'danger'
        size?: 'small' | 'medium' | 'large'
    }>()

    const emit = defineEmits<{
        (e: 'update:modelValue', v: boolean): void
        (e: 'confirm'): void
        (e: 'cancel'): void
    }>()

    const close = () => {
        emit('update:modelValue', false)
        emit('cancel')
    }

    const confirm = () => {
        emit('confirm')
        emit('update:modelValue', false)
    }
</script>

<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="close">
      <div class="modal" :class="size">
        <div class="header">
          <h2>{{ title }}</h2>
          <span class="btn-close" @click="close">×</span>
        </div>
        <div class="content">
          <slot />
        </div>
        <div class="footer">
          <button class="btn cancel" @click="close">
            {{ cancelText || 'Cancel' }}
          </button>
          <button class="btn confirm" :class="confirmVariant || 'primary'" @click="confirm">
            {{ confirmText || 'Confirm' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 999;
}

.modal {
  background: #E2BDF6;
//   width: 50%;
  padding: 30px;
  border-radius: 10px;
  color: #592F6F;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  &.small {
    width: 450px;
  }

  &.medium {
    width: 50%;
  }

  &.large {
    width: 80%;
  }
}

.header {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #6e597b5e;
    padding-bottom: 12px;
    .btn-close {
        cursor: pointer;
        background: #9566B0;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
}

.content{
    margin-top: 25px;
    margin-bottom: 25px;
}

.footer {
  display: flex;
  gap: 10px;
  margin-top: 20px;

  .btn {
    flex: 1;
    padding: 14px;
    font-size: 14px;
    border-radius: 8px;
    cursor: pointer;
    border: none;
    font-family: $font-main;
    font-weight: 600;
  }

  .cancel {
    background: #E8DCEF;
    color: #592F6F;

    &:hover {
      background: #d5c1e0;
    }
  }

  .confirm.primary {
    background: #9566B0;
    color: white;

    &:hover {
      background: #7e52a0;
    }
  }

  .confirm.danger {
    background: #d9534f;
    color: white;

    &:hover {
      background: #c9302c;
    }
  }
}

@media (max-width: $breakpoint-md) {
  .modal {
    width: 95% !important;
  }

  .footer {
    flex-direction: column;
  }
}
</style>