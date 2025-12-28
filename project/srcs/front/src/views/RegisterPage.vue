<script setup>
import Button from '@/components/Button.vue';
import Input from '@/components/Input.vue';
import { ref } from 'vue';

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const userName = ref('');
const passWord = ref('');
const confPassWord = ref('');
</script>

<template>
    <div class="page">
        <div class="content">
            <h2 class="title">Create Your Account</h2>
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
            <Button class="btn" to="confirm-email" text="Register"></Button>
            <div class="div_center">Already have an account? <Button class="just_btn" to="signin" backgroundColor="rgba(255, 255, 255, 0)"
                    text="Sign in"></Button></div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.page {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;

    .content {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        padding: 4%;
        min-height: 50%;
        min-width: 50%;

        .title {
            align-self: center;
            font-weight: 700;
            font-size: 32px;
            margin-bottom: 10%;
        }
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
    }
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
