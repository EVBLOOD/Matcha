<script setup>
    // import Button from '@/components/Button.vue';
    // import { RouterLink, RouterView } from 'vue-router';

</script>

<template>
    <div class="content">
        <div class="sideBar">
            <div>
                <img width="90%" style="margin-bottom: 22px;" src="/img/avatar.svg" alt="">
                <div style="font-weight:500; font-size: 26px;">Saad Akllam</div>
                <div><div></div> Online</div>
            </div>
            <div>
                <div> <img src="/img/logOut.svg" alt=""> Profile Views :  324</div>
                <div> <img src="/img/logOut.svg" alt=""> Likes Received :  105</div>
            </div>
            <div>
                <p>Fame Rating 🔥</p>
                <div>stars</div>
            </div>
        </div>
        <div>
            LOL
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .content{
        height: 100%;

        color: #FFFFFF;
        // padding: 3%;
        display: flex;
        // flex-direction: row;
        align-items: center;
        // justify-content: center;
        height: 100%;
        width: 100%;
    }
    .sideBar {
        padding: 5%;
        border-color: rgba(255, 255, 255, 0.25);;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: start;
        justify-content: center;
        gap: 50px;
        border-style: solid;
        border-width: 0px 1px 0px 0px;
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;

            // margin: 0;
        }
    }
</style>

