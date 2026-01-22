import apiClient from '@/api/client';
import type { dateProposing } from '@/types/helpers';
import type { an } from 'vue-router/dist/router-CWoNjPRp.mjs';

export default {
  propose_date(userData: dateProposing) {
    return apiClient.post('/dates/propose', userData);
  },
  respond_to_date(status: string) {
    return apiClient.post('/respond/<int:date_id>', {"status": status});
  }, get_my_dates() {
    return apiClient.get('/dates/my-dates');
  }

};