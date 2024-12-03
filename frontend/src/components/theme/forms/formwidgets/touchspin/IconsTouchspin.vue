<template>
    <Card3 colClass="col-xl-6" cardbodyClass="common-flex pre-post-touchspin" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Icons with prefix and postfix" :desc="desc">
        <div class="input-group">
            <button class="decrement-touchspin btn-touchspin touchspin-primary" @click="primeryDecrement()"><i
                    class="fa fa-minus"></i></button><span class="input-group-text">$</span>
            <input class="input-touchspin  mx-1 spin-outline-primary" type="number" v-model="conter">
            <button class="increment-touchspin btn-touchspin touchspin-primary" @click="primeryIncrement()"><i
                    class="fa fa-plus"> </i></button>
        </div>
        <div class="input-group">
            <button class="decrement-touchspin btn-touchspin touchspin-primary" @click="secondaryDecrement()"><i
                    class="fa fa-minus"></i></button>
            <input class="input-touchspin  mx-1 spin-outline-primary" type="number" v-model="conter1"><span
                class="input-group-text">%</span>
            <button class="increment-touchspin btn-touchspin touchspin-primary" @click="secondaryIncrement()"><i
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