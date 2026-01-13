<script setup lang="ts">
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import { ref } from 'vue'
import UserService from '@/api/services/UserService'
import { useRouter } from 'vue-router'
import axios, { AxiosError } from 'axios';

const passWord = ref('');
const passWordConf = ref('');
const router = useRouter()

interface BackendError {
  error?: string;
  errors?: any[];
}

const isLoading = ref(false);
const error = ref<null | string | any[]>(null);


const clickSave = async (e: Event) => {
    try {
       await UserService.changePassword(passWord.value);
       router.push('/')
     } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Registration failed for unknown reason';
        } else {
            error.value = 'Change failed for unknown reason'
        }
     } finally {
       isLoading.value = false;
     }
}
</script>

<template>
    <div class="wraper">
        <div class="two_inputs">

            <Input name="pass" label="Password" id="pass" v-model="passWord" type="password" />
            <Input name="confpass" label="Confirm Password" id="confpass" v-model="passWordConf" type="password" />
        </div>

        <Button class="btn" text="Save" @click="clickSave"></Button>
    </div>

</template>

<style lang="scss" scoped>
.btn {
    width: 100%;
}

.wraper {
    height: 100%;
    width: 100%;
    padding-top: 5%;
}

.two_inputs {
    display: flex;
    justify-content: space-between;
    flex-wrap: nowrap;
    gap: 2%;
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
    }
}
</style>
