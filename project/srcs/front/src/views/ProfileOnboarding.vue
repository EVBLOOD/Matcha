<script setup>
import Card from '@/components/Card.vue';
    import Button from '@/components/Button.vue';
    import Input from '@/components/Input.vue';
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
                        <label style="display: flex; justify-content: center; align-items: center;" for="files"><img src="/img/vector.svg" alt=""></label>
                    </div>
                 </div>
                <p>Saad AKLLAM</p>
            </div>

            <div>
                <p>Gender</p> 
                <div>
                     <input type="radio" name="m" id="Male"> <label for="m">Male</label>
                </div>
                <div>
                     <input type="radio" name="m" id="Female"> <label for="m">Female</label>
                </div>
                <div>
                     <input type="radio" name="m" id="Other"> <label for="m">Other</label>
                </div>
            </div>

            <div>
                <p>Orientation</p> 
                <select id="orientation">
                  <option value="a">A</option>
                  <option value="b">B</option>
                  <option value="c">C</option>
                </select>
            </div>

            <div>
                <!-- <p>Interest</p>  I don't know how they will make this goes as it should when the list is too long -->
                <p>Interest</p>  
                <select id="orientation">
                  <option value="a">A</option>
                  <option value="b">B</option>
                  <option value="c">C</option>
                </select>
            </div>

            <div>
                <p>bio</p>  
                <textarea name="bio" id="bio"></textarea>
            </div>
            <div>
                <p>Photos</p>
                <div>
                    decoration or background
                    <input type="file" name="extra" id="">
                    <input type="file" name="extra" id="">
                    <input type="file" name="extra" id="">
                    <input type="file" name="extra" id="">
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
.avatar_upload {
    position: relative;
    width: 100%;
    display: flex;
    justify-items: center;
    align-items: center;
    flex-direction: column;
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

