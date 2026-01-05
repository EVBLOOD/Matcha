import { defineStore } from 'pinia';
import { socket } from '@/socket/socket';

export const useSocketStore = defineStore('socket', {
  state: () => ({
    isConnected: false,
    onlineUsers: [] as string[],
    notifs: [] as string[],
  }),
  actions: {
    bindEvents() {
      socket.on('connect', () => { this.isConnected = true; });
      socket.on('disconnect', () => { this.isConnected = false; });
      socket.on('online', (users) => { this.onlineUsers = users; });
      socket.on('notifs', (notif) => { this.notifs = [notif, ...this.notifs]; });
    },
    connect() {
      if (!socket.connected) socket.connect();
    },
    disconnect() {
      if (socket.connected) socket.disconnect();
    }
  }
});