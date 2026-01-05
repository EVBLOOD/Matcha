import { onMounted, onUnmounted } from 'vue';
import { socket } from '@/socket/socket';

export function useSocketListener(event: string, callback: (data: any) => void) {
  onMounted(() => {
    socket.on(event, callback);
  });

  onUnmounted(() => {
    socket.off(event, callback);
  });
}