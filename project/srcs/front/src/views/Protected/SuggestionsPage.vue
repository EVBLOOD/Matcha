<script setup lang="ts">
import Button from '@/components/Button.vue';
import SuggestionsbarElem from '@/components/SuggestionsbarElem.vue';
import UserExploreCard from '@/components/UserExploreCard.vue';

const handleSubmit = () => {
    console.log("SEARCH!")
}

import SuggestionsService from '@/api/services/SuggestionsService'
import type { SuggestionsResponse } from '@/types/apiResponses'
import axios, { AxiosError } from 'axios';
import { ref, onMounted, watch } from 'vue';

const suggestionsData = ref<SuggestionsResponse[] | null>(null);
const isLoading = ref(true);
const isError = ref<string | null>(null);
const selectedChoice = ref<string | null>(null);
// const selectedChoice = ref<string | null>(null);
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

const currentType = ref<string | null>(null);

const Onclick = (type: string) => {
    if (type === currentType.value) {
        currentType.value = null
        return
    }
    currentType.value = type
}

watch(selectedChoice, () => {
    console.log(selectedChoice.value)
})
</script>

<template>
    <div class="wraper">
        <div class="search_holder">
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin: 5px;">
                <Button text="Sort" @click="Onclick('Sort')" :img="'/img/filterIcon.svg'"></Button>
                <Button text="Filter" @click="Onclick('Filter')" :img="'/img/sortIcon.svg'"></Button>
            </div>
            <div v-if="currentType" class="inner_search_bar">
                <SuggestionsbarElem :firstElem="true" elemName="Age" :inputType="currentType == 'Sort' ? 'Filter' : 'radio'" @selected_choice="(value) => {selectedChoice = value}"/>
                <SuggestionsbarElem elemName="Location" 
                    :inputType="currentType == 'Sort' ? 'Filter' : 'radio'" @selected_choice="(value) => {selectedChoice = value}"/>
                <SuggestionsbarElem elemName="Fame" :inputType="currentType == 'Sort' ? 'Filter' : 'radio'" @selected_choice="(value) => {selectedChoice = value}"/>
                <SuggestionsbarElem elemName="Tags" 
                    :inputType="currentType == 'Sort' ? 'Filter' : 'radio'" @selected_choice="(value) => {selectedChoice = value}"/>
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
    justify-content: space-between;
    flex-wrap: wrap;

    padding: 20px 35px 20px 35px;

    gap: 2%;
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
