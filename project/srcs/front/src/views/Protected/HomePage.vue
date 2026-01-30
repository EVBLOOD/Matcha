<script setup lang="ts">
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
import { useSocketStore } from '@/stores/socket';
import { ref } from 'vue';
import AuthService from '@/api/services/AuthService'
import useUserStore from '@/stores/user';
import Loading from '@/components/Loading.vue';

const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const socket = useSocketStore();
const loading = ref(true);

const clickLogOut = async () => {
    try {
        const token = localStorage.getItem('auth_token');
        if (token) socket.disconnectAll(token)
        await AuthService.logout();

        await userStore.fetchUser()
        localStorage.removeItem('auth_token');

        userStore.setIsLoaded(false)

        router.push('login')
    } catch (err) {
        localStorage.removeItem('auth_token');
    }
}

const isActive = (path: string) => {
    if (path === '/') return route.path === '/'
    return route.path.startsWith(path)
}

</script>



<!-- <Loading v-if="loading" :duration="600" @finished="loading = false" /> -->
<template>
    <div class="content">
        <div class="side_bar">
            <img class="logo" style="margin-top: 15px;margin-left: 5%;" src="/img/Logo.svg" width="119px" alt="Logo" />
            <nav class="nav">
                <RouterLink class="link" to="/" :class="{ selected: isActive('/')}"><img src="/img/homeIcon.svg" alt="" /> <span>Explore</span></RouterLink>

                <RouterLink class="link" to="/notifications" :class="{ selected: isActive('/notifications')}">
                    <div class="_link" style="position: relative; overflow: visible;">
                        <div class="icon"><img src="/img/notifMenuIcon.svg" alt="" /></div>
                        <div v-if="socket.getNotifsCount"
                            style="position: absolute; height: 17px; width: 17px; background-color: #EC4B2F; bottom: 10%; left: 55%; font-weight: 600; border-radius: 50%; font-size: x-small; display: flex; justify-content: center; align-items: center;">
                            {{ socket.getNotifsCount > 9 ? '+9' : socket.getNotifsCount }}
                        </div>
                    </div>
                    <span>Notifications</span>
                </RouterLink>

                <RouterLink class="link" to="/messages" :class="{ selected: isActive('/messages')}">
                    <div class="_link" style="position: relative; overflow: visible;">
                        <div class="icon"><img src="/img/messageMenuIcon.svg" alt="" /></div>
                        <div v-if="socket.getMessagesCount"
                            style="position: absolute; height: 17px; width: 17px; background-color: #EC4B2F; bottom: 10%; left: 55%; font-weight: 600; border-radius: 50%; font-size: x-small; display: flex; justify-content: center; align-items: center;">
                            {{ socket.getMessagesCount > 9 ? '+9' : socket.getMessagesCount }}

                        </div>
                    </div>
                    <span>Messages</span>
                </RouterLink>

                <RouterLink class="link" to="/suggestions" :class="{ selected: isActive('/suggestions')}">
                    <div class="icon"><img src="/img/suggestionMenuIcon.svg" alt="" /></div>
                    <span>Suggestions</span>
                </RouterLink>

                <RouterLink class="link" to="/events" :class="{ selected: isActive('/events')}">
                    <div class="icon"><img src="/img/eventMenuIcon.svg" alt="" /></div>
                    <span>Events</span>
                </RouterLink>

                <RouterLink class="link" :to="`/profile/${userStore.getUserID}`" :class="{ selected: isActive('/profile')}">
                    <div class="icon"><img src="/img/profileMenuIcon.svg" alt="" /> </div>
                    <span>Profile</span>
                </RouterLink>
                <a class="link mobile" v-on:click="clickLogOut">
                    <div class="icon"><img src="/img/logOut.svg" alt="" /> </div>
                    <span>Logout</span>
                </a>
            </nav>
            <a class="link desktop" v-on:click="clickLogOut">
                <div class="icon"><img src="/img/logOut.svg" alt="" /> </div>
                <span>Logout</span>
            </a>
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
    color: $text-color;
}


.main_title {
    height: 10%;
    width: 100%;
    border-style: solid;
    border-color: $border-color;
    border-width: 0px 0px 1px 0px;
    padding-left: 3%;
    align-content: center;
    color: $text-color;
}

.main_div_parent {
    width: 100%;
    height: 100%;

    border-style: solid;
    border-color: $border-color;
    border-width: 0px 1px 0px 1px;
}

.side_bar {
    display: flex;
    flex-direction: column;
    gap: 33px;
    // height: 100%;
    width: 20%;
    padding: 10px 10px 40px 10px;
    // margin-right: 1%;
}

.nav {
    display: flex;
    flex-direction: column;
    position: relative;
    // gap: 1px;
    gap: 5px;
    height: 100%;
}

.link {
    cursor: pointer;
    display: flex;
    align-content: center;
    text-decoration: none;
    gap: 10px;
    color: $text-color;
    padding: 12px;
    width: 100%;
    align-items: center;
    min-height: max-content;

    span{
        max-width: auto;
        overflow: hidden;
        text-overflow: ellipsis;
    }
}
.mobile{ display: none;}

.icon{
    height: 20px;
    width: 20px;
    min-width: 20px;
    min-height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    img {
        height: 100%;
        width: 100%;
        object-fit: contain;
    }
}

.link:hover {
    background: $components-hover-color;
    border-radius: 8px;
}

.selected {
    background: $components-hover-color;
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
        background-color: $components-background-color;
    }

    ._link {
            padding: 3%;
            // border-style: solid;
            // border-width: 0px 1px 0px 0px;
            border-color: $border-color;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
    }
    .link {
        padding: 3%;
        border-style: solid;
        border-width: 0px 1px 0px 0px;
        border-color: $border-color;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;

        span {
            // overflow: hidden; // OR
            display: none;
        }
    }
    .mobile{ display: block;}
    .desktop{ display: none;}

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

        padding: 0px;

        .logo {
            display: none;
        }
    }

    .main_title {
        height: 6%;
    }

    .main_div {
        height: 94%;
    }
}
</style>
