import { defineStore } from 'pinia';
import AuthService from '@/api/services/AuthService';

const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isLoaded: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.user,
    isProfileComplete: (state) => state.user?.profile_status === 'completed'
  },
  actions: {
    async fetchUser() {
      try {
        const { data } = await AuthService.getProfile();
        state.user.profile_status = 'completed';
      } catch (error) {
        console.log(error)
        if (error?.response?.data?.error == "profile completion required") {          
          this.user = {profile_status:  'not_completed'}
        } else {
          this.user = null;
        }
      } finally {
        this.isLoaded = true;
      }
    }
  }
});

export default useUserStore;