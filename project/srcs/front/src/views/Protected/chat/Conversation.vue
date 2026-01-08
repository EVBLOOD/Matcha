<script setup lang="ts">
    import { ref, onMounted, watch, nextTick, onUnmounted, useTemplateRef } from 'vue';
    import { useRoute } from 'vue-router';
    import type { ConversationsResponse, MessagesResponse } from '@/types/apiResponses'
    import ChatService from '@/api/services/ChatService'
    import { useSocketStore } from '@/stores/socket'
    import  userUserStore  from '@/stores/user'
    import axios, { AxiosError } from 'axios';
    import { useSocketListener } from '@/composables/useSocketChat'

    interface BackendError {
        error: string;
    }

    // new_message_notification


    const route = useRoute();
    const socketStore = useSocketStore()
    const userStore = userUserStore()
    

    const conversationData = ref<ConversationsResponse[] | null>(null);
    const conversationMessages = ref<MessagesResponse[] | null>(null);
    const isLoading = ref(true);
    const isError = ref<string | null>(null);
    const newMessage = ref('')



    const fetchConversations = async () => {
        if (!route.params.id) return;
        isLoading.value = true;
        try {
            const { data } = await ChatService.getMessages(parseInt(route.params.id as string));
            console.log(data)
            // conversationData.value = data;
            conversationData.value = [...data.data];
            if (conversationData.value[0].messages_list)
                conversationMessages.value = [...conversationData.value[0].messages_list]
            socketStore.joinChat(conversationData.value[0].peer_id.toString())
        } catch (err: unknown) {
            if (axios.isAxiosError(err)) {
                isError.value = (err.response?.data as BackendError)?.error;
            }
            else {
                isError.value = "Registration failed for unknown reason'";
            }
        } finally {
            isLoading.value = false;
        }
    };
    
    onMounted(fetchConversations);

    watch(() => route.params.id, fetchConversations);

    function sendMessage() {
        if (!newMessage.value.trim()) return;

        if (conversationData.value) {
            const id = socketStore.sendMessage(conversationData.value[0].peer_id.toString(), newMessage.value.trim());
            // if (conversationMessages.value)
            //     conversationMessages.value.push({id: id, content: newMessage.value.trim(), is_read: false, sender_id: userStore.getUserID as number, sent_at: "Now"})
        }
        newMessage.value = ''
    }

    onUnmounted(() => {
        if (conversationData.value)
            socketStore.leaveChat(conversationData.value[0].peer_id.toString())
    })


    const pictures_handler = (link: string) => {
        if (link.indexOf('/') > 0) {
            return link
        }
        return `http://localhost:8081/profile/pictures/${link}`
    }


    useSocketListener('message_chat', (params) => {

         if (conversationMessages.value )
                conversationMessages.value.push({id: params.id, content: params.text, is_read: true, sender_id: params.sender as number, sent_at: "Now"})

        console.log(params)
    })

    const messagesContainer = ref<HTMLElement | null>(null);


    watch(
            conversationMessages, scrollToBottom,
            { deep: true }
        );
    

    async function scrollToBottom() {
        await nextTick();
        if (!messagesContainer.value) return;
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
</script>

<template>
    <div class="chat" v-if="conversationData && !isLoading && !isError">
        <div class="header">
            <button class="back-btn" @click="$router.push('/messages')">←</button>
            <div class="user">
                <div class="avatar">
                    <img :src="pictures_handler(conversationData[0].profile_picture_url[0].url)" alt="avatar" />
                </div>
                <div class="infos">
                    <p class="name">{{ conversationData[0].first_name + " " + conversationData[0].last_name}}</p>
                    <div class="status">
                        <span :class="['dot', conversationData[0].last_online ? 'online' : 'offline']"></span>
                        <span class="text">
                            {{ !conversationData[0].last_online ? 'Online' : `Last seen ${conversationData[0].last_online}` }}
                        </span>
                    </div>
                </div>
            </div>
            <button class="btn">View Profile</button>
        </div>
        <div v-if="conversationMessages" class="messages" ref="messagesContainer">
            <div v-for="msg in conversationMessages" :key="msg.id" :class="['message', msg.sender_id == userStore.getUserID ? 'sent' : 'received']">
                {{ msg.content }}
            </div>
        </div>
        <div class="inputBar">
            <textarea v-model="newMessage" placeholder="Type a message..." rows="1"
                @keydown.enter.exact.prevent="sendMessage" @keydown.enter.shift.exact.stop></textarea>
            <button @click="sendMessage"><img src="/img/send.svg" alt="Send"></button>
        </div>
    </div>
</template>

<style lang="scss" scoped>

.chat{
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.chat .header{
    border-bottom: 1px solid $border-color;
    padding: 8px 20px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
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
    border-radius: 50%;
    overflow: hidden;
}

.user .avatar img {
    height: 100%;
    width: 100%;
    object-fit: cover;
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

// .messages::-webkit-scrollbar {
//     width: 6px;
// }

// .messages::-webkit-scrollbar-track {
//     background: transparent;
// }

// .messages::-webkit-scrollbar-thumb {
//     background-color: rgba(255, 255, 255, 0.25);
//     border-radius: 10px;
// }

// .messages::-webkit-scrollbar-thumb:hover {
//     background-color: rgba(255, 255, 255, 0.45);
// }

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

.back-btn {
    display: none;
    background: none;
    border: none;
    color: white;
    font-size: 22px;
    cursor: pointer;
    margin-right: 8px;
    flex-shrink: 0;
}

.btn{
    cursor: pointer;
    border: none;
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 14px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
    flex-shrink: 0;
    height: fit-content;
    background-color: #785D86;
    transition: 0.3s;
}

.btn:hover{
    transition: 0.3s;
    opacity: 0.8;
}

@media (max-width: $breakpoint-md) {
        .back-btn {
            display: block;
        }
        .chat .header{
            display: flex;
            align-items: center;
        }
    }
</style>

