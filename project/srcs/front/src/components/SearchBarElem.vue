<script setup lang="ts">
import { ref, computed } from 'vue';
import Fame from '@/components/Fame.vue';

const props = defineProps({
    firstElem: {
        type: Boolean,
        default: false
    },
    elemName: String, // Age | Location | Fame | Tags
    tagsList: Array<String>,
    locationList: Array<String>,
    fame: Array
});

const emit = defineEmits(['AgeMin-selected', 'AgeMax-selected', 'location-selected', 'fame-selected', 'tags-selected']);

const isMenuOpen = ref(false)


// if (props.elemName === 'Age') 
const AgeMin = ref(18)
const AgeMax = ref(24)

const add_age = (type: string) => {
    if (type === 'AgeMin-selected') {
        if (AgeMin.value < AgeMax.value) AgeMin.value++;
        emit('AgeMin-selected', AgeMin.value);
    } else {
        AgeMax.value++;
        emit('AgeMax-selected', AgeMax.value);
    }
};

const minus_age = (type: string) => {
    if (type === 'AgeMin-selected') {
        if (AgeMin.value > 18) AgeMin.value--;
        emit('AgeMin-selected', AgeMin.value);
    } else {
        if (AgeMax.value > AgeMin.value) AgeMax.value--;
        emit('AgeMax-selected', AgeMax.value);
    }
};

// else if (props.elemName === 'Location') 
const selectedLocation = ref<Array<string>>([])

const selection_location = (city: string) => {
    const index = selectedLocation.value.indexOf(city);
    if (index > -1) {
        selectedLocation.value.splice(index, 1);
    } else {
        selectedLocation.value.push(city);
    }
    emit('location-selected', selectedLocation.value);
};

// else if (props.elemName === 'Fame') 
const selectedFame = ref<number>(4.0)

const add_fame = () => {
    if (selectedFame.value < 5) {
        selectedFame.value = parseFloat((selectedFame.value + 0.1).toFixed(1));
        // selectedFame.value = selectedFame.value + 0.1;
        emit('fame-selected', selectedFame.value);
    }
};

const minus_fame = () => {
    if (selectedFame.value > 0) {
        // selectedFame.value = selectedFame.value - 0.1;
        selectedFame.value = parseFloat((selectedFame.value - 0.1).toFixed(1));
        emit('fame-selected', selectedFame.value);
    }
};

//  else if (props.elemName === 'Tags') 
const selectedIntersts = ref<Array<string>>([]);

const tagClick = (tag: string) => {
    const index = selectedIntersts.value.indexOf(tag);
    if (index > -1) {
        selectedIntersts.value.splice(index, 1);
    } else {
        selectedIntersts.value.push(tag);
    }
    emit('tags-selected', selectedIntersts.value);
};


const listClick = (lt: String, elemName: string) => {
    if (elemName == "Tags") {
        tagClick(lt as string);
    } else {
        selection_location(lt as string);
    }
}


const valueDisplay = computed(
    () => {
        if (props.elemName === 'Age') {
            return `${AgeMin.value} - ${AgeMax.value}`
        } else if (props.elemName === 'Location') {

            if (selectedLocation.value.length >= 3) {
                return [`${selectedLocation.value[0]},`, `${selectedLocation.value[1]}...`]
            } else if (selectedLocation.value.length >= 2) {
                return [`${selectedLocation.value[0]},`, selectedLocation.value[1]]
            } else if (selectedLocation.value.length == 1) {
                return [selectedLocation.value[0]]
            }
            return ["-"]

        } else if (props.elemName === 'Fame') {
            return selectedFame.value.toFixed(1);
        } else if (props.elemName === 'Tags') {

            if (selectedIntersts.value.length >= 3) {
                return [`#${selectedIntersts.value[0]},`, `#${selectedIntersts.value[1]}...`]
            } else if (selectedIntersts.value.length >= 2) {
                return [`#${selectedIntersts.value[0]},`, `#${selectedIntersts.value[1]}`]
            } else if (selectedIntersts.value.length == 1) {
                return [`#${selectedIntersts.value[0]}`]
            }
            return ["-"]

        } else {
            return null
        }
    }
);

const handleClick = () => { 
    isMenuOpen.value = !isMenuOpen.value;
};

const checkListExists = (lt: String, elemName: string) => {
    if (elemName == "Tags") {
        return selectedIntersts.value.includes(lt as string)
    }
    return selectedLocation.value.includes(lt as string)
}
</script>

<template>

    <div class="div_breaker">
        <div v-if="!firstElem" class="break_line"></div>
        <div class="search_type">
            <div class="label_input">
                <h3>{{ elemName || "evblood" }}</h3>
                <input type="image" src="/img/arrowDownIcon.svg" @click="handleClick()" />
            </div>
            <div v-if="elemName !== 'Tags' && elemName !== 'Location' && elemName !== 'Fame'">{{ valueDisplay }}</div>
            <div v-if="elemName === 'Tags' || elemName === 'Location'" style="display: flex; gap: 2px;">
                <span v-for="val in valueDisplay">{{ elemName === 'Tags' ? `${val}` : val }}</span>
            </div>
            <Fame v-if="elemName === 'Fame'" :initialFameScore="selectedFame"/>
        </div>



        <div v-if="elemName === 'Age'" class="search_menu_age" v-show="isMenuOpen">
            <div>
                <input @click="minus_age('AgeMin-selected')" type="image" src="/img/lessIcon.svg"> {{ AgeMin }}
                <input @click="add_age('AgeMin-selected')" type="image" src="/img/plusIcon.svg">
            </div>
            to
            <div>
                <input @click="minus_age('AgeMax-selected')" type="image" src="/img/lessIcon.svg"> {{ AgeMax }}
                <input @click="add_age('AgeMax-selected')" type="image" src="/img/plusIcon.svg">
            </div>
        </div>

        <div  v-if="elemName === 'Fame'" class="search_menu_fame"  v-show="isMenuOpen">
            <div>
                <input @click="minus_fame()" type="image" src="/img/lessIcon.svg"> {{ selectedFame }} <input
                    @click="add_fame()" type="image" src="/img/plusIcon.svg">
            </div>
        </div>

        <div  v-show="isMenuOpen"  v-if="elemName === 'Location' || elemName === 'Tags'" class="search_menu_location" style="flex-direction: column;">
            <div @click="listClick(lt, elemName)" v-for="lt in (locationList || tagsList)" :class="{ active: checkListExists(lt, elemName)}">
                {{ lt }}
            </div>
        </div>

    </div>

</template>

<style lang="scss" scoped>
.div_breaker {
    position: relative;
    display: flex;
    overflow: visible;
    gap: 20px;
    height: 100%;
    justify-content: center;
    align-items: center;
}

.search_type {
    display: flex;
    flex-direction: column;

}

.label_input {
    display: flex;
    gap: 60px;
    justify-content: space-between;
}

.break_line {
    height: 30px;
    border-style: solid;
    border-width: 0px 0px 0px 2px;
    border-radius: 10%;
    border-color: $border-color;
}


.search_menu_age {
    position: absolute;
    background-color: $primary-color;
    top: calc(100% + 4px);
    left: 0;
    display: flex;
    justify-content: center;
    gap: 10%;
    align-items: center;
    width: 300px;
    height: 80px;
    border-radius: 8px;
    padding: 3%;
    color: $menu-text-color;
    font-weight: bolder;
    z-index: 1;

    div {
        display: flex;
        justify-content: center;
        align-content: center;
        gap: 5px;
    }
}

.search_menu_location {
    cursor: pointer;
    position: absolute;
    background-color: $primary-color;
    top: calc(100% + 4px);
    left: 0;
    justify-items: center;
    width: 300px;
    max-height: 300px;
    border-radius: 8px;
    padding: 3%;
    color: $menu-text-color;
    font-weight: bolder;
    z-index: 1;

    div {
        width: 100%;
        margin-top: 4px;
        margin-bottom: 4px;
        padding-top: 4px;
        padding-bottom: 4px;
        text-align: center;
        &.active {
            background-color: $menu-background-color-active;
            color: $text-color;
            border-radius: 4px;
        }
        &:hover {
            color: $text-color;
            background-color: $menu-background-color-hover;

        }
    }

}

.search_menu_fame {
    position: absolute;
    background-color: $primary-color;
    top: calc(100% + 4px);
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 200px;
    height: 80px;
    border-radius: 8px;
    padding: 3%;
    color: $menu-text-color;
    font-weight: bolder;
    z-index: 1;

    div {
        display: flex;
        justify-content: center;
        align-content: center;
        gap: 30px;
    }
}

.search_menu_tags {
    position: absolute;
    background-color: $primary-color;
    top: calc(100% + 4px);
    left: 0;
    justify-items: center;
    width: 300px;
    max-height: 300px;
    border-radius: 8px;
    padding: 3%;
    color: $menu-text-color;
    font-weight: bolder;
    z-index: 1;

    div {
        padding-top: 4px;
        padding-bottom: 4px;
    }
}

@media (max-width: $breakpoint-md) {
    .div_breaker {
        display: flex;
        flex-direction: column;
        width: 100%;
        align-items: flex-start;
    }
    .break_line {
    width: 100%;
    border-style: solid;
    height: 2px;
    border-width: 2px 0px 0px 0px;
    }
    .search_menu_fame .search_menu_tags .search_menu_location .search_menu_age {
        z-index: 1;
    }
}
</style>
