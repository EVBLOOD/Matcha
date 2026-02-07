import { onMounted, onUnmounted } from 'vue';
import { socketChat } from '@/socket/socket';

export function useSocketListener(event: string, callback: (data: any) => void) {
  onMounted(() => {
    socketChat.on(event, callback);
  });

  onUnmounted(() => {
    socketChat.off(event, callback);
  });
}