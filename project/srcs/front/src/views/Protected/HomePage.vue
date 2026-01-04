<script setup lang="ts">
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
import AuthService from '@/api/services/AuthService'
import useUserStore from '@/stores/user';
const userStore = useUserStore();
const route = useRoute();
const router = useRouter()

const clickLogOut = async () => {
    console.log("Logout")
    try {
        const response = await AuthService.logout();
        console.log(response)
        localStorage.removeItem('auth_token');
        userStore.fetchUser()
        // userStore.setIsLoaded(false)
        router.push('login')
    } catch (err) {
        console.log(err);
        localStorage.removeItem('auth_token');
    }
}
</script>

<template>
    <div class="content">
        <div class="side_bar">
            <img class="logo" style="margin-top: 15px;margin-left: 5%;" src="/img/Logo.svg" width="119px" alt="Logo" />
            <nav class="nav">
                <RouterLink class="link" to="/"><img src="/img/homeIcon.svg" alt="" /> <span>Home</span></RouterLink>
                <RouterLink class="link" to="/messages"><img src="/img/messagesIcon.svg" alt="" /> <span>Messages</span>
                </RouterLink>
                <RouterLink class="link" to="/notifications"><img src="/img/notificationsIcon.svg" alt="" />
                    <span>Notifications</span>
                </RouterLink>
                <RouterLink class="link" to="/profile/id"><img src="/img/profileIcon.svg" alt="" /> <span>Profile</span>
                </RouterLink>
                <a class="link log_a" v-on:click="clickLogOut"><img src="/img/logOut.svg" alt="" /> <span>Log
                        out</span></a>
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
.content {
    display: flex;
    flex-direction: row;
    height: 100%;
    width: 100%;
}

.main_div {
    width: 100%;
    height: 90%;
    color: #FFFFFF;
}


.main_title {
    height: 10%;
    width: 100%;
    border-style: solid;
    border-color: rgba(255, 255, 255, 0.25);
    ;
    border-width: 0px 0px 1px 0px;
    padding-left: 3%;
    align-content: center;
    color: #E6E6E6;
}

.main_div_parent {
    width: 100%;
    height: 100%;

    border-style: solid;
    border-color: rgba(255, 255, 255, 0.25);
    ;
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
    // gap: 1px;
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
    // height: 6%;
    padding: 6%;
    align-content: center;
    cursor: pointer;
    flex-wrap: wrap;
}

.link:hover {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 8px;

}

@media (max-width: $breakpoint-md) {
    .content {
        flex-direction: column-reverse;
    }

    .nav {
        flex-direction: row;
        position: static;
        justify-content: center;
        align-items: center;
        background-color: #592F6F;
    }


    .link {
    padding: 6%;

        border-style: solid;
        border-width: 0px 1px 0px 0px;
        border-color: rgb(255, 255, 255, 0.25);
        flex-direction: row;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;


        span {
            // overflow: hidden; // OR
            display: none;
        }
    }

    .link:hover {
        border-radius: 0px;

    }

    .nav {
        width: 100%;
        height: fit-content;
    }

    .log_a {
        position: static;
        border-width: 0px 0px 0px 0px;

    }

    .side_bar {
        flex-shrink: 0;
        flex-direction: row;
        height: fit-content;
        gap: 0px;

        width: 100%;
        margin-right: 0%;
        .logo {
            display: none;
        }
    }
}
</style>
