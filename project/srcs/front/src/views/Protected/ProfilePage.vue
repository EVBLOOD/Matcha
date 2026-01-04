<script setup lang="ts">
// import Button from '@/components/Button.vue';
// import { RouterLink, RouterView } from 'vue-router';
    import { RouterView } from 'vue-router';
import Fame from '@/components/Fame.vue';

</script>

<template>
    <div class="contentz">
        <div class="sideBar">
            <div>
                <img width="90%" style="margin-bottom: 22px;" src="/img/profilePictureDemo.png" alt="">
                <div style="font-weight:500; font-size: 26px;">Saad Akllam</div>
                <div class="status_bar">
                    <div class="status"></div> Online
                </div>
            </div>
            <div class="stats_holder">
                <div class="stats_count"> <img src="/img/viewIcon.svg" alt=""> Profile Views : <span
                        style="font-weight: bold;">324</span></div>
                <div class="stats_count"> <img src="/img/likesIcon.svg" alt=""> Likes Received : <span
                        style="font-weight: bold;">323</span></div>
            </div>
            <div>
                <p>Fame Rating 🔥</p>
                <Fame />
            </div>
        </div>
        <div class="profile_vue">
            <RouterView />
        </div>
    </div>
</template>

<style lang="scss" scoped>
// .fa {
//     font-size: 25px;
// }

// .partial {
//     background: linear-gradient(90deg, orange 90%, #FFFFFF 0%);
//     background-clip: text;
//     color: transparent;
// }

// .checked {
//     color: orange;
// }


.contentz {
    color: #FFFFFF;
    display: flex;
    align-items: center;

    height: 100%;
    width: 100%;
}

.sideBar {
    padding: 5%;
    height: 100%;
    gap: 10%;

    border-color: rgba(255, 255, 255, 0.25);
    ;
    display: flex;
    flex-direction: column;
    border-style: solid;
    border-width: 0px 1px 0px 0px;
}

.status_bar {
    display: flex;
    align-items: center;
    gap: 3%;
    font-weight: normal;
}

.status {
    height: 8px;
    width: 8px;
    border-radius: 50%;
    background-color: green;
}

.stats_count {
    display: flex;
    gap: 5px;
    align-items: center;
    flex-wrap: wrap;
}

.stats_holder {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.profile_vue {
    height: 100%;
    width: 100%;
    padding: 2%;
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;

        // margin: 0;
    }
}
</style>
