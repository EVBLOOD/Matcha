<script setup lang="ts">
import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { useSocialStore } from '@/stores/profile';
import UserService from '@/api/services/UserService';
import axios, { AxiosError } from 'axios';
import { toast } from '@/composables/useToast';

const profile = useSocialStore()


const firstName = ref(profile.activeProfile?.user.first_name);
const lastName = ref(profile.activeProfile?.user.last_name);
const email = ref(profile.activeProfile?.user.email || "");
const userName = ref(profile.activeProfile?.user.username);

const rawDate = new Date(profile.activeProfile?.user.birthdate || Date.now());
const formattedDate = rawDate.toISOString().split('T')[0];
const birthdate = ref(formattedDate);

const router = useRouter()

interface BackendError {
    error?: string;
    errors?: any[];
}

interface ValidationErrors {
    [key: string]: string[];
}

const isLoading = ref(false);
const error = ref<null | string | any[]>(null);


const clickSave = async (e: Event) => {
    try {
        const payload = {
            'first_name': firstName.value,
            'last_name': lastName.value,
            'email': email.value,
            'username': userName.value,
            'birthdate': birthdate.value
        }
        await UserService.change_infos_top(payload);
        toast('success', 'Personal infos update success', "Personal infos were updated successfuly!");
        router.push('/')
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Registration failed for unknown reason';
        } else {
            error.value = 'Change failed for unknown reason'
        }
        if (axios.isAxiosError(err)) {
            error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Personal infos update failed for unknown reason';
        } else {
            error.value = 'Change failed for unknown reason'
        }
        if (Array.isArray(error.value)) {
            error.value.map((err) => {
                toast('error', 'Personal infos update failed', err as string);
            })
        } else if (typeof (error.value) === 'string') {
            toast('error', 'Personal infos update failed', error.value);
        } else if (error.value && typeof (error.value) === 'object') {
            const errorData = error.value as ValidationErrors
            Object.entries(errorData).map(([field, messages]) => {
                messages.map((msg) => {
                    toast('error', 'Personal infos update failed', msg);
                })
                return messages.map(msg => msg.toUpperCase());
            });
        }
    } finally {
        isLoading.value = false;
    }
}
import Loading from '@/components/Loading.vue';

</script>

<template>
    <Loading v-if="isLoading" />
    <div v-if="!isLoading" class="wraper">
        <div class="two_inputs">
            <Input name="uname" label="Username" id="uname" v-model="userName" type="text" />
            <Input name="fname" label="First Name" id="fname" v-model="firstName" type="text" />
            <Input name="lname" label="Last Name" id="lname" v-model="lastName" type="text" />
        </div>
        <div class="two_inputs">
            <Input name="email" label="Email" id="email" v-model="email" type="email" />
            <Input name="birthdate" label="Birthdate" id="birthdate" v-model="birthdate" type="date" />
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
