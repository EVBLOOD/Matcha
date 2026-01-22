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

const ExploreData = ref<SuggestionsResponse[] | null>(null);
const isLoading = ref(true);
const isError = ref<string | null>(null);

interface BackendError {
    error: string;
}


const fetchExplores = async () => {
    isLoading.value = true;
    try {
        const { data } = await SuggestionsService.getExplore();
        console.log(data)
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
    console.log(value)
    query_base.age_min = value
}
const get_max_age = (value: any) => {
    console.log(value)
    query_base.age_max = value
}
const get_locations = (value: any) => {
    console.log(value)
    query_base.location = value
}

const get_fame = (value: any) => {
    console.log(value)
    query_base.fame_min = value
}
const get_tags = (value: any) => {
    console.log(value)
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
    console.log("LOL")
    delete query_base.fame_min
}
const reset_tags = () => {
    delete query_base.tags
}

// const PageData = ref<any | null>(null);

const handleSubmit = async () => {
    isLoading.value = true;
    try {
        if (selectedChoice.value != '') query_base.sort = selectedChoice.value
        else delete query_base.sort

        const query = new URLSearchParams(query_base as any).toString();
        const { data } = await SuggestionsService.getSearch(query);
        console.log(data)
        console.log(data["data"])
        ExploreData.value = data["data"];
        
        // PageData.value = data["data"]['page'];
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
const selectedChoice = ref<string | null>(null);

const sortHandeling = (value: any) => {
    console.log(value)
    if (!selectedChoice.value) {
        selectedChoice.value = value
        return
    }

    if (selectedChoice.value == value) selectedChoice.value = ''
    else selectedChoice.value = value
}

const openMenuName = ref(null);

const toggleMenu = (name: any) => {
    openMenuName.value = openMenuName.value === name ? null : name;
};

const currentSort = ref(null);

const toggleCurrentSort = (name: any) => {
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
                <SearchBarElem :sortOrNot="currentSort === 'Tags'" @toggle_2="toggleCurrentSort('Tags')"  :isMenuOpen="openMenuName === 'Tags'" @toggle_1="toggleMenu('Tags')" @selected_choice="(value) => { sortHandeling(value) }" elemName="Tags" :tagsList="['Sport', 'Coding', 'Cars', 'Sience', 'IT', 'Art']" @tags-selected="get_tags" @tags-reset="reset_tags"/>
                <Button class="btn" @click="handleSubmit" text="Search"></Button>
            </div>
        </div>
        <div style="display: flex; gap: 10px; justify-content: flex-end; margin: 5px; margin-bottom: 2%;">
            <Button text="List" @click="Onclick('List')" :img="'/img/listIcon.svg'"></Button>
            <Button text="Map" @click="Onclick('Map')" :img="'/img/mapIcon.svg'"></Button>
        </div>
        <div v-if="currentType == 'List'" class="body">
            <UserExploreCard v-for="value in ExploreData" :userID="value.user_id"
                :full-name="value.first_name + ' ' + value.last_name" :location="value.location" :age="value.age"
                :fame-score="value.fame_rating" :avatar="pictures_handler(value.profile_picture_url[0].url)" />
        </div>
        <div v-if="currentType == 'Map'">
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

    // gap: 10px;
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
