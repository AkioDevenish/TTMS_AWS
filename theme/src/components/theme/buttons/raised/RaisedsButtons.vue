<template>
    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Default buttons" :desc="desc" text="true">
        <button class="btn btn-pill" data-bs-toggle="tooltip" :title="'btn btn-pill ' + item.classes" :class="item.classes"
            v-for="(item, index) in raised " :key="index" type="button">{{
                item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Large buttons" :desc="desc1" text="true">
        <button class="btn btn-pill  btn-lg" data-bs-toggle="tooltip" :title="'btn btn-pill btn-lg ' + item.classes"
            :class="item.classes" v-for="(item, index) in raised" :key="index" type="button">{{
                item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Small buttons" :desc="desc2" text="true">
        <button class="btn btn-pill btn-sm" :class="item.classes" v-for="(item, index) in raised" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Extra Small buttons" :desc="desc3" text="true">
        <button class="btn btn-pill btn-xs" :class="item.classes" v-for="(item, index) in raised" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Active Buttons" :desc="desc4" text="true">
        <button class="btn btn-pill active" :class="item.classes" v-for="(item, index) in raised" :key="index"
            type="button">Active</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Disabled buttons" :desc="desc5" text="true">
        <button class="btn btn-pill disabled" :class="item.classes" v-for="(item, index) in raised" :key="index"
            type="button">Disabled</button>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { Tooltip } from "bootstrap";
import { raised } from "@/core/data/buttons"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Add <code>.btn-pill</code> and <code>.btn-air-*</code> class for raised button")
let desc1 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-air-*</code> and <code>.btn-lg</code> class for large button")
let desc2 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-air-*</code> and <code>.btn-sm</code> class for small button")
let desc3 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-air-*</code> and <code>.btn-xs</code> class for extra small button")
let desc4 = ref<string>('Add <code>.active</code> for active state')
let desc5 = ref<string>('Add <code>.disabled</code> class or <code>disabled="disabled"</code> attribute for disabled button')
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>