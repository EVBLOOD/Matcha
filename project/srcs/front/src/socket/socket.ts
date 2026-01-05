import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.BACKEND_LINK || 'http://localhost:8081';

const token = localStorage.getItem('auth_token');

export const socketStatus: Socket = io(`${SOCKET_URL}/status`, {
  withCredentials: true,
  extraHeaders: {Authorization: `Bearer ${token}`},
  autoConnect: false,
});

export const socketChat: Socket = io(`${SOCKET_URL}/chat`, {
  withCredentials: true,
  extraHeaders: {Authorization: `Bearer ${token}`},
  autoConnect: false,
});
