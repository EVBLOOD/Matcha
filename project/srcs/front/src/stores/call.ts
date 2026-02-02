import { defineStore } from 'pinia';
import { useSocketStore } from '@/stores/socket';

interface ActivePeer {
    id: string;
    name: string;
    avatar: string;
}

export const useCallStore = defineStore('call', {
    state: () => ({
        isCalling: false,
        callState: 'dialing' as 'dialing' | 'ringing' | 'connected',
        activePeer: null as ActivePeer | null,
        pendingOffer: null as RTCSessionDescriptionInit | null,
        heartbeatInterval: null as number | null,
    }),
    actions: {
        initiateCall(id: string, name: string, avatar: string) {
            this.isCalling = false;

            this.activePeer = { id, name, avatar };
            this.isCalling = true;
            this.callState = 'dialing';
        },
        receiveIncoming(id: string, name: string, avatar: string, offer: RTCSessionDescriptionInit) {
            this.activePeer = { id, name, avatar };
            this.pendingOffer = offer;
            this.isCalling = false;
            this.isCalling = true;
            this.callState = 'ringing';
        },
        sendSignal(type: string, args: any) {
            const socketStore = useSocketStore();
            if (this.activePeer) {
                console.log(this.activePeer.id)
                console.log("type", type)
                console.log("args", args)
                socketStore.CallUser(this.activePeer.id, type, args);
            }
        },
        setConnected() {
            this.callState = 'connected';
            this.startHeartbeat();
        },
        reset() {
            this.stopHeartbeat();
            this.isCalling = false;
            this.callState = 'dialing';
            this.activePeer = null;
            this.pendingOffer = null;
        },
        startHeartbeat() {
            if (this.heartbeatInterval) return;

            this.heartbeatInterval = window.setInterval(() => {
                this.sendSignal('heartbeat_callers', {});
            }, 20000); 
        },

        stopHeartbeat() {
            if (this.heartbeatInterval) {
                clearInterval(this.heartbeatInterval);
                this.heartbeatInterval = null;
            }
        },
    }
});