import { defineStore } from 'pinia';
import AuthService from '@/api/services/AuthService';
import axios, { AxiosError } from 'axios';

interface UserStore {
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
    isProfileComplete: (state) => state.user?.profile_status === 'completed'
  },
  actions: {
    async fetchUser() {
      try {
        const { data } = await AuthService.getProfileStatus();
        this.user = {
          verified_email: true,
          profile_status: 'completed'
        };
      } catch (error: unknown) {
        if (axios.isAxiosError(error)) {
          const errorMessage = (error.response?.data as BackendError)?.error;
          if (errorMessage === "profile completion required") {
            this.user = { verified_email: true, profile_status: 'not_completed' };
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
    }
  }
});

export default useUserStore;