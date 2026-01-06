import { defineStore } from 'pinia';
import { socketChat, socketStatus } from '@/socket/socket';
import { ref } from 'vue';

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

        socketStatus.on('notify', (msg: string) => {
          console.log(msg)
         this.notifications.push(msg); // this is just a current example to use in future | I should fix backend
        });

        socketChat.on('recieved_message', (msg: string) => {
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
      socketStatus.emit(type, user_id)
    }
  }
});
