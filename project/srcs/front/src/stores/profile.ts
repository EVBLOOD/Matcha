
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
    isMatch: false,
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

    handleNewMatch(partnerId: number, conversation_id: number) {
      if (this.activeProfile?.user.user_id === partnerId) {
        this.activeProfile = {
          ...this.activeProfile,
          interactions: {
            ...this.activeProfile.interactions,
            is_connected: 2,
            conversation_id: conversation_id
          }
        };
        this.isMatch = true;
        console.log("Store updated with ID:", conversation_id);
      }
    },
    handleUnMatch(partnerId: number) {

      if (this.activeProfile?.user.user_id === partnerId) {
        this.activeProfile.interactions = {
          ...this.activeProfile.interactions,
          is_connected: (this.activeProfile.interactions.is_connected || 1) - 1
        };
      }
    },
    handleBlock(userId: number) {
      if (this.activeProfile?.user.user_id === userId) {

        this.activeProfile = null;
      }
    },

    clearActiveProfile() {
      this.activeProfile = null;
      this.isMatch = false;
    }
  }
});