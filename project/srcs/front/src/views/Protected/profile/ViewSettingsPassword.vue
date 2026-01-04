<script setup lang="ts">
    import Input from '@/components/Input.vue';
import Button from '@/components/Button.vue';
    import { ref } from 'vue'
    const passWord = ref('');
    const passWordConf = ref('');
const clickSave = (e: Event) => {
    console.log("SAAAAAAAVE ME")
}
</script>

<template>
    <div class="wraper">
        <div class="two_inputs">
    
            <Input name="pass" label="Password" id="pass" v-model="passWord" type="password"/>
            <Input name="confpass" label="Confirm Password" id="confpass" v-model="passWordConf" type="password"/>
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
        }
    }
</style>

