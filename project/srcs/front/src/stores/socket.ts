import { defineStore } from 'pinia';
import { socketChat, socketStatus } from '@/socket/socket';

export const useSocketStore = defineStore('socket', {
  state: () => ({
    isConnected: false,
    onlineUsers: [] as string[],
    notifs: [] as string[],
  }),
  actions: {
    bindStatusEvents() {
      socketStatus.on('connect', () => { this.isConnected = true; });
      socketStatus.on('disconnect', () => { this.isConnected = false; });
    },
    bindChatEvents() {
      socketChat.on('connect', () => { this.isConnected = true; });
      socketChat.on('disconnect', () => { this.isConnected = false; });
    },
    connectAll() {
      if (!socketChat.connected) socketChat.connect();
      if (!socketStatus.connected) socketStatus.connect();

    //   this.bindStatusEvents();
    //   this.bindChatEvents();
    },
    disconnectAll() {
      if (socketChat.connected) socketChat.disconnect();
      if (socketStatus.connected) socketStatus.disconnect();
    }
  }
});
