import apiClient from '@/api/client';
import type { Login, RecoverPassword, RecoverPasswordIn } from '@/types/auth';
export default {
  login(userData: Login) {
    return apiClient.post('/auth/login', userData);
  },
  logout() {
    return apiClient.post('/auth/logout');
  },
  getProfileStatus() {
    return apiClient.get('/user/protected')
  },
  getProfileStatusHalfPub() {
    return apiClient.get('/user/not_protected')
  },
  rest_password(input: RecoverPassword) {
    return apiClient.post('/auth/forgot_pass', {"user_input": input.email})
  },
  rest_new_password(payload: RecoverPasswordIn) {
    return apiClient.post('/auth/confirm-reset', payload)
  },
  resend_verfiy_mail() {
    return apiClient.post('/user/verify_account_retry')
  }
};