import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.VITE_SOCKET_LINK;

export const socketStatus: Socket = io(`${SOCKET_URL}/status`, {
  path: '/api/socket.io',
  withCredentials: true,
  autoConnect: false,
});

export const socketChat: Socket = io(`${SOCKET_URL}/chat`, {
  path: '/api/socket.io',
  withCredentials: true,
  autoConnect: false,
});
