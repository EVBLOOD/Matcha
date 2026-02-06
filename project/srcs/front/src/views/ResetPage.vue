<script setup lang="ts">
import Card from '@/components/Card.vue';
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import { toast } from '@/composables/useToast';

import AuthService from '@/api/services/AuthService'

import { ref } from 'vue';
import { useRouter } from 'vue-router'

import type { RecoverPassword } from '@/types/auth'
import axios, { AxiosError } from 'axios';


interface ValidationErrors {
  [key: string]: string[];
}

const router = useRouter()
const userEmail = ref('');

const isLoading = ref(false);
const error = ref<null | string | any[]>(null);

const handleReset = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const payload: RecoverPassword = {
      email: userEmail.value,
    };
    const response = await AuthService.rest_password(payload);
    router.push('/login')
    toast('success', 'Reset success', "Please check your email.");
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      error.value = err.response?.data?.errors || err.response?.data?.error || 'Reset failed for unknown reason';
    } else {
      error.value = 'Reset Password failed for unknown reason'
    }
    if (Array.isArray(error.value)) {
      for (err in error.value) {
        toast('error', 'Reset failed', err as string);
      }
    } else if (typeof (error.value) === 'string') {
      toast('error', 'Reset failed', error.value);
    } else if (error.value && typeof (error.value) === 'object') {
      const errorData = error.value as ValidationErrors
      Object.entries(errorData).map(([field, messages]) => {
        messages.map((msg) => {
          toast('error', 'Reset failed', msg);
        })
        return messages.map(msg => msg.toUpperCase());
      });
    }
  } finally {
    isLoading.value = false;
  }
};
import Loading from '@/components/Loading.vue';


</script>

<template>

  <Loading v-if="isLoading" @finished="isLoading = false" />
  <Card title="Reset Password"  v-if="!isLoading">
    <Input name="unameoremail" label="Email" id="unameoremail" v-model="userEmail" />
    <div class="btn" style="display: flex;flex-direction: column; gap: 2px;padding: 6px;">
      <Button text="Reset Password" @click="handleReset" style="background-color: #9566B0;"></Button>
    </div>
    <p class="account">Don’t have an account? &nbsp;
    <p class="sign_up" @click="router.push('register')">Sign up</p>
    </p>
  </Card>
</template>

<style lang="scss" scoped>
.btn {
  margin-top: 5%;
  margin-bottom: 5%;
}

.extra {
  display: flex;
  justify-content: center;
  align-content: center;
  width: 100%;
  gap: 5px;
}

.just_btn {
  margin-top: 0%;
  padding: 0px;
  border-style: none;
}

.forgot_pass {
  margin-top: -2%;
  font-size: 14px;
  text-decoration: underline;
  cursor: pointer;
  color: #e4e4e4;
}

.account {
  display: flex;
  justify-content: center;
  font-size: 14px;
}

.sign_up {
  text-decoration: underline;
  cursor: pointer;
  color: #e4e4e4;
}

.description {
  color: #F4E4FC;
  font-weight: 600;
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.btn-github {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  padding: 12px 16px;
  background-color: #24292f;
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
  font-family: $font-main;
}

.btn-github:hover {
  background-color: #2c3137;
}

.github-icon {
  width: 18px;
  height: 18px;
}

.separator {
  display: flex;
  align-items: center;
  text-align: center;
  color: #F4E4FC;
  font-size: 14px;
  margin: 20px 0;
}

.separator::before,
.separator::after {
  content: "";
  flex: 1;
  height: 1px;
  background-color: #BD82DD;
}

.separator::before {
  margin-right: 12px;
}

.separator::after {
  margin-left: 12px;
}

@media (max-width: $breakpoint-md) {
  .page {
    display: flex;
    flex-direction: column;
  }
}
</style>
