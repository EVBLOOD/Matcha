import { defineStore } from 'pinia';
import AuthService from '@/api/services/AuthService';
import axios, { AxiosError } from 'axios';

interface UserStore {
  id?: number;
  full_name?: string;
  profile_status: string;
  verified_email: boolean;
}

interface BackendError {
  error: string;
}

const useUserStore = defineStore('user', {
  state: (): { user: UserStore | null, isLoaded: boolean } => ({
    user: null,
    isLoaded: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
    isVerified: (state) => state.user?.verified_email,
    isProfileComplete: (state) => state.user?.profile_status === 'completed',
    getUserID: (state) => (state.user?.id || "unknown"),
    getUserName: (state) => (state.user?.full_name || "unknown")
  },
  actions: {
    async fetchUser() {
      try {
        const { data } = await AuthService.getProfileStatusHalfPub();
        console.log(data)
        this.user = {
          id: data.user_id,
          full_name: data.full_name,
          verified_email: true,
          profile_status: 'not_completed'
        };
        await AuthService.getProfileStatus();
        this.user.profile_status = "completed"

      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          const errorMessage = (error.response?.data as BackendError)?.error;
          if (errorMessage === "profile completion required") {
            if (this.user) this.user.profile_status = 'not_completed';
            else this.user = { verified_email: true, profile_status: 'not_completed' };
          } else if (errorMessage === "account isn't verified!") {
            this.user = { verified_email: false, profile_status: 'not_completed' };
          } else {
            this.user = null;
          }
        }
        else {
          this.user = null;
          console.error(error);
        }
      } finally {
        this.isLoaded = true;
      }
    },
    setIsLoaded(isLoaded: boolean) {
      this.isLoaded = isLoaded;
    },
    resetStore() {
      this.user = null
    }
  }
});

export default useUserStore;