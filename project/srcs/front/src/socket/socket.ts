import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.SOCKET_LINK || 'http://localhost:8081';


export const socketStatus: Socket = io(`${SOCKET_URL}/status`, {
  withCredentials: true,
  autoConnect: false,
});

export const socketChat: Socket = io(`${SOCKET_URL}/chat`, {
  withCredentials: true,
  autoConnect: false,
});
