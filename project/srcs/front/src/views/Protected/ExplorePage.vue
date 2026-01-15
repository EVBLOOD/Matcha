<script setup lang="ts">
import Button from '@/components/Button.vue';
import SearchBarElem from '@/components/SearchBarElem.vue';
import UserExploreCard from '@/components/UserExploreCard.vue';

const handleSubmit = () => {
    console.log("SEARCH!")
}

import SuggestionsService from '@/api/services/SuggestionsService'
import type { SuggestionsResponse } from '@/types/apiResponses'
import axios, { AxiosError } from 'axios';
import { ref, onMounted } from 'vue';

const suggestionsData = ref<SuggestionsResponse[] | null>(null);
const isLoading = ref(true);
const isError = ref<string | null>(null);

interface BackendError {
  error: string;
}


const fetchSugestions = async () => {
  isLoading.value = true;
  try {
    const { data } = await SuggestionsService.getSuggestions();
    console.log(data)
    suggestionsData.value = data["data"];
  } catch(err : unknown) {
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
    fetchSugestions()
})

const pictures_handler = (link: string) => {
    if (link.indexOf('/') > 0) {
        return link
    }
    return `${import.meta.env.VITE_BACKEND_LINK}/profile/pictures/${link}`
}
</script>

<template>
    <div class="wraper">
        <div class="search_holder">
            <h2 style="margin-bottom: 2%;font-weight: normal;">
                Filters
            </h2>
            <div class="inner_search_bar">
                <SearchBarElem :firstElem="true" elemName="Age" />
                <SearchBarElem elemName="Location" 
                    :locationList="['Tiznit', 'Agadir', 'Mirleft', 'Khouribga','Oujda', 'Casablaca']" />
                <SearchBarElem elemName="Fame" />
                <SearchBarElem elemName="Tags" 
                    :tagsList="['Sport', 'Coding', 'Cars', 'Sience','IT', 'Art']" />
                <Button class="btn" @click="handleSubmit" text="Search"></Button>
            </div>
        </div>
        <div class="body">
            <UserExploreCard v-for="value in suggestionsData" :userID="value.user_id" :full-name="value.first_name + ' ' + value.last_name" :location="value.location" :age="value.age" :fame-score="value.fame_rating" :avatar="pictures_handler(value.profile_picture_url[0].url)"/>
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
