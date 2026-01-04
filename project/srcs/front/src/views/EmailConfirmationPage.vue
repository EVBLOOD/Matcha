<script setup lang="ts">
import Card from '@/components/Card.vue';
import Button from '@/components/Button.vue';


import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import useUserStore from '@/stores/user';

const router = useRouter();

onMounted(() => {
    const userStore = useUserStore();
    userStore.setIsLoaded(false)
    router.push('/profile-onboarding');
});

</script>


<template>
    <!-- <div class="page"> -->
        <Card title="An email has been sent to your address.">
            <Button class="btn" to="nothing" text="Resend Email"></Button>
            <div class="extra">Went to the wrong place? <Button class="just_btn" to="login" text="Back to Sign In"
                    backgroundColor="rgba(255, 255, 255, 0)"></Button></div>
        </Card>
    <!-- </div> -->
</template>

<style lang="scss" scoped>
// .page {
//     display: flex;
//     align-items: center;
//     justify-content: center;
//     height: 100vh;
// }

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
