<script setup lang="ts">
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
import { useSocketStore } from '@/stores/socket';
import { ref, watch } from 'vue';
import AuthService from '@/api/services/AuthService'
import useUserStore from '@/stores/user';
import Loading from '@/components/Loading.vue';
import { useCallStore } from '@/stores/call';
import { useSocketListener } from '@/composables/useSocketChat';
import { toast } from '@/composables/useToast';

const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const socket = useSocketStore();
const loading = ref(true);

const clickLogOut = async () => {
    try {
        const token = localStorage.getItem('auth_token');
        if (token) socket.disconnectAll()
        await AuthService.logout();

        await userStore.fetchUser()
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');

        userStore.setIsLoaded(false)

        router.push('login')
    } catch (err) {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('refresh_token');
    }
}

const isActive = (path: string) => {
    if (path === '/') return route.path === '/'
    return route.path.startsWith(path)
}




const callStore = useCallStore()
const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}


const rtcConfig: RTCConfiguration = {
    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
};

let pc: RTCPeerConnection | null = null;
let localStream: MediaStream | null = null;


const localVideo = ref<HTMLVideoElement | null>(null);
const remoteVideo = ref<HTMLVideoElement | null>(null);


const createPeerConnection = () => {
    pc = new RTCPeerConnection(rtcConfig);

    pc.ontrack = (event: RTCTrackEvent) => {
        if (remoteVideo.value) {
            remoteVideo.value.srcObject = event.streams[0];
        }
    };

    pc.onicecandidate = (event: RTCPeerConnectionIceEvent) => {
        if (event.candidate) {
            callStore.sendSignal('candidate', event.candidate);
        }
    };
};

const setupWebRTC = async () => {
    createPeerConnection();

    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        if (localVideo.value) localVideo.value.srcObject = localStream;

        localStream.getTracks().forEach(track => {
            if (pc && localStream) pc.addTrack(track, localStream);
        });
    } catch (err) {
        console.log("Access denied for camera/mic");
    }
};


const startCall = async () => {
    await setupWebRTC();

    if (!pc) return;

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    callStore.sendSignal('offer', offer);
};

watch(() => callStore.isCalling, async (isCalling) => {

    if (callStore.callState === 'dialing' && !pc && isCalling) {
        await startCall()
    }
});


const acceptCall = async () => {

    await setupWebRTC();
    if (callStore.pendingOffer) {
        await pc?.setRemoteDescription(new RTCSessionDescription(callStore.pendingOffer));
        const answer = await pc?.createAnswer();
        await pc?.setLocalDescription(answer);
        
        callStore.sendSignal('answer', answer);
        callStore.setConnected();
    }
};

useSocketListener('video_signal', async (data) => {
    if (data.type === 'offer') {
        callStore.receiveIncoming(data.sender_id, data.sender_name, data.sender_avatar, data.args);
    }
    else if (data.type === 'answer') {
        if (pc) {
            await pc.setRemoteDescription(new RTCSessionDescription(data.args));
            callStore.setConnected();
        }
    }
    else if (data.type === 'candidate') {
        if (pc) {
            await pc.addIceCandidate(new RTCIceCandidate(data.args));
        }
    } else if (data.type === 'hangup') {
        endCall(false);
    } else if (data.type === 'busy') {
        toast('call', 'Busy', 'User is on another call.')
        endCall(false);
    } else if (data.type === 'offline') {
        toast('call', 'Offline', 'User is not connected.')
        endCall(false);
    } else if (data.type === 'timeout') {
        toast('call', 'No answer', 'Call timed out.')
        endCall(false);
    }
});


const endCall = (sendSignal: boolean = true) => {
    if (sendSignal) {
        callStore.sendSignal('hangup', null);
    }
    localStream?.getTracks().forEach(t => t.stop());
    pc?.close();
    pc = null;
    localStream = null;
    callStore.reset();
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
        <Teleport to="body">
            <div v-if="callStore.isCalling" class="video-call">
                <div>
                    <div v-if="callStore.callState === 'dialing'" class="box">
                        <div class="user">
                            <div class="avatar">
                                <img :src="pictures_handler(callStore.activePeer?.avatar || '')" alt="Avatar">
                            </div>
                            <p class="name">{{callStore.activePeer?.name}}</p>
                        </div>
                        <p class="status-call">Calling...</p>
                        <button @click="endCall()" class="btn-cancel">Cancel</button>
                    </div>

                    <div v-if="callStore.callState === 'ringing'" class="box">
                        <div class="user">
                            <div class="avatar">
                                <img :src="pictures_handler(callStore.activePeer?.avatar || '')" alt="Avatar">
                            </div>
                            <p class="name">{{callStore.activePeer?.name}}</p>
                        </div>
                        <p class="status-call">Incoming Call...</p>
                        <div class="btn-call">
                            <button class="btn-accept" @click="acceptCall()">
                                <img src="/img/btn-accept-call.svg" alt="Accept">
                                <p>Accept</p>
                            </button>
                            <button class="btn-decline" @click="endCall()">
                                <img src="/img/btn-decline-call.svg" alt="Decline">
                                <p>Decline</p>
                            </button>
                        </div>
                    </div>

                    <div v-show="callStore.callState === 'connected'" class="box-video-call">
                        <div class="videos">
                            <div class="video1">
                                <video ref="remoteVideo" autoplay playsinline></video>
                                <p>{{callStore.activePeer?.name}}</p>
                            </div>
                            <div class="video2">
                                <video ref="localVideo" autoplay muted playsinline></video>
                                <p>{{userStore.getUserName}}</p>
                            </div>
                        </div>
                        <div @click="endCall()" class="btn-hang-up"><img src="/img/hang-up.svg"></div>
                    </div>
                </div>
            </div>
        </Teleport>
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
    width: 20%;
    padding: 10px 10px 40px 10px;
}

.nav {
    display: flex;
    flex-direction: column;
    position: relative;
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

.btn {
    cursor: pointer;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    font-family: $font-main;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    font-weight: 600;
    color: white;
    background-color: #9566B0;
    transition: all 0.2s ease;
    
    &:hover {
        filter: brightness(1.1);
    }
}

.video-call {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.9);
    z-index: 30;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
}

.box{
    background-color: #E2BDF6;
    width: 400px;
    padding: 20px;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #592F6F;
}

.box-video-call{
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    background-color: #E2BDF6;
    padding: 30px;
    color: #592F6F;
    .videos{
        display: flex;
        gap: 20px;
        .video1, .video2{
            display: flex;
            flex-direction: column;
            align-items: start;
            font-weight: 600;
            font-size: 13px;
            gap: 4px;
            video{
                width: 300px;
                max-height: max-content;
                background: #333;
                border-radius: 10px;
            }
        }
    }
    .btn-hang-up{
        cursor: pointer;
        transition: 0.3s;
        &:hover {
            transform: scale(1.1);
            transition: 0.3s;
        }
    }
}

.status-call{
    font-weight: 500;
    font-size: 13px;
    margin-bottom: 25px;
}

.btn-accept {
  @extend .btn;
  background-color: #9566B0;
  color: white;

  &:hover {
    background-color: #7e52a0;
  }
}

.btn-decline {
  @extend .btn;
  background-color: #E8DCEF;
  color: #592F6F;

  &:hover {
    background-color: #d5c1e0;
  }
}

.btn-cancel {
  @extend .btn;
  width: 100%;
  background-color: #E8DCEF;
  color: #592F6F;

  &:hover {
    background-color: #d5c1e0;
  }
}

.btn-call {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 6px;
}

.btn-call-video {
    @extend .btn;
    color: #592F6F;
    flex-shrink: 0;
    background-color: #FEA8FF;
    gap: 8px;
}


.box .user {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.box .user .name{
    font-weight: 600;
    font-size: 18px;
}

video {
    width: 300px;
    background: #333;
}

.user {
    display: flex;
    transition: 0.3s;
    align-items: center;
    padding: 4px;
    gap: 7px;
    user-select: none;
    width: 100%;
}

.user .avatar {
    height: 50px;
    width: 50px;
    min-height: 50px;
    min-width: 50px;
    border-radius: 50%;
    overflow: hidden;
}

.user .avatar img {
    height: 100%;
    width: 100%;
    object-fit: cover;
}

.user .name {
    font-weight: 500;
    font-size: 14px;
    color: #592F6F;
}

.user {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
}

@media (max-width: $breakpoint-md) {
    .back-btn {
        display: block;
    }


    .btn{
        padding: 8px;
    }

    .box .user .name{
        font-size: 14px;
    }


}
</style>
