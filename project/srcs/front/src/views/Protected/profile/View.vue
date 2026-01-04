<script setup lang="ts">
    import { ref } from 'vue';
import RenderPictures from '@/components/RenderPictures.vue';
import TagsList from '@/components/TagsList.vue';
    import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';

    const insertedPictures = ref([{id: '1', url: '/img/profilePictureDemo.png'}, 
    {id: '2', url: '/img/profilePictureDemo.png'}, {id: '3', url: '/img/profilePictureDemo.png'}, {id: '4', url: '/img/profilePictureDemo.png'}])
    const availableTags = ['art', 'music', 'coding'];

</script>

<template>
    <div class="wraper">
        <div style="width: 100%;display: flex; justify-content: flex-end;height: 5%;">
            <RouterLink class="link" to=":id/settings"><img src="/img/editProfileIcon.svg" alt=""/> <span>Edit Profile</span></RouterLink>
        </div>
        <div class="user_infos">
            <RenderPictures :readonly="true" :initialpictures="insertedPictures"/>

            <div><img src="/img/maleIcon.svg" alt=""> Male</div>
            <div><img src="/img/locationIcon.svg" alt=""> California - USA</div>
            <div>
                Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.
            </div>
            <TagsList :readonly="true" :initialtags="availableTags"/>

        </div>
        <div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .wraper {
        display: flex;
        flex-direction: column;
        gap: 5%;
        height: 100%;
    }
.interest_span {
    padding: 3px;
    border-color: #9566B0;
    background: rgba(150, 104, 177, 1 - 0.24);
    border-style: solid;
    border-radius: 8px;
    padding: 0.5% 2% 0.5% 2%;
    flex-wrap: nowrap;
}
.interest_div_spans {
    display: flex;
    flex-wrap: wrap;
    gap: 2%;
}
    .user_infos {
        display: flex;
        flex-direction: column;
        gap: 2%;
        height: 100%;
    }
    .pictures_list {
        display: flex;
        gap: 4%;
        flex-wrap: wrap;
    }

    .image-box {
        width: 100px;
        height: 100px;
        border-radius: 8px;
        background-size: cover;
        background-position: center;
        position: relative;
    }

        .link {
        display: flex;
        gap: 10px;
        text-decoration: none;
        color: $text-color;
        justify-content: flex-end;
        align-items: center;
        // width: 20%;
        // height: 20px;
        padding:  1% 2% 1% 2%;
        cursor: pointer;
        background: rgba(255, 255, 255, 0.14);
        border-radius: 4px;
    }
    .link:hover {
        background: rgba(255, 255, 255, 0.12);

    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

