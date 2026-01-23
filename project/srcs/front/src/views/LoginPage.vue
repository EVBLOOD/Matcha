<script setup lang="ts">
import Card from '@/components/Card.vue';
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import { toast } from '@/composables/useToast';

import AuthService from '@/api/services/AuthService'
import useUserStore from '@/stores/user';

import { ref } from 'vue';
import { useRouter } from 'vue-router'

import type { Login } from '@/types/auth'
import axios, { AxiosError } from 'axios';

interface BackendError {
  error?: string;
  errors?: any[];
}


const router = useRouter()
const userName = ref('');
const passWord = ref('');

const isLoading = ref(false);
const error = ref<null | string | any[]>(null);
const user = useUserStore();


const handleLogin = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const payload: Login = {
      username: userName.value,
      password: passWord.value
    };
    const response = await AuthService.login(payload);
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
      await user.fetchUser();
      router.push({ name: 'home' });
    }
    toast('success', 'Login successful', 'You have successfully logged in.');
    if (response.data.access_token) router.push('/')
  } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Login failed for unknown reason';
    } else {
      error.value = 'Login failed for unknown reason'
    }
    if (Array.isArray(error.value)) {
      for (err in error.value) {
        toast('error', 'Login failed', err as string);
      }
    } else if (typeof(error.value) === 'string') {
      toast('error', 'Login failed', error.value);
    }
  } finally {
    isLoading.value = false;
  }
};
// TODO: we should integrate the Loading and error displaying

// const startOAuth = () => {
//   const authUrl = "http://localhost:8081/api/auth/oauth/github";
//   window.open(authUrl);
// };

const startOAuth = () => {
  const url = "http://localhost:8081/api/auth/oauth/github";

  const width = 600;
  const height = 700;
  const left = window.screenX + (window.outerWidth - width) / 2;
  const top = window.screenY + (window.outerHeight - height) / 2;

  const popup = window.open(
    url,
    'auth-popup',
    `width=${width},height=${height},left=${left},top=${top},scrollbars=yes,status=1`
  );

  return popup;
};

const authChannel = new BroadcastChannel('auth_status');

authChannel.onmessage = (event) => {
  // if (event.data.type === 'AUTH_SUCCESS') {
  router.push('/')
  // }
};

import Loading from '@/components/Loading.vue';

</script>

<template>
    <Loading v-if="isLoading" @finished="isLoading = false" />
  
  <Card v-if="!isLoading" title="Welcome back">
    <p class="description">Sign in to continue to your account</p>
    <button class="btn-github" v-on:click="startOAuth">
      <img src="/img/github-white-icon.png" alt="GitHub" class="github-icon" />
      Continue with GitHub
    </button>
    <div class="separator">
      <span>Or</span>
    </div>
    <Input name="unameoremail" label="Username" id="unameoremail" v-model="userName" />
    <Input name="pword" label="Password" id="pword" v-model="passWord" type="password" />
    <p class="forgot_pass" @click="router.push('reset-password')">Forgot your password</p>

    <div class="btn" style="display: flex;flex-direction: column; gap: 2px;padding: 6px;">
      <Button text="Sign in" @click="handleLogin" style="background-color: #9566B0;"></Button>
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
    // margin: 0;
  }
}
</style>
