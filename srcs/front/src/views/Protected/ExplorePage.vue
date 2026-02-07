<script setup lang="ts">
import Button from '@/components/Button.vue';
import SearchBarElem from '@/components/SearchBarElem.vue';
import UserExploreCard from '@/components/UserExploreCard.vue';
import InteractionMap from '@/components/InteractionMap.vue';

import { ref, onMounted } from 'vue';
import axios, { AxiosError } from 'axios';

import SuggestionsService from '@/api/services/SuggestionsService'
import type { SuggestionsResponse } from '@/types/apiResponses'
import { toast } from '@/composables/useToast';
import Loading from '@/components/Loading.vue';

const ExploreData = ref<SuggestionsResponse[] | null>(null);
const isLoading = ref(true);
const isError = ref<string | null>(null);

interface BackendError {
    error: string;
}
const tagsList = ref<string[]>([]);

import ProfileService from '@/api/services/ProfileService';
const fetchExplores = async () => {
    isLoading.value = true;
    try {
        {
            const { data } = await ProfileService.get_top_10_used_tags()
            tagsList.value = data.map((elem: any) => elem.name)

        }
        const { data } = await SuggestionsService.getExplore();
        ExploreData.value = data["data"];
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Registration failed for unknown reason'";
        }
    } finally {
        isLoading.value = false;
    }
};

onMounted(() => {
    fetchExplores()
})

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}


const currentType = ref<string>('List')

const query_base: any = {}

const Onclick = (type: string) => {
    currentType.value = type
}

const get_min_age = (value: any) => {
    query_base.age_min = value
}
const get_max_age = (value: any) => {
    query_base.age_max = value
}
const get_locations = (value: any) => {
    query_base.location = value
}

const get_fame = (value: any) => {
    query_base.fame_min = value
}
const get_tags = (value: any) => {
    query_base.tags = value
}


const reset_min_age = () => {
    delete query_base.age_min
}
const reset_max_age = () => {
    delete query_base.age_max
}
const reset_locations = () => {
    delete query_base.location
}

const reset_fame = () => {
    delete query_base.fame_min
}
const reset_tags = () => {
    delete query_base.tags
}

const handleSubmit = async () => {
    isLoading.value = true;
    try {
        if (selectedChoice.value != '') query_base.sort_by = selectedChoice.value
        else delete query_base.sort_by

        const query = new URLSearchParams(query_base as any).toString();
        const { data } = await SuggestionsService.getSearch(query);
        ExploreData.value = data["data"];
        
    } catch (err: unknown) {
        if (axios.isAxiosError(err)) {
            isError.value = (err.response?.data as BackendError)?.error;
        }
        else {
            isError.value = "Registration failed for unknown reason'";
        }
    } finally {
        isLoading.value = false;
    }
}
const selectedChoice = ref<string>('');

const sortHandeling = async (value: any) => {
    if (selectedChoice.value == '') {
        selectedChoice.value = value
        await handleSubmit()
        return
    }

    if (selectedChoice.value == value) selectedChoice.value = ''
    else selectedChoice.value = value
    await handleSubmit()

}

const openMenuName = ref(null);

const toggleMenu = (name: any) => {
    openMenuName.value = openMenuName.value === name ? null : name;
};

const currentSort = ref(null);

const toggleCurrentSort =  (name: any) => {
    currentSort.value = currentSort.value === name ? null : name;
};

</script>

<template>
    <div class="wraper">
        <div class="search_holder">
            <h2 style="margin-bottom: 2%;font-weight: normal;">Filters</h2>
            <div class="inner_search_bar">
                <SearchBarElem :sortOrNot="currentSort === 'Age'" @toggle_2="toggleCurrentSort('Age')" :isMenuOpen="openMenuName === 'Age'" @toggle_1="toggleMenu('Age')" @selected_choice="(value) => { sortHandeling(value) }" :firstElem="true" elemName="Age" @AgeMin-selected="get_min_age" @AgeMax-selected="get_max_age" @AgeMin-reset="reset_min_age" @AgeMax-reset="reset_max_age"/>
                <SearchBarElem :sortOrNot="currentSort === 'Location'" @toggle_2="toggleCurrentSort('Location')"  :isMenuOpen="openMenuName === 'Location'" @toggle_1="toggleMenu('Location')" @selected_choice="(value) => { sortHandeling(value) }" elemName="Location"
                    :locationList="['Tiznit', 'Agadir', 'Mirleft', 'Khouribga', 'Oujda', 'Casablaca']" @DisMax-selected="get_locations" @DisMax-reset="reset_locations"/>
                <SearchBarElem :sortOrNot="currentSort === 'Fame'" @toggle_2="toggleCurrentSort('Fame')"  :isMenuOpen="openMenuName === 'Fame'" @toggle_1="toggleMenu('Fame')" @selected_choice="(value) => { sortHandeling(value) }" elemName="Fame" @fame-selected="get_fame" @fame-reset="reset_fame" />
                <SearchBarElem :sortOrNot="currentSort === 'Tags'" @toggle_2="toggleCurrentSort('Tags')"  :isMenuOpen="openMenuName === 'Tags'" @toggle_1="toggleMenu('Tags')" @selected_choice="(value) => { sortHandeling(value) }" elemName="Tags" :tagsList="tagsList" @tags-selected="get_tags" @tags-reset="reset_tags"/>
                <Button class="btn" @click="handleSubmit" text="Search"></Button>
            </div>
        </div>
        <div style="display: flex; gap: 10px; justify-content: flex-end; margin: 5px; margin-bottom: 2%;">
            <Button text="List" @click="Onclick('List')" :img="'/img/listIcon.svg'"></Button>
            <Button text="Map" @click="Onclick('Map')" :img="'/img/mapIcon.svg'"></Button>
        </div>
        <Loading v-if="isLoading" />
        <div v-if="currentType == 'List' && !isLoading" class="body">
            <UserExploreCard v-for="value in ExploreData" :userID="value.user_id"
                :full-name="value.first_name + ' ' + value.last_name" :location="value.location" :age="value.age"
                :fame-score="value.fame_rating" :avatar="pictures_handler(value.profile_picture_url[0].url)" :isLiked="value.is_liked ? true : false"/>
        </div>
        <div v-if="currentType == 'Map' && !isLoading">
            <InteractionMap />
        </div>
    </div>
</template>


<style lang="scss" scoped>

.body {
    padding-bottom: 0px;

    display: flex;
    justify-content: center;
    width: 100%;
    gap: 2%;
    flex-wrap: wrap;
}

.wraper {
    padding: 3%;
    width: 100%;

}

.search_holder {
    position: relative;
    width: 100%;
    overflow: visible;
    margin-bottom: 2%;
}

.btn {
    width: 20%;
    margin-left: 3%;
}

.inner_search_bar {
    display: flex;
    align-items: center;
    justify-content: space-around;
    flex-wrap: wrap;

    padding: 6px;

    min-height: 83px;

    background-color: $components-background-color;

    border-radius: 12px;
    border-color: $border-color;
    border-style: solid;
    border-width: 1px;

    overflow: visible;
}

@media (max-width: $breakpoint-md) {
    .inner_search_bar {
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: center;
        width: 100%;
    }

    .btn {
        width: 100%;
        margin-left: 0%;
    }
}
</style>
