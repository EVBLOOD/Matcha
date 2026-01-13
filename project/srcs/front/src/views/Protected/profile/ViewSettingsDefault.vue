<script setup lang="ts">
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { useSocialStore } from '@/stores/profile';
import UserService from '@/api/services/UserService';
import axios, { AxiosError } from 'axios';

const profile = useSocialStore()


const firstName = ref(profile.activeProfile?.user.first_name);
const lastName = ref(profile.activeProfile?.user.last_name);
const email = ref(profile.activeProfile?.user.email || "");
const userName = ref(profile.activeProfile?.user.username);

const router = useRouter()

interface BackendError {
  error?: string;
  errors?: any[];
}

const isLoading = ref(false);
const error = ref<null | string | any[]>(null);


const clickSave = async (e: Event) => {
    try {
        const payload = {
            'firstname': firstName.value,
            'lastname': lastName.value,
            'email': email.value,
            'userName': userName.value,
        }
       await UserService.change_infos_top(payload);
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

            <Input name="fname" label="First Name" id="fname" v-model="firstName" type="text" />
            <Input name="lname" label="Last Name" id="lname" v-model="lastName" type="text" />
        </div>
        <div class="two_inputs">

            <Input name="email" label="Email" id="email" v-model="email" type="email" />
            <Input name="uname" label="Username" id="uname" v-model="userName" type="text" />
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
        // margin: 0;
    }
}
</style>
