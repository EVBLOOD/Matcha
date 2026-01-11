<script setup lang="ts">
import Card from '@/components/Card.vue';
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';

import AuthService from '@/api/services/AuthService'

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

const handleLogin = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const payload : Login = { 
           username: userName.value,
           password: passWord.value
       };
       const response = await AuthService.login(payload);
       localStorage.setItem('auth_token', response.data.access_token);
       router.push('/')
     } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Registration failed for unknown reason';
        } else {
            error.value = 'Registration failed for unknown reason'
        }
     } finally {
       isLoading.value = false;
     }
};
// TODO: we should integrate the Loading and error displaying

</script>

<template>
        <Card title="Create Your Account">
            <Input name="unameoremail" label="Username" id="unameoremail" v-model="userName" />
            <Input name="pword" label="Password" id="pword" v-model="passWord" type="password"/>
            <!-- <Button  class="btn" text="Login" @click="handleLogin"></Button> -->

            <div class="btn" style="display: flex;flex-direction: column; gap: 2px;padding: 6px;">
                <Button text="Login" @click="handleLogin"  style="background-color: #DEB0F5;"></Button>
                <Button text="Register" to="register"></Button>
            </div>
        <div class="extra">Forgot password? <Button class="just_btn" to="Reset" text="Reset Password" backgroundColor="rgba(255, 255, 255, 0)"></Button></div>
        </Card>
</template>

<style lang="scss" scoped>
    .btn {
        margin-top:  5%;
        margin-bottom:  5%;
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
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

