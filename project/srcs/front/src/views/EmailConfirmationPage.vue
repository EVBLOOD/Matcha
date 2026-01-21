<script setup lang="ts">
import Card from '@/components/Card.vue';
import Button from '@/components/Button.vue';


import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';
import AuthService from '@/api/services/AuthService';
import axios, { AxiosError } from 'axios';
import { toast } from '@/composables/useToast';

interface ValidationErrors {
  [key: string]: string[];
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
        
        toast('success', 'Resend email success', "Check your email please");
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            error.value = err.response?.data?.errors || err.response?.data?.error || 'Resend email failed for unknown reason';
        } else {
            error.value = 'Resend email failed for unknown reason'
        }
         if (Array.isArray(error.value)) {
      error.value.map((err) => {
        toast('error', 'Resend email failed', err as string);
      })
    } else if (typeof (error.value) === 'string') {
      toast('error', 'Resend email failed', error.value);
    } else if (error.value && typeof (error.value) === 'object') {
      const errorData = error.value as ValidationErrors
      Object.entries(errorData).map(([field, messages]) => {
        messages.map((msg) => {
          toast('error', 'Resend email failed', msg);
        })
        return messages.map(msg => msg.toUpperCase());
      });
    }
    } finally {
        isLoading.value = false;
    }
};

const userStore = useUserStore();


const clickLogOut = async () => {
    try {
        const response = await AuthService.logout();
        console.log(response)
        userStore.fetchUser()
        localStorage.removeItem('auth_token');

        userStore.setIsLoaded(false)

        router.push('login')
    } catch (err) {
        console.log(err);
        localStorage.removeItem('auth_token');
    }
}

</script>


<template>
    <div v-on:click="clickLogOut" style="position: absolute; bottom: 10%; left: 5%;">
        <a class="link log_a"><img src="/img/logOut.svg" alt="" /> <span>Log
                out</span></a>
    </div>
    <Card title="An email has been sent to your address.">
        <Button class="btn" @click="handleResendMail" text="Resend Email"></Button>
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

.link {
    display: flex;
    gap: 10px;
    text-decoration: none;
    color: $text-color;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    // height: 6%;
    padding: 6%;
    align-content: center;
    cursor: pointer;
    flex-wrap: wrap;
}

.link:hover {
    background: $components-hover-color;
    border-radius: 8px;

}


@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
