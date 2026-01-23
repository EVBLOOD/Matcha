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

const fetchSugestions = async (params: any = undefined) => {
    isLoading.value = true;
    try {
        const { data } = await SuggestionsService.getSuggestions(params);
        console.log(data)
        suggestionsData.value = data["data"];
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
const selected_order = ref('')
const selected_filter = ref('')
const search_query = ref('')
watch(selectedChoice, async (newValue) => {
    if (newValue && newValue?.includes('radioby')) {
        if (newValue.replace('radioby', '') == selected_order.value) {
            selected_order.value = ''
        } else {
            selected_order.value = newValue.replace('radioby', '')
        }
    }

    if (newValue && newValue?.includes('Filterby')) {
        console.log("HELLO")
        if (newValue.replace('Filterby', '') == selected_filter.value) {
            selected_filter.value = ''
        } else {
            selected_filter.value = newValue.replace('Filterby', '')
        }
    }
    const params = new URLSearchParams();
    
    if (selected_order.value) {
        params.append('sort', selected_order.value.toLowerCase());
    }
    if (selected_filter.value) {
        params.append('filter', selected_filter.value.toLowerCase());
    }
    console.log(params.toString())
    await fetchSugestions(params.toString());
})

import Loading from '@/components/Loading.vue';

</script>

<template>

    <div class="wraper">
        <div class="search_holder">
            <div style="display: flex; gap: 10px; justify-content: flex-end; margin: 5px;">
                <Button text="Sort" @click="Onclick('Sort')" :img="'/img/filterIcon.svg'"></Button>
                <Button text="Filter" @click="Onclick('Filter')" :img="'/img/sortIcon.svg'"></Button>
            </div>
            <div v-if="currentType" class="inner_search_bar">
                <SuggestionsbarElem :firstElem="true" elemName="Age"
                    :inputType="currentType == 'Sort' ? 'Filter' : 'radio'"
                    @selected_choice="(value) => { selectedChoice = value }" />
                <SuggestionsbarElem elemName="Location" :inputType="currentType == 'Sort' ? 'Filter' : 'radio'"
                    @selected_choice="(value) => { selectedChoice = value }" />
                <SuggestionsbarElem elemName="Fame" :inputType="currentType == 'Sort' ? 'Filter' : 'radio'"
                    @selected_choice="(value) => { selectedChoice = value }" />
                <SuggestionsbarElem elemName="Tags" :inputType="currentType == 'Sort' ? 'Filter' : 'radio'"
                    @selected_choice="(value) => { selectedChoice = value }" />
                <Button class="btn" @click="handleSubmit" text="Search"></Button>
            </div>
        </div>
        <Loading v-if="isLoading" @finished="isLoading = false" />

        <div v-if="!isLoading" class="body">
            <UserExploreCard v-for="value in suggestionsData" :userID="value.user_id"
                :full-name="value.first_name + ' ' + value.last_name" :location="value.location" :age="value.age"
                :fame-score="value.fame_rating" :avatar="pictures_handler(value.profile_picture_url[0].url)" />
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
