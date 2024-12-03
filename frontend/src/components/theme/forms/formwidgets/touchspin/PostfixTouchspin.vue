<template>
    <Card3 colClass="col-xl-6" cardbodyClass="common-flex pre-post-touchspin bg-touchspin" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Buttons with prefix and postfix" :desc="desc">
        <div class="input-group">
            <button class="decrement-touchspin btn-touchspin touchspin-warning" @click="primeryDecrement()"><i
                    class="fa fa-minus"></i></button>
            <button class="btn-outline-warning" id="button-addon1" type="button">Pre</button>
            <input class="input-touchspin  mx-1 spin-outline-primary" type="number" v-model="conter">
            <button class="increment-touchspin btn-touchspin touchspin-warning" @click="primeryIncrement()"><i
                    class="fa fa-plus"> </i></button>
        </div>
        <div class="input-group">
            <button class="decrement-touchspin btn-touchspin touchspin-warning" @click="secondaryDecrement()"><i
                    class="fa fa-minus"></i></button>
            <input class="input-touchspin  mx-1 spin-outline-primary" type="number" v-model="conter1">
            <button class="btn-outline-warning" id="button-addon2" type="button">Post</button>
            <button class="increment-touchspin btn-touchspin touchspin-warning" @click="secondaryIncrement()"><i
                    class="fa fa-plus"></i></button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))

let desc = ref<string>("  Use the <code>.decrement-touchspin </code>and <code>.increment-touchspin </code>class.")
let conter = ref<number>(0)
let conter1 = ref<number>(0)
function primeryIncrement() {
    conter.value++
}
function primeryDecrement() {
    if (conter.value > 0) {
        conter.value--
    }
}
function secondaryIncrement() {
    conter1.value++
}
function secondaryDecrement() {
    if (conter1.value > 0) {
        conter1.value--
    }
}
</script>