
import { defineStore } from 'pinia';
import axios, { AxiosError } from 'axios';


import ProfileService from '@/api/services/ProfileService'
import type { UserProfileResponse } from '@/types/apiResponses'

// this will cause problems if I keep it 
import { useSocketStore } from '@/stores/socket';


interface BackendError {
  error: string;
}



export const useSocialStore = defineStore('profile', {
  state: () => ({
    activeProfile: null as UserProfileResponse | null,
    loading: false,
    error: null as string | null
  }),
  getters: {
    getConversationId: (state) => state.activeProfile?.interactions?.conversation_id,
    getConnectionStatus: (state) => state.activeProfile?.interactions?.is_connected || 0
  },
  actions: {
    async fetchProfile(id: number) {
      this.loading = true;
      this.error = ""
      const socket = useSocketStore();
      try {
        const { data } = await ProfileService.getProfile(id.toString());
        this.activeProfile = data;
        if (this.activeProfile?.user) {
          socket.reachStausOneUser(this.activeProfile.user.user_id.toString())
        }
      } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          this.error = (err.response?.data as BackendError)?.error;
        }
        else {
          this.error = "Registration failed for unknown reason'";
        }
      } finally {
        this.loading = false;
      }
    },
    handleNewMatch(partnerId: number, secondId: number, conversation_id: number) {

      if (this.activeProfile?.user.user_id == partnerId) {
        this.activeProfile.interactions.is_connected = 2
        this.activeProfile.interactions.interaction_status = 'liked'

      } else if (this.activeProfile?.user.user_id == secondId) {

        this.activeProfile.interactions.is_connected = 2

        this.activeProfile.interactions.interaction_status = 'liked'
        this.activeProfile.interactions.likes_count++

      }
    },
    handleDislike(partnerId: number, secondId: number, conversation_id: number) {

      if (this.activeProfile?.user.user_id == partnerId) {

        if (this.activeProfile.interactions.is_connected) this.activeProfile.interactions.is_connected--
        else this.activeProfile.interactions.is_connected = 0
        
      }  else if (this.activeProfile?.user.user_id == secondId) {

        if (this.activeProfile.interactions.is_connected) this.activeProfile.interactions.is_connected--
        else this.activeProfile.interactions.is_connected = 0
        this.activeProfile.interactions.likes_count--

        this.activeProfile.interactions.interaction_status = undefined
      }
    },
    handleLike(partnerId: number, secondId: number, conversation_id: number) {

      if (this.activeProfile?.user.user_id == partnerId) {
        if (this.activeProfile.interactions.is_connected) this.activeProfile.interactions.is_connected++
        else this.activeProfile.interactions.is_connected = 1

      } else if (this.activeProfile?.user.user_id == secondId) {

        if (this.activeProfile.interactions.is_connected) this.activeProfile.interactions.is_connected++
        else this.activeProfile.interactions.is_connected = 1

        this.activeProfile.interactions.interaction_status = 'liked'
        this.activeProfile.interactions.likes_count++

      }
    },
    handleUnMatch(partnerId: number, secondId: number) {


      if (this.activeProfile?.user.user_id == partnerId) {

        if (this.activeProfile.interactions.is_connected) this.activeProfile.interactions.is_connected--
        else this.activeProfile.interactions.is_connected = 0
        
      }  else if (this.activeProfile?.user.user_id == secondId) {

        if (this.activeProfile.interactions.is_connected) this.activeProfile.interactions.is_connected--
        else this.activeProfile.interactions.is_connected = 0
        this.activeProfile.interactions.likes_count--

        this.activeProfile.interactions.interaction_status = undefined
      }
    },
    handleBlock(userId: number, secondId: number) {

      if (this.activeProfile?.user.user_id == userId || this.activeProfile?.user.user_id == secondId) {

        this.activeProfile = null;
      }
    },

    clearActiveProfile() {
      this.activeProfile = null;
    }
  }
});