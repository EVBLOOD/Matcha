<script setup>
import Card from '@/components/Card.vue';
    import Input from '@/components/Input.vue';
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="page">
        <Card title="Create Your Account">
            <Input name="unameoremail" label="First name" id="unameoremail" v-model="firstName" />
            <Input name="pword" label="First name" id="pword" v-model="firstName" />
        <Button class="btn" to="home" text="Register"></Button>
        <div class="extra">Forgot password? <Button class="just_btn" to="Reset" text="Reset Password" backgroundColor="rgba(255, 255, 255, 0)"></Button></div>
        </Card>
    </div>
</template>

<style lang="scss" scoped>
    .page{
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 40px 20px;
    }
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

