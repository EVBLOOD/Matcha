import apiClient from '@/api/client';
import type { dateProposing } from '@/types/helpers';
import type { an } from 'vue-router/dist/router-CWoNjPRp.mjs';

export default {
  propose_date(userData: dateProposing) {
    return apiClient.post('/dates/propose', userData);
  },
  respond_to_date(event_id: number, status: string) {
    return apiClient.post(`/dates/respond/${event_id}`, {"status": status});
  }, get_my_dates() {
    return apiClient.get('/dates/my-dates');
  }

};