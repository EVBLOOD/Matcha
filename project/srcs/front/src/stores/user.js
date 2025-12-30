import { defineStore } from 'pinia';
import AuthService from '@/api/services/AuthService';

const useUserStore = defineStore('user', {
  state: () => ({
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
        const { data } = await AuthService.getProfile();
        this.user = {
          verified_email: true,
          profile_status: 'completed'
        };
      } catch (error) {
        console.log(error)
        if (error?.response?.data?.error == "profile completion required") {          
          this.user = {
            verified_email: true,
            profile_status:  'not_completed'
          };
        } else if (error?.response?.data?.error == "account isn't verified!") {
          this.user = {
            verified_email: false,
            profile_status:  'not_completed'
          };
        } else {
          this.user = null;
        }
      } finally {
        this.isLoaded = true;
      }
    },
    setIsLoaded(isLoaded) {
      this.isLoaded = isLoaded;
    }
  }
});

export default useUserStore;