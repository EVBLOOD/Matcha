<script setup>
// import Button from '@/components/Button.vue';
// import { RouterLink, RouterView } from 'vue-router';
    import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';

</script>

<template>
    <div class="content">
        <div class="sideBar">
            Chat Bar List
                <RouterLink class="link" to="/messages/:id"><img src="/img/homeIcon.svg" alt=""/> <span>Home</span></RouterLink>
        </div>
        <div class="profile_vue">
            <RouterView />
        </div>
    </div>
</template>

<style lang="scss" scoped>
.fa {
    font-size: 25px;
}

.partial {
    background: linear-gradient(90deg, orange 90%, #FFFFFF 0%);
    background-clip: text;
    color: transparent;
}

.checked {
    color: orange;
}


.content {
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
