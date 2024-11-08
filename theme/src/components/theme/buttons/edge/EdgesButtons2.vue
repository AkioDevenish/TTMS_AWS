<template>
    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline buttons" :desc="desc" text="true">
        <button class="btn btn-pill" :class="item.classes" v-for="(item, index) in color" :key="index" type="button">{{
            item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="bold Border outline buttons" :desc="desc1" text="true">
        <button class="btn btn-pill" :class="item.classes" v-for="(item, index) in outline" :key="index" type="button">{{
            item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline Large buttons" :desc="desc2" text="true">
        <button class="btn btn-pill btn-lg" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline small buttons" :desc="desc3" text="true">
        <button class="btn btn-pill btn-sm" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Outline extra small buttons" :desc="desc4" text="true">
        <button class="btn btn-pill btn-xs" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Disabled outline buttons" :desc="desc5" text="true">
        <button class="btn btn-pill disabled" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">Disabled</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Gradien buttons" :desc="desc6" text="true">
        <button class="btn btn-pill" :class="item.classes" v-for="(item, index) in gradien" :key="index" type="button">{{
            item.title }}</button>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { Tooltip } from "bootstrap";
import { color, outline, gradien } from "@/core/data/buttons"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Add <code>.btn-pill</code> and <code>.btn-outline-*</code> class for button with outline")
let desc1 = ref<string>("Add <code>.btn-pill</code> and <code>.btn-outline-*-2x</code> class for button with bold outline")
let desc2 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-outline-*</code> and <code>.btn-lg</code> class for large button")
let desc3 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-outline-*</code> and <code>.btn-sm</code> class for small button")
let desc4 = ref<string>('Add <code>.btn-pill</code>,<code>.btn-outline-*</code> and <code>.btn-xs</code> class for extra small button')
let desc5 = ref<string>('Add <code>.disabled</code> class or <code>disabled="disabled"</code> attribute for disabled button')
let desc6 = ref<string>('Add <code>.btn-pill</code> and <code>.btn-*-gradien</code>class for gradien button')
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>