<script setup lang="ts">
import Card from '@/components/Card.vue';
import Button from '@/components/Button.vue';


import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';
import AuthService from '@/api/services/AuthService';
import axios, { AxiosError } from 'axios';

interface BackendError {
  error?: string;
  errors?: any[];
}

const router = useRouter();

onMounted(() => {
    const userStore = useUserStore();
    userStore.setIsLoaded(false)
    router.push('/profile-onboarding');
});



const isLoading = ref(false);
const error = ref<null | string | any[]>(null);

const handleResendMail = async () => {
  isLoading.value = true;
  error.value = null;

  try {
       const response = await AuthService.resend_verfiy_mail();
       console.log(response)
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
          error.value = (err.response?.data as BackendError).errors || (err.response?.data as BackendError).error || 'Resend email failed for unknown reason';
        } else {
            error.value = 'Resend email failed for unknown reason'
        }
     } finally {
       isLoading.value = false;
     }
};


</script>


<template>
        <Card title="An email has been sent to your address.">
            <Button class="btn" @click="handleResendMail"  text="Resend Email"></Button>
            <div class="extra">Went to the wrong place? <Button class="just_btn" to="login" text="Back to Sign In"
                    backgroundColor="rgba(255, 255, 255, 0)"></Button></div>
        </Card>
</template>

<style lang="scss" scoped>

.btn {
    margin-bottom: 5%;
}

.extra {
    display: flex;
    justify-content: center;
    align-content: center;
    width: 100%;
    gap: 5px;
}

.just_btn {
    margin-top: 0%;
    padding: 0px;
    border-style: none;
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
