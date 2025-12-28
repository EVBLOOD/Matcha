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
        <div>Forgot password? <Button to="Reset" text="Reset Password"></Button></div>
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
        margin-top: 10px;
        margin-bottom: 10px;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

