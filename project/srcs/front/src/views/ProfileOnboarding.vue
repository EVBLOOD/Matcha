<script setup>
    import Button from '@/components/Button.vue';
</script>

<template>
    <div class="page">
        <div class="content">
            <h2>Complete Your Profile</h2>

            <div>
                <input type="image" src="/" alt="idno why">
                <input type="file" name="profile" id="profile">
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
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .page{
        display: grid;
        grid-template-columns: 1fr 1fr;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 40px 20px;
        .content {
            overflow: hidden;
            p {
                margin-bottom: 30px;
            }
        }
        .title{
            font-weight: 700;
            font-size: 40px;
        }
        .description{
            font-size: 30px;
        }
        .image img{
            height: auto;
            width: 100%;
        }
    }
    @media (max-width: $breakpoint-md) {
        .page{
            display: flex;
            flex-direction: column;
            // margin: 0;
        }
    }
</style>

