import { defineStore } from 'pinia';
import { socketChat, socketStatus } from '@/socket/socket';
import { ref } from 'vue';
import { useSocialStore } from '@/stores/profile';
import { toast } from '@/composables/useToast';


export const useSocketStore = defineStore('socket', {
  state: () => ({
    onlineUsers: new Map<string, string>(),
    notifications: ref<string[]>([]),
    new_chats_notifs: ref<string[]>([]),
    notifs_counter: ref(0),
    messages_counter: ref(0),
    isBound: false,
  }),
  getters: {
    getNotifsCount: (state) => state.notifs_counter,
    getMessagesCount: (state) => state.messages_counter,
  },
  actions: {
    setNotifsCount(val: number) {
      this.notifs_counter = val
    },
    setMessagesCount() {
      socketChat.emit('number_of_messages', (number: number) => {
        console.log(number)
        this.messages_counter = number
      })
    },
    bindStatusEvents() {
      if (this.isBound) return;
      socketStatus.on('connected', (response) => {
        console.log(response);
        const id: string = Object.keys(response)[0];
        const value: string = Object.values(response)[0] as string;
        this.onlineUsers.set(id, value);
      });

      socketStatus.on('notify', (msg) => {
        console.log(msg)
        this.notifs_counter++
        this.handleSocialEvent(msg.type, { "username": msg.user.user.username, "avatar": msg.user.pictures[0].url, "userId": msg.dst_id, "conversation_id": msg.conversation_id, "FromId": msg.source_id });
        this.notifications.push(msg);
      });

      socketChat.on('new_message_notification', (msg) => {
        // toast('error', ' sent you a message.', msg);
        this.messages_counter++

        console.log(msg.user_data)
        console.log(msg.user_data.pictures[0].url)

        toast('message', 'New message', "sent you a message.", msg.user_data.pictures[0].url, msg.conv, msg.user_data.user.username);
        this.new_chats_notifs.push(msg); // this is just a current example to use in future | I should fix backend

      });
      socketStatus.emit('number_of_notifs', (number: number) => {
        this.notifs_counter = number
      })
      socketChat.emit('number_of_messages', (number: number) => {
        console.log(number)
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
          console.log(response)
          this.onlineUsers.set(id, response.status ? "Online" : response.status);
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
            this.onlineUsers.set(id, value);
          });
        }
      })
    },
    joinChat(id: any) {
      socketChat.emit('join_chat', { user_id: id }, ((resp: any) => {
        console.log(resp)
      }))
    },
    JoinUser(id: any) {
      socketChat.emit('join_video_chat', { user_id: id }, ((resp: any) => {
        console.log(resp)
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
        if (typeof(resp) == 'object' && resp.error) {
          toast('error', 'Send Message fail', resp.error);
        }
        id_message = resp as number
      }))
      return id_message || -1
    },
    UserStatus(id: string) {
      return this.onlineUsers.get(id)
    },
    disconnectAll(token: string) {
      if (!this.isBound) return;

      socketStatus.io.opts.extraHeaders = {
        Authorization: `Bearer ${token}`
      };
      if (socketStatus.connected) socketStatus.disconnect();

      socketChat.io.opts.extraHeaders = {
        Authorization: `Bearer ${token}`
      };
      if (socketChat.connected) socketChat.disconnect();

      socketChat.off();
      socketStatus.off();

      this.isBound = false;
    },
    interactWithUser(user_id: number, type: string) {
      const token = localStorage.getItem('auth_token');
      socketStatus.io.opts.extraHeaders = {
        Authorization: `Bearer ${token}`
      };
      console.log(
        socketStatus.emit(type, user_id)
      )
    },
    handleSocialEvent(type: string, payload: any) {
      const profileStore = useSocialStore();
      // const notifStore = useNotificationStore();
      // notifStore.addNotification(type + payload); // this is for later
      // notifStore.unreadCount++;


      switch (type) {
        case 'match':
          profileStore.handleNewMatch(payload.FromId);
          toast('like', 'New match', "matched your profile.", payload.avatar, payload.FromId, payload.username);
          break;
        case 'unmatch':
          profileStore.handleUnMatch(payload.FromId);
          toast('info', 'New unmatch', "unmatch your profile.", payload.avatar, payload.FromId, payload.username);

          break;
        case 'like':
          toast('info', 'New like', "liked your profile.", payload.avatar, payload.FromId, payload.username);

          if (profileStore.activeProfile?.user.user_id === payload.userId) {
            profileStore.fetchProfile(payload.userId);
          }
          break;

        case 'view':
          toast('view', 'Profile New', "viewed your profile.", payload.avatar, payload.FromId, payload.username);

          if (profileStore.activeProfile?.user.user_id === payload.userId && profileStore.activeProfile?.interactions.views_count) {
            profileStore.activeProfile.interactions.views_count++;
          }
          break;

        case 'block':
          profileStore.handleBlock(payload.userId);
          break;
      }
    }
  }
});
