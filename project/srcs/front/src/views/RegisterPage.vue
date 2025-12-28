<script setup>
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="page">
        <div class="content">
            <h2>Create Your Account</h2>
            <label for="fname"> first name</label> <input name="fname" type="text">
            <label for="lname"> last name</label> <input name="lname" type="text">
            <label for="email"> email</label> <input name="email" type="email">
            <label for="uname"> username</label> <input name="uname" type="text">
            <label for="pword"> PassWord</label> <input name="pword" type="password">
            <label for="cpword"> Confirm PassWord</label> <input name="cpword" type="password">
            <Button to="confirm-email" text="Register"></Button>
            <div>Already have an account <Button to="signin" text="Sign in"></Button></div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .page{
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 40px 20px;
        .content {
            overflow: hidden;
            p {
                margin-bottom: 30px;
            }
        }
        .title{
            font-weight: 700;
            font-size: 40px;
        }
        .description{
            font-size: 30px;
        }
        .image img{
            height: auto;
            width: 100%;
        }
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

