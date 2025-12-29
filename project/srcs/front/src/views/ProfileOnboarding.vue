<script setup>
import Card from '@/components/Card.vue';
    import Button from '@/components/Button.vue';
    import InputLabel from '@/components/InputLabel.vue';
    import Select from '@/components/Select.vue';
import { ref } from 'vue';


    const orientation = [{ value: 'a', label: 'A' }, { value: 'b', label: 'B' }, { value: 'c', label: 'C' }]
    const selectedOrientation = ref('a');
    const selectedGender = ref('Male');
</script>

<template>
    <div class="page">
        <!-- <div class="content"> -->
            <Card title="Complete Your Profile">
            <div class="avatar_upload">
                 <div class="avatar_upload">
                    <div class="avatar"></div>
                    <div class="add_avatar">
                        <input type="file" id="files" class="hidden"/>
                        <label style="display: flex; justify-content: center; align-items: center; cursor: pointer;" for="files"><img src="/img/vector.svg" alt=""></label>
                    </div>
                 </div>
                <p class="full_name">Saad AKLLAM</p>
            </div>

            <div class="gender_div">
                <p>Gender</p>
                <div class="labels_list">
                    <InputLabel name="gender" label="Male" type="radio" id="Male" v-model="selectedGender"/>
                    <InputLabel name="gender" label="Female" type="radio" id="Female" v-model="selectedGender"/>
                    <InputLabel name="gender" label="Other" type="radio" id="Other" v-model="selectedGender"/>
                </div>
            </div>

            <div class="orientation_div">
                <p>Orientation</p> 
                <Select :options="orientation" v-model="selectedOrientation" />
            </div>

            <div class="interest_div">
                <p>Interest</p>
                <div class="interest_div_spans">
                    <div class="interest_span">#vegan</div>
                    <div class="interest_span">#geek</div>
                    <div class="interest_span">#sport</div>
                    <div class="interest_span">+ Add tag</div>
                </div>
            </div>

            <div class="bio_div">
                <p>Bio</p>  
                <textarea class="bio_erea" name="bio" id="bio" maxlength="500"></textarea>
            </div>

            <div class="bio_div">
                <p>Photos</p>
                <div>
                    <div class="add_pictures">
                        <input type="file" id="files" class="hidden"/>
                        <label style="display: flex; justify-content: center; align-items: center; cursor: pointer;" for="files"><img src="/img/add_picture.svg" alt=""></label>
                    </div>
                </div>
            </div>
            <Button to="home" text="Save and Continue"></Button>
            </Card>
        <!-- </div> -->
    </div>
</template>

<style lang="scss" scoped>
.page {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}


.add_pictures {
    width: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
}



.bio_div {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 2%;
}
.bio_erea {
    padding: 10px;
    border-color: #BD82DD;
    border-width: 1px;
    min-height: 36px;
    background: rgba(255, 255,255, 0.08);
    color: rgba(255, 255,255, 0.50);
    border-radius: 12px;
    resize: vertical;
    width: 100%;
}

.interest_span {
    padding: 3px;
    border-color: #BD82DD;
    border-style: solid;
    border-radius: 8px;

}
.interest_div_spans {
    display: flex;
    gap: 3px;
}
.interest_div {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 2%;
}

.orientation_div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2%;

}

.gender_div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2%;

}
.labels_list {
    display: flex;
    justify-content: space-around;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
}

.full_name {
    font-weight: 600;
    font-size: 18px;
}
.avatar_upload {
    position: relative;
    width: 100%;
    display: flex;
    justify-items: center;
    align-items: center;
    flex-direction: column;
    margin-bottom: 2%;
}
.avatar {
    width: 100px;
    height: 100px;
    background-image: url("/img/avatar.svg");
    border-radius: 50%;
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
}
.hidden {
    display: none;
}
.add_avatar {
    position: absolute;
    top: 70%;
    left:56%;
    background-color: #DEB0F5;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
}
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

