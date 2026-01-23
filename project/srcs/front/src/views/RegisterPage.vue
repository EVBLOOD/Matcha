<script setup lang="ts">
import Button from '@/components/Button.vue';
import Input from '@/components/Input.vue';
import Card from '@/components/Card.vue';
import { toast } from '@/composables/useToast';

import UserService from '@/api/services/UserService'
import type { UserRegister } from '@/types/user';

import { ref } from 'vue';
import { useRouter } from 'vue-router'


interface ValidationErrors {
  [key: string]: string[];
}

const router = useRouter()
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const birthdate = ref('');
const userName = ref('');
const passWord = ref('');
const confPassWord = ref('');


const isLoading = ref(false);
const error = ref<null | string | any[]>(null);



const handleRegister = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const payload : UserRegister = { 
        username: userName.value,
        email: email.value,
        password: passWord.value,
        first_name: firstName.value,
        last_name: lastName.value,
        birthdate: birthdate.value
    };

    if (!firstName.value || !email.value || !passWord.value || !confPassWord.value || !firstName.value || !lastName.value || !birthdate.value || !userName.value) {
      toast('error', 'Registration failed', 'All fields are required');
      return
    }

    if (passWord.value !== confPassWord.value) {
      toast('error', 'Registration failed', 'Passwords do not match');
      return
    }
    
    await UserService.register(payload);

    router.push('confirm-email')
    toast('success', 'Registration success', "Please check your email.");
  } catch (err: any) {
    error.value = err.response?.data?.errors || err.response?.data?.error || 'Registration failed for unknown reason';
    if (Array.isArray(error.value)) {
      for (err in error.value) {
        toast('error', 'Registration failed', err as string);
      }
    } else if (typeof(error.value) === 'string') {
      toast('error', 'Registration failed', error.value);
    } else if (error.value && typeof(error.value) === 'object') {
      const errorData = error.value as ValidationErrors
      Object.entries(errorData).map(([field, messages]) => {
        messages.map((msg) => {
          toast('error', 'Registration failed', msg);
        })
        return messages.map(msg => msg.toUpperCase());
      });
    }
  } finally {
    isLoading.value = false;
  }
};

import Loading from '@/components/Loading.vue';


// TODO: we should integrate the Loading and error displaying
</script>



<template>
  <Loading v-if="isLoading" @finished="isLoading = false" />
        <Card v-if="!isLoading" title="Create Your Account">
            <div class="two-inputs">
                <Input name="fname" label="First name" id="fname" v-model="firstName" />
                <Input name="lname" label="Last name" id="lname" v-model="lastName" />
            </div>
            <Input name="email" label="Email" id="email" v-model="email" type="email" />
            <Input name="uname" label="Username" id="uname" v-model="userName" />
            <Input name="birthdate" label="Birthdate" id="birthdate" v-model="birthdate" type="date" />
            <div class="two-inputs">
                <Input name="pword" label="Password" id="pword" v-model="passWord" type="password" />
                <Input name="cpword" label="Confirm Password" id="cpword" v-model="confPassWord" type="password" />
            </div>
            <Button class="btn" text="Register" @click="handleRegister"></Button>
            <div class="div_center">Already have an account? <Button class="just_btn" to="login" backgroundColor="rgba(255, 255, 255, 0)"
                    text="Sign in"></Button></div>
        </Card>
</template>

<style lang="scss" scoped>

.two-inputs {
    display: flex;
    flex-direction: row;
    gap: 10px;
    
}
.btn {
    margin-top: 5%;
    margin-bottom: 5%;
}

.just_btn {
    margin-top: 0%;
    padding: 0px;
    border-style: none;
}

.div_center {
    display: flex;
    justify-content: center;
    align-content: center;
    width: 100%;
    gap: 5px;
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
    }
}
</style>
