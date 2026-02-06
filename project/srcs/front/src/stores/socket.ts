import { defineStore } from 'pinia';
import { socketChat, socketStatus } from '@/socket/socket';
import { ref } from 'vue';
import { useSocialStore } from '@/stores/profile';
import { toast } from '@/composables/useToast';
import { formatDistanceToNow } from 'date-fns';

import useUserStore from '@/stores/user';
import type { dateProposing } from '@/types/helpers';
import type { UserDatesResponse } from '@/types/apiResponses'

export const useSocketStore = defineStore('socket', {
  state: () => ({
    onlineUsers: {} as Record<string, string>,
    notifications: ref<string[]>([]),
    new_chats_notifs: ref<string[]>([]),
    notifs_counter: ref(0),
    messages_counter: ref(0),
    isBound: false,
    currentConversation: null as null | number,
    EventsData: null as UserDatesResponse[] | null
  }),
  getters: {
    getNotifsCount: (state) => state.notifs_counter,
    getMessagesCount: (state) => state.messages_counter,
    getAllOnliners: (state) => state.onlineUsers,
    getEventsData: (state) => state.EventsData,
  },
  actions: {
    setEventsData(vals: UserDatesResponse[] | null = null) {
      this.EventsData = vals
    },
    setCurrentConversation(val: number | null = null) {
      this.currentConversation = val
    },
    setNotifsCount(val: number) {
      this.notifs_counter = val
    },
    setMessagesCount() {
      socketChat.emit('number_of_messages', (number: number) => {
        this.messages_counter = number
      })
    }, startsocket(heartbeatInterval: any) {
      if (heartbeatInterval) clearInterval(heartbeatInterval);
      heartbeatInterval = setInterval(() => {
        if (socketStatus.connected) {
          socketStatus.emit('ping');
        }
      }, 20000);
    }
    ,
    bindStatusEvents() {
      if (this.isBound) return;

      let heartbeatInterval;
      this.startsocket(heartbeatInterval)

      socketStatus.on('user_status_change', (response) => {
        const id: string = response.user_id;
        const value: string = response.status;

        this.onlineUsers[id] = value === "online" ? "Online" : formatDistanceToNow(new Date(value), { addSuffix: true });
      });

      socketStatus.on('notify', (msg) => {
        if (msg.type != 'dislike' && msg.source_id != useUserStore().getUserID)
          this.notifs_counter++
        this.handleSocialEvent(msg.type, { "username": msg.user.user.username, "avatar": msg.user.pictures[0].url, "userId": msg.dst_id, "conversation_id": msg.conversation_id, "FromId": msg.source_id, "date_id": msg.date_id });
        this.notifications.push(msg);
      });

      socketChat.on('new_message_notification', (msg) => {
        if (this.currentConversation && msg.conv == this.currentConversation) return
        this.messages_counter++
        toast('message', 'New message', "sent you a message.", msg.user_data.pictures[0].url, msg.conv, msg.user_data.user.username);
        this.new_chats_notifs.push(msg);
      });
      socketStatus.emit('number_of_notifs', (number: number) => {
        this.notifs_counter = number
      })
      socketChat.emit('number_of_messages', (number: number) => {
        this.messages_counter = number
      })
    },
    bindChatEvents() {
      if (this.isBound) return;
      socketChat.on('connect', () => { });
      socketChat.on('disconnect', () => { });
    },
    connectAll() {
      const token = localStorage.getItem('auth_token');
      if (!token) return;
      socketChat.io.opts.extraHeaders = {
        Authorization: `Bearer ${token}`
      };
      socketStatus.io.opts.extraHeaders = {
        Authorization: `Bearer ${token}`
      };
      if (!socketChat.connected) socketChat.connect();
      if (!socketStatus.connected) socketStatus.connect();
      this.bindStatusEvents();

      this.isBound = true;
    },
    reachStausOneUser(id: string) {

      socketStatus.emit("check_user_connect", id, (response: any) => {
        if (response) {
          this.onlineUsers[id] = (response.status === "Online" || response.status === true) ? "Online" : formatDistanceToNow(new Date(response.status), { addSuffix: true })
        }
      })
    },
    reachStausManyUsers(ids: string[]) {
      socketStatus.emit("check_users_connect", ids, (response: any[]) => {
        if (response) {
          const id: string[] = Object.keys(response)
          response.forEach((v) => {
            const id: string = Object.keys(v)[0];
            const value: string = Object.values(v)[0] as string;
            this.onlineUsers[id] = value;
          });
        }
      })
    },
    joinChat(id: any) {
      socketChat.emit('join_chat', { user_id: id }, ((resp: any) => {
      }))
    },
    JoinUser(id: any) {
      socketChat.emit('join_video_chat', { user_id: id }, ((resp: any) => {
      }))
    },
    CallUser(id: string, type: string, args: any) {
      socketChat.emit('video_call', { user_id: id, type: type, args: args })
    },
    leaveChat(id: string) {
      socketChat.emit('join_chat', { user_id: id })
    },
    sendMessage(id: string, content: string): number {
      let id_message = undefined
      socketChat.emit('send_message', { user_id: id, text: content }, ((resp: any) => {
        if (typeof (resp) == 'object' && resp.error) {
          toast('error', 'Send Message fail', resp.error);
        }
        id_message = resp as number
      }))
      return id_message || -1
    },
    UserStatus(id: string) {
      return this.onlineUsers[id]
    },
    propose_date(userData: dateProposing) {
      let rtrn = false

      socketStatus.emit('propose_date', userData, ((resp: any) => {
        rtrn = resp
      }))
      return rtrn
    },
    respond_to_date(event_id: number, status: string) {

      socketStatus.emit('respond_to_date', {"event_id": event_id, "status": status }, ((resp: any) => {

      }))
    },
    disconnectAll() {
      if (!this.isBound) return;


      socketChat.off();
      socketStatus.off();

      if (socketStatus.connected) socketStatus.disconnect();

      this.isBound = false;
    },
    interactWithUser(user_id: number, type: string) {
      const token = localStorage.getItem('auth_token');
      socketStatus.io.opts.extraHeaders = {
        Authorization: `Bearer ${token}`
      };
      socketStatus.emit(type, user_id)
    },
    handleSocialEvent(type: string, payload: any) {
      const profileStore = useSocialStore();

      switch (type) {
        case 'match':
          profileStore.handleNewMatch(payload.FromId, payload.userId, payload.conversation_id);
          if (payload.FromId != useUserStore().getUserID)
            toast('like', 'New match', "matched your profile.", payload.avatar, payload.FromId, payload.username);
          break;
        case 'unmatch':
          profileStore.handleUnMatch(payload.FromId, payload.userId,);
          if (payload.FromId != useUserStore().getUserID)
            toast('info', 'New unmatch', "unmatch your profile.", payload.avatar, payload.FromId, payload.username);
          break;
        case 'like':
          if (payload.FromId != useUserStore().getUserID)
            toast('info', 'New like', "liked your profile.", payload.avatar, payload.FromId, payload.username);
          profileStore.handleLike(payload.FromId, payload.userId, 0);
          break;
        case 'dislike':
          profileStore.handleDislike(payload.FromId, payload.userId, 0);
          break;
        case 'view':
          toast('view', 'Profile New', "viewed your profile.", payload.avatar, payload.FromId, payload.username);

          if (profileStore.activeProfile?.user.user_id === payload.userId && profileStore.activeProfile?.interactions.views_count) {
            profileStore.activeProfile.interactions.views_count++;
          }
          break;

        case 'block':
          profileStore.handleBlock(payload.userId, payload.userId);
          break;
        default :
          if (this.EventsData)
            this.EventsData = this.EventsData?.map((evnt) => {
                    if (evnt.id == payload.date_id) {
                        evnt.status = type.split(' ')[1];
                    }
                    return evnt
          })
          if (payload.FromId != useUserStore().getUserID)
            toast('view', type, type, payload.avatar, payload.FromId, payload.username);
          break
      }
    }
  }
});