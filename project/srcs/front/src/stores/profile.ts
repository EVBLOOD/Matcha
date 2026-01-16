
import { defineStore } from 'pinia';
import axios, { AxiosError } from 'axios';


import ProfileService from '@/api/services/ProfileService'
import type {UserProfileResponse} from '@/types/apiResponses'

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
    error : null as string | null
  }),

  actions: {
    async fetchProfile(id: number) {
      this.loading = true;
      const socket = useSocketStore();
      try {
        const { data } = await ProfileService.getProfile(id.toString());
        this.activeProfile = data;
        if (this.activeProfile?.user)
            socket.reachStausOneUser(this.activeProfile.user.user_id.toString())
      } catch(err : unknown) {
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

    handleNewMatch(partnerId: number) {
      if (this.activeProfile?.user.user_id === partnerId) {
        this.activeProfile.interactions.is_connected = 2
        this.isMatch = true;
      }
    },
    handleUnMatch(partnerId: number) {

      if (this.activeProfile?.user.user_id === partnerId) {
        this.activeProfile.interactions.is_connected = (this.activeProfile.interactions.is_connected || 1) - 1
        this.isMatch = true;
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