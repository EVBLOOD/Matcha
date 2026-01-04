<script setup lang="ts">
import Button from '@/components/Button.vue';
import Input from '@/components/Input.vue';
import Card from '@/components/Card.vue';

import UserService from '@/api/services/UserService'
import type { UserRegister } from '@/types/user';

import { ref } from 'vue';
import { useRouter } from 'vue-router'


const router = useRouter()
const firstName = ref('');
const lastName = ref('');
const email = ref('');
const userName = ref('');
const passWord = ref('');
const confPassWord = ref('');


const isLoading = ref(false);
const error = ref(null);



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
    };
    
    await UserService.register(payload);

    router.push('confirm-email')
  } catch (err: any) {
    error.value = err.response?.data?.errors || err.response?.data?.error || 'Registration failed for unknown reason';
  } finally {
    isLoading.value = false;
  }
};


// TODO: we should integrate the Loading and error displaying
</script>



<template>
    <!-- <div class="page"> -->
        <Card title="Create Your Account">
            <div class="two-inputs">
                <Input name="fname" label="First name" id="fname" v-model="firstName" />
                <Input name="lname" label="Last name" id="lname" v-model="lastName" />
            </div>
            <Input name="email" label="Email" id="email" v-model="email" type="email" />
            <Input name="uname" label="Username" id="uname" v-model="userName" />
            <div class="two-inputs">
                <Input name="pword" label="Password" id="pword" v-model="passWord" type="password" />
                <Input name="cpword" label="Confirm Password" id="cpword" v-model="confPassWord" type="password" />
            </div>
            <Button class="btn" text="Register" @click="handleRegister"></Button>
            <div class="div_center">Already have an account? <Button class="just_btn" to="signin" backgroundColor="rgba(255, 255, 255, 0)"
                    text="Sign in"></Button></div>
        </Card>
    <!-- </div> -->
</template>

<style lang="scss" scoped>
// .page {
//     display: flex;
//     align-items: center;
//     justify-content: center;
//     height: 100%;
// }
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
