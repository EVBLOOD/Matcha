<script setup lang="ts">
import Button from '@/components/Button.vue';
import SearchBarElem from '@/components/SearchBarElem.vue';
import UserExploreCard from '@/components/UserExploreCard.vue';

const handleSubmit = () => {
    console.log("SEARCH!")
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
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
            <UserExploreCard :userID="1"/>
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
    // padding-bottom: 0px;
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
    justify-content: center;
    flex-wrap: wrap;

    padding: 6px;

    gap: 10px;
    min-height: 83px;

    background-color: rgba(255, 255, 255, 0.06);

    border-radius: 12px;
    border-color: #BD82DD;
    border-style: solid;
    border-width: 1px;

    overflow: visible;
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
