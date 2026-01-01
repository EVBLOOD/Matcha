<script setup>
    import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
    import { ref } from 'vue'
    const firstName = ref('');
    const lastName = ref('');
    const email = ref('');
    const userName = ref('');
const clickSave = (e) => {
    console.log("SAAAAAAAVE ME")
}
</script>

<template>
    <div class="wraper">
        <div class="two_inputs">
    
            <Input name="fname" label="First Name" id="fname" v-model="firstName" type="text"/>
            <Input name="lname" label="Last Name" id="lname" v-model="lastName" type="text"/>
        </div>
        <div class="two_inputs">
    
            <Input name="email" label="Email" id="email" v-model="email" type="email"/>
            <Input name="uname" label="Username" id="uname" v-model="userName" type="text"/>
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
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

