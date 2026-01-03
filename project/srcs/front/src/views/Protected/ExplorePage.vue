<script setup>
import Button from '@/components/Button.vue';
import SearchBarElem from '@/components/SearchBarElem.vue';
// import { RouterLink, RouterView } from 'vue-router';
import Fame from '@/components/Fame.vue';


const handleSubmit = () => {
    console.log("SEARCH!")
}
const handleClick = () => {

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
                <SearchBarElem :firstElem="true" elemName="Location" 
                    :locationList="['Agadir', 'Agadir', 'Agadir', 'Agadir','Agadir', 'Agadir']" />

                <div class="div_breaker">
                    <div class="break_line"></div>
                    <div class="search_type">
                        <div class="label_input">
                            <h3>Location</h3>
                            <input type="image" src="/img/arrowDownIcon.svg" />
                        </div>
                        <div>Agadir</div>

                    </div>
                    <!-- <div class="search_menu" style="flex-direction: column;">
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                        <div>
                            Agadir
                        </div>
                    </div> -->
                </div>
                <div class="div_breaker">
                    <div class="break_line"></div>
                    <div class="search_type">
                        <div class="label_input">
                            <h3>Fame</h3>
                            <input type="image" src="/img/arrowDownIcon.svg" />
                        </div>
                        <Fame />
                    </div>
                    <!-- <div class="search_menu">
                        <div>
                            <input type="image"src="/img/lessIcon.svg"> 5.00 <input type="image" src="/img/plusIcon.svg">
                        </div>
                    </div> -->
                </div>
                <div class="div_breaker">
                    <div class="break_line"></div>
                    <div class="search_type">
                        <div class="label_input">
                            <h3>Tags</h3>
                            <input type="image" src="/img/arrowDownIcon.svg" />
                        </div>
                        <div style="display: flex; gap: 2px;"><span>#Sport,</span> <span>#Football...</span></div>
                    </div>
                    <!-- <div class="search_menu" style="flex-direction: column;">
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                        <div>
                            Code
                        </div>
                    </div> -->
                </div>
                <Button class="btn" @click="handleSubmit" text="Search"></Button>
            </div>
        </div>
        <div class="body">

            <div class="user_card">
                <img src="/img/avatar.svg" alt="">
                <span>Saad</span>
                <div>
                    <span>Age</span>
                    -
                    <span>Location</span>
                </div>
                <Fame />
                <Button style="background-color: #BC80DC;color: #592F6F;" class="user_card_btn" text="Like"></Button>
                <Button class="user_card_btn" text="View Profile"></Button>

            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>

.user_card {
    padding: 2%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 260px;

    background-color: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    gap:5px;
}

.user_card_btn {
    width: 100%;
    max-width: 200px;

}

.wraper {
    padding: 3%;

}

.search_holder {
    width: 100%;
    overflow: visible;
    margin-bottom: 2%;
    // align-content: center;
}

// for Age
// .search_menu {
//     position: absolute;
//     background-color: #E6E6E6;
//     top: calc(100% + 4px);
//     left: 0;
//     display: flex;
//     justify-content: center;
//     gap: 10%;
//     align-items: center;
//     width: 300px;
//     height: 80px;
//     border-radius: 8px;
//     padding: 3%;
//     color: #75478D;
//     font-weight: bolder;
//     div {
//         display: flex;
//         justify-content: center;
//         align-content: center;
//         gap: 5px;
//     }
// }

// for Location
// .search_menu {
//     position: absolute;
//     background-color: #E6E6E6;
//     top: calc(100% + 4px);
//     left: 0;
//     justify-items: center;
//     width: 300px;
//     max-height: 300px;
//     border-radius: 8px;
//     padding: 3%;
//     color: #75478D;
//     font-weight: bolder;
//     // overflow:visible;
//     div {
//         padding-top: 4px;
//         padding-bottom: 4px;
//     }
// }

// for Fame
// .search_menu {
//     position: absolute;
//     background-color: #E6E6E6;
//     top: calc(100% + 4px);
//     left: 0;
//     display: flex;
//     justify-content: center;
//     align-items: center;
//     width: 200px;
//     height: 80px;
//     border-radius: 8px;
//     padding: 3%;
//     color: #75478D;
//     font-weight: bolder;
//     div {
//         display: flex;
//         justify-content: center;
//         align-content: center;
//         gap: 30px;
//     }
// }

// for Tags
.search_menu {
    position: absolute;
    background-color: #E6E6E6;
    top: calc(100% + 4px);
    left: 0;
    justify-items: center;
    width: 300px;
    max-height: 300px;
    border-radius: 8px;
    padding: 3%;
    color: #75478D;
    font-weight: bolder;
    // overflow:visible;
    div {
        padding-top: 4px;
        padding-bottom: 4px;
    }
}

.btn {
    width: 20%;
    margin-left: 3%;
}

.inner_search_bar {
    padding-left: 3%;
    padding-right: 3%;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    height: 83px;
    background-color: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    border-color: #BD82DD;
    border-style: solid;
    border-width: 1px;
    overflow: visible;
}

.search_type {
    display: flex;
    // width: 100%;
    flex-direction: column;

}

.div_breaker {
    position: relative;
    display: flex;
    overflow: visible;
    gap: 20px;
    height: 100%;
    // width: 20%;
    // height: 20%;
    justify-content: center;
    align-items: center;
    // flex-direction: column;

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
    border-color: #BD82DD;
}

@media (max-width: $breakpoint-md) {
    .page {
        display: flex;
        flex-direction: column;
        // margin: 0;
    }
}
</style>
