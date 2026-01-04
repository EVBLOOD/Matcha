import apiClient from '@/api/client';
import type { UserRegister } from '@/types/user';

export default {
  getProfile(user_id: string | null) {
    if (user_id) return apiClient.get(`/profile/${user_id}`);
    return apiClient.get(`/profile/`);
  },
  likeProfile() {
    return [];
  }
};