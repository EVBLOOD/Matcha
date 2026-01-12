import { defineStore } from 'pinia';
import { socketChat, socketStatus } from '@/socket/socket';
import { ref } from 'vue';
import { useSocialStore } from '@/stores/profile';


export const useSocketStore = defineStore('socket', {
  state: () => ({
    onlineUsers: new Map<string, string>(),
    notifications: ref<string[]>([]),
    new_chats_notifs: ref<string[]>([]),
    isBound: false,
  }),
  actions: {
    bindStatusEvents() {
      if (this.isBound) return;
      socketStatus.on('connected', (response) => {
        console.log(response);
        const id: string = Object.keys(response)[0];
        const value: string = Object.values(response)[0] as string;
        this.onlineUsers.set(id, value);
      });

        socketStatus.on('notify', (msg) => {
          // console.log(msg)
          this.handleSocialEvent(msg.type, {"userId": msg.dst_id, "conversation_id": msg.conversation_id, "FromId": msg.source_id});
         this.notifications.push(msg); // waiting for desing to add it in front as pop up
        });

        socketChat.on('recieved_message', (msg: string) => {
          console.log(msg)
         this.new_chats_notifs.push(msg); // this is just a current example to use in future | I should fix backend
        });
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
          this.onlineUsers.set(id, response.status ? "Online" : "Offline"); // TODO: update Offline to last view time.
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
    joinChat(id: string) {
      socketChat.emit('join_chat', {user_id: id}, ((resp: any) => {
        console.log(resp)
      }))
    },
    leaveChat(id: string) {
      socketChat.emit('join_chat', {user_id: id}, ((resp: any) => {
        console.log(resp)
      }))
    },
    sendMessage(id: string, content: string) : number {
      let id_message = undefined
      socketChat.emit('send_message', {user_id: id, text: content}, ((resp: any) => {
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
          break;
        case 'unmatch':
          profileStore.handleUnMatch(payload.FromId);
          break;
        case 'like':
          if (profileStore.activeProfile?.user.user_id === payload.userId) {
            profileStore.fetchProfile(payload.userId);
          }
          break;

        case 'view':
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
