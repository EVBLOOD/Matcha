<script setup>
// import Button from '@/components/Button.vue';
// import { RouterLink, RouterView } from 'vue-router';
    import { ref } from 'vue';
    import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
    const users = [
        { id: 1, name: 'Karim Id Bouhouch', date: 'Apr 15, 2025', avatar: '/img/profilePictureDemo.png', online: true, lastSeen: 'Online' },
        { id: 2, name: 'Saad Akllam', date: 'May 01, 2025', avatar: '/img/profilePictureDemo.png', online: false, lastSeen: '2 hours ago' },
        { id: 3, name: 'Sadio Mané', date: 'Jan 01, 2026', avatar: '/img/profilePictureDemo.png', online: true, lastSeen: 'Online' },
        { id: 4, name: 'Mohamed Salah', date: 'Apr 23, 2024', avatar: '/img/profilePictureDemo.png', online: false, lastSeen: '1 day ago' }
    ];
    const selectedUser = ref(users[0])

    const messages = ref([
        { id: 1, text: 'Salam', fromMe: false },
        { id: 2, text: 'Wa salam! Kidayr ?', fromMe: true },
        { id: 3, text: 'Labas hamdullah, nta ?', fromMe: false },
        { id: 4, text: 'Kolchi mzyan', fromMe: true }
    ])
    const newMessage = ref('')

    function sendMessage() {
        if (!newMessage.value.trim()) return
        messages.value.push({ id: Date.now(), text: newMessage.value, fromMe: true })
        newMessage.value = ''
    }

    const router = useRouter();

</script>

<template>
    <div class="content">
        <div class="sideBar">
            <div class="user" v-for="user in users" :key="user.id" @click="() => router.push(`/messages/${user.id}`)">
                <div class="avatar">
                    <img :src="user.avatar" alt="avatar" />
                </div>
                <div class="infos">
                    <p class="name">{{ user.name }}</p>
                    <p class="date">{{ user.date }}</p>
                </div>
            </div>
        </div>
        <RouterView />
    </div>
</template>

<style lang="scss" scoped>
.fa {
    font-size: 25px;
}

.partial {
    background: linear-gradient(90deg, orange 90%, #FFFFFF 0%);
    background-clip: text;
    color: transparent;
}

.checked {
    color: orange;
}

.content {
    color: #FFFFFF;
    display: flex;
    align-items: center;
    height: 100%;
    width: 100%;
}

.sideBar {
    padding: 1%;
    height: 100%;
    width: 30%;
    gap: 2px;
    border-color: rgba(255, 255, 255, 0.25);
    display: flex;
    flex-direction: column;
    border-style: solid;
    border-width: 0px 1px 0px 0px;
}

.chat{
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.chat .header{
    border-bottom: 1px solid $border-color;
    padding: 5px;
    flex-shrink: 0;
}

.user {
    display: flex;
    transition: 0.3s;
    align-items: center;
    padding: 4px;
    gap: 7px;
    user-select: none;
    overflow: hidden;
}

.sideBar .user:hover {
    cursor: pointer;
    background-color: #ffffff1c;
    transition: 0.3s;
    border-radius: 6px;
}

.user .avatar {
    height: 50px;
    width: 50px;
    border-radius: 50%;
    overflow: hidden;
}

.user .avatar img {
    height: 100%;
    width: 100%;
    object-fit: cover;
}

.user .infos {

}

.user .infos .name {
    font-weight: 500;
    font-size: 14px;
}

.user .infos .date {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
}

.messages {
    flex: 1;
    overflow-y: scroll;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    height: 100%;
    width: 100%;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.25) transparent;
}

.message {
    max-width: 60%;
    // overflow: hidden;
    // display: flex;
    // align-items: center;
    padding: 12px 12px;
    border-radius: 10px;
    font-size: 14px;
    flex-shrink: 0;
    white-space: pre-wrap;
    // word-wrap: break-word;
    // overflow-wrap: break-word;
}

.message.received {
    align-self: flex-start;
    background: #807785;
    border-bottom-left-radius: 0;
}

.message.sent {
    align-self: flex-end;
    background: #785D86;
    border-bottom-right-radius: 0;
}

.inputBar {
    position: relative;
    padding: 10px;
    border-top: 1px solid $border-color;
    flex-shrink: 0;
}

.inputBar textarea {
    min-height: 40px;
    max-height: 120px;
    resize: none;
    width: 100%;
    padding: 10px 45px 10px 12px;
    border-radius: 8px;
    border: 1px solid #BD82DD;
    background-color: transparent;
    color: #FFFFFF;
    outline: none;
    line-height: 1.4;
}

.inputBar textarea::placeholder {
    color: rgba(255, 255, 255, 0.6);
}

.inputBar button {
    position: absolute;
    right: 18px;
    top: 50%;
    transform: translateY(-50%);
    background: transparent;
    padding: 6px;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.messages::-webkit-scrollbar {
    width: 6px;
}

.messages::-webkit-scrollbar-track {
    background: transparent;
}

.messages::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.25);
    border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb:hover {
    background-color: rgba(255, 255, 255, 0.45);
}

.status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
}

.dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.dot.online {
    background-color: #22c55e;
}

.dot.offline {
    background-color: rgba(255, 255, 255, 0.4);
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;

        // margin: 0;
    }
}
</style>
