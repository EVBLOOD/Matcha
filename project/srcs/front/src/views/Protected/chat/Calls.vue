<script setup lang="ts">
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import type { ConversationsResponse, MessagesResponse } from '@/types/apiResponses'
import ChatService from '@/api/services/ChatService'
import { useSocketStore } from '@/stores/socket'
import userUserStore from '@/stores/user'
import axios from 'axios';
import { useSocketListener } from '@/composables/useSocketChat'
import Input from '@/components/Input.vue';
import { toast } from '@/composables/useToast';
import Alert from '@/components/Alert.vue';

interface BackendError {
    error: string;
}

// new_message_notification


const route = useRoute();
const socketStore = useSocketStore()
const userStore = userUserStore()


const conversationData = ref<ConversationsResponse[] | null>(null);
const conversationMessages = ref<MessagesResponse[]>([]);

const isLoading = ref(true);
const isError = ref<string | null>(null);
const newMessage = ref('')
const ProposeDateVisible = ref(false);


const fetchConversations = async () => {
    if (!route.params.id) return;
    isError.value = ""
    isLoading.value = true;
    try {
        const { data } = await ChatService.getMessages(parseInt(route.params.id as string));
        // conversationData.value = data;
        conversationData.value = [...data.data];
        if (conversationData.value[0].messages_list)
            conversationMessages.value = [...conversationData.value[0].messages_list]
        socketStore.reachStausOneUser(conversationData.value[0].peer_id.toString())
        socketStore.joinChat(conversationData.value[0].peer_id.toString())
        socketStore.setMessagesCount()
        socketStore.setCurrentConversation(conversationData.value[0].conversation_id)
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Registration failed for unknown reason'";
        }
        router.push({ name: 'not-found' });

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
    socketStore.setCurrentConversation()
})


const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}


useSocketListener('message_chat', (params) => {

    if (conversationMessages.value)
        conversationMessages.value.push({ id: params.id, content: params.text, is_read: true, sender_id: params.sender as number, sent_at: "Now" })

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

const callStore = useCallStore()

const startCall = async () => {
    if (!conversationData.value) return
    callStore.initiateCall(conversationData.value[0].peer_id.toString(), conversationData.value[0].first_name + " " + conversationData.value[0].last_name, conversationData.value[0].profile_picture_url[0].url)
};

import { useRouter } from 'vue-router';

const router = useRouter()

const go_to = (id: number) => {
  router.push( `/profile/${id}`)

}



import EventService from '@/api/services/EventService';
import type { dateProposing } from '@/types/helpers';

interface BackendError {
  error: string;
}
interface ValidationErrors {
  [key: string]: string[];
}
const partner_id = ref(1);
const location = ref('');
const time_str = ref('');
const datetime_str = ref('');
const date_str = ref('');
const description = ref('');

const AddEvents = async () => {
    if (!conversationData.value) return
  isLoading.value = true;
  try {
    await EventService.propose_date({
        partner_id: conversationData.value[0].peer_id || -1,
        location: location.value,
        datetime_str:(new Date(date_str.value + " " + time_str.value)).toISOString(),
        description: description.value
    });
    toast("success", "Date Invite Sent", "Your date invite has been sent successfully!")
    ProposeDateVisible.value = false;
  } catch(err : unknown) {
    if (axios.isAxiosError(err)) {
      isError.value = err.response?.data?.errors || err.response?.data?.error || 'Date Invite failed for unknown reason';
    } else {
      isError.value = 'Date Invite failed for unknown reason'
    }
    if (Array.isArray(isError.value)) {
      for (err in isError.value) {
        toast('error', 'Date Invite failed', err as string);
      }
    } else if (typeof (isError.value) === 'string') {
      toast('error', 'Date Invite failed', isError.value);
    } else if (isError.value && typeof (isError.value) === 'object') {
      const errorData = isError.value as ValidationErrors
      Object.entries(errorData).map(([field, messages]) => {
        messages.map((msg) => {
          toast('error', 'Date Invite failed', msg);
        })
        return messages.map(msg => msg.toUpperCase());
      });
    }
    
  } finally {
    isLoading.value = false;
  }
};
const send_invite = async () => {
    if (!date_str.value || !time_str.value || !location.value) {
        toast("error", "Incomplete Data", "Please fill in all the fields to send a date invite.")
        return;
    }

    await AddEvents()
    // if (add_event){
    //     toast("success", "Date Invite Sent", "Your date invite has been sent successfully!")
    //     ProposeDateVisible.value = false;
    // }
}


import Loading from '@/components/Loading.vue';
import {  computed } from 'vue';
import { useCallStore } from '@/stores/call';

const statusUser = computed(() => {
    if (conversationData.value) {
        const userId = conversationData.value[0].peer_id;
        if (!userId) return 'Offline';
        return socketStore.UserStatus(userId.toString());
    }
});

</script>

<template>
    <Loading v-if="isLoading" />
    <div class="chat" v-if="conversationData && !isLoading && !isError">
        <div class="header">
            <button class="back-btn" @click="$router.push('/messages')">←</button>
            <div class="user" @click="go_to(conversationData[0].peer_id)" style="cursor: pointer;">
                <div class="avatar">
                    <img :src="pictures_handler(conversationData[0].profile_picture_url[0].url)" alt="avatar" />
                </div>
                <div class="infos">
                    <p class="name">{{ conversationData[0].first_name + " " + conversationData[0].last_name }}</p>
                    <div class="status">
                        <span :class="['dot', conversationData[0].last_online ? 'online' : 'offline']"></span>
                        <span class="text">
                            {{ statusUser }}
                        </span>
                    </div>
                </div>
            </div>
            <div class="buttons">
                <button class="btn-propose-date" @click="ProposeDateVisible = !ProposeDateVisible"><img src="/img/ProposeDate.svg" alt="video call"><p>Propose a Date</p></button>
                <button class="btn-call-video" @click="startCall"><img src="/img/videoCall.svg" alt="video call"></button>
            </div>
        </div>
        <div class="messages" ref="messagesContainer">
            <div v-if="!conversationMessages.length" class="empty-state">
                <h3>No messages yet.</h3>
                <p>Start the conversation.</p>
            </div>
            <div v-else v-for="msg in conversationMessages" :key="msg.id"
                :class="['message', msg.sender_id == userStore.getUserID ? 'sent' : 'received']">
                {{ msg.content }}
            </div>
        </div>
        <div class="inputBar">
            <textarea v-model="newMessage" placeholder="Type a message..." rows="1"
                @keydown.enter.exact.prevent="sendMessage" @keydown.enter.shift.exact.stop></textarea>
            <button @click="sendMessage"><img src="/img/send.svg" alt="Send"></button>
            <!-- <button @click="startCall">Start Call</button> -->
        </div>
    </div>

    <Alert 
        v-model="ProposeDateVisible" 
        title="Propose a Date"
        @confirm="send_invite"
        confirm-text="Send Invite"
        size="medium"
    >
        <div class="content">
            <div class="date_time">
                <Input v-model="date_str" variant="popup" label="Select Date" type="date" />
                <Input v-model="time_str" variant="popup" label="Time" type="time" />
            </div>
            <Input v-model="location" variant="popup" label="Location" />
            <Input v-model="description" variant="popup" label="Message" />
        </div>
        <!-- <template #footer>
            <div class="footer">
                <button class="btn-cancel-invite" @click="ProposeDateVisible = false">Cancel</button>
                <button class="btn-send-invite" @click="send_invite">Send Invite</button>
            </div>
        </template> -->
    </Alert>
</template>

<style lang="scss" scoped>

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

.content{
    width: 100%;
    .date_time{
        display: flex;
        gap: 10px;
    }
}
.footer{
    display: flex;
    justify-content: flex-end;
    // margin-top: 20px;
    gap: 10px;
    width: 100%;
    .btn-send-invite {
        @extend .btn;
        font-size: 15px;
        padding: 15px 30px;
        flex: 1;
    }
    .btn-cancel-invite {
        @extend .btn;
        padding: 15px 30px;
        font-size: 15px;
        background-color: #E8DCEF;
        color: #592F6F;
        flex: 1;
        &:hover {
            background-color: #d5c1e0;
        }
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

.buttons{
    display: flex;
    gap: 10px;
    flex-shrink: 0
}

.btn-propose-date {
    @extend .btn;
    color: #592F6F;
    flex-shrink: 0;
    background-color: #C39FD8;
    gap: 8px;
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

.chat {
    display: flex;
    flex-direction: column;
    // display: grid;
    // grid-template-rows: auto 1fr auto;
    // height: 100vh;

    width: 100%;
    height: 100%;
}

.chat .header {
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

.user .infos .name {
    font-weight: 500;
    font-size: 14px;
}

.user .infos .date {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.6);
}

.messages {
    // flex: 1;
    flex: 1 1 auto;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    height: 100%;
    width: 100%;
    scrollbar-width: thin;
    scrollbar-color: rgba(255, 255, 255, 0.25) transparent;
    min-height: 0;
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

.empty-state{
    margin: auto;
    opacity: 0.6;
    font-size: 17px;
    text-align: center;
    
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

.status {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    min-width: fit-content;
}

.dot {
    width: 8px;
    height: 8px;
    min-width: 8px;
    min-height: 8px;
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

@media (max-width: $breakpoint-md) {
    .back-btn {
        display: block;
    }

    .chat .header {
        display: flex;
        align-items: center;
    }

    .btn{
        padding: 8px;
    }

    .box .user .name{
        font-size: 14px;
    }

    .btn-propose-date {
        p {
            display: none;
        }
    }
}
</style>
