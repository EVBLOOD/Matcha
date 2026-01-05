import { io, Socket } from 'socket.io-client';

const SOCKET_URL = import.meta.env.BACKEND_LINK || 'http://localhost:8081';

export const socket: Socket = io(SOCKET_URL, {
  withCredentials: true,
});