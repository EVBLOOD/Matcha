<script setup>
    import { RouterLink, RouterView, useRoute } from 'vue-router';
    const route = useRoute();
    const clickLogOut = () => {
        console.log("Logout")
        
    }
</script>

<template>
    <div class="content">
        <div class="side_bar">
            <img style="margin-top: 15px;margin-left: 5%;" src="/img/Logo.svg" width="119px" alt="Logo"/> 
            <nav class="nav">
                <RouterLink class="link" to="/"><img src="/img/homeIcon.svg" alt=""/> <span>Home</span></RouterLink>
                <RouterLink class="link" to="/messages"><img src="/img/messagesIcon.svg" alt=""/> <span>Messages</span></RouterLink>
                <RouterLink class="link" to="/notifications"><img src="/img/notificationsIcon.svg" alt=""/> <span>Notifications</span></RouterLink>
                <RouterLink class="link" to="/profile"><img src="/img/profileIcon.svg" alt=""/> <span>Profile</span></RouterLink>
                <a class="link log_a" v-on:click="clickLogOut"><img src="/img/logOut.svg" alt=""/> <span>Log out</span></a>
            </nav>
        </div>
        <div class="main_div_parent">
            <div class="main_title">
                <h2>{{ route.meta.title || 'EVBLOOD is the Title' }}</h2>
            </div>
            <div class="main_div">
                <RouterView />
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .content{
        display: flex;
        flex-direction: row;
        height: 100vh;
    }

    .main_div {
        width: 100%;
    }
    
    .main_title {
        width: 100%;
        border-style: solid;
        border-color: rgba(255, 255, 255, 0.25);;
        border-width: 0px 0px 1px 0px;
        padding: 3%;
        color: #E6E6E6;
    }

    .main_div_parent {
        width: 100%;
        border-style: solid;
        border-color: rgba(255, 255, 255, 0.25);;
        border-width: 0px 1px 0px 1px;
    }

    .side_bar {
        display: flex;
        flex-direction: column;
        gap: 33px;
        height: 100%;
        width: 20%;
        margin-right: 1%;
    }
    

    .nav {
        display: flex;
        flex-direction: column;
        position: relative;
        
        height: 100%;
    }
    .log_a {
        position: absolute;
        bottom: 10%;
    }

    .link {
        display: flex;
        gap: 10px;
        text-decoration: none;
        color: $text-color;
        justify-content: flex-start;
        align-items: center;
        width: 100%;
        height: 44px;
        padding-left: 5%;
        cursor: pointer;
    }
    .link:hover {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 8px;

    }
    // @media (max-width: $breakpoint-md) {
    //     .page{
    //         display: flex;
    //         flex-direction: column;
    //         // margin: 0;
    //     }
    // }
</style>

