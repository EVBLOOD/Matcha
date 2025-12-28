<script setup>
import Button from '@/components/Button.vue';
import Input from '@/components/Input.vue';
import Card from '@/components/Card.vue';
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
            <Button class="btn" to="confirm-email" text="Register"></Button>
            <div class="div_center">Already have an account? <Button class="just_btn" to="signin" backgroundColor="rgba(255, 255, 255, 0)"
                    text="Sign in"></Button></div>
        </Card>
    </div>
</template>

<style lang="scss" scoped>
.page {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
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

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
    }
}
</style>
