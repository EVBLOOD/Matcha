import { onMounted, onUnmounted } from 'vue';
import { socketStatus } from '@/socket/socket';

export function useSocketListener(event: string, callback: (data: any) => void) {
  onMounted(() => {
    socketStatus.on(event, callback);
  });

  onUnmounted(() => {
    socketStatus.off(event, callback);
  });
}