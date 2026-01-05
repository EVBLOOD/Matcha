import { defineStore } from 'pinia';
import { socketChat, socketStatus } from '@/socket/socket';

export const useSocketStore = defineStore('socket', {
  state: () => ({
    onlineUsers: new Map<string, string>(),
    notifs: [] as string[],
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
          const id: string = Object.keys(response)[0];
          const value: string = Object.values(response)[0] as string;
          this.onlineUsers.set(id, value);
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
    }
  }
});
