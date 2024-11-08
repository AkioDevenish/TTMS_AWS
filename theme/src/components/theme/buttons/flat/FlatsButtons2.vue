<template>
    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Custom state buttons" :desc="desc" text="true">
        <a class="btn btn-square btn-primary" href="#" data-toggle="tooltip" title="btn btn-primary" role="button">Link</a>
        <input class="btn btn-square btn-secondary" type="button" value="Input" data-toggle="tooltip"
            title="btn btn-secondary">
        <input class="btn btn-square btn-success" type="submit" value="Submit" data-toggle="tooltip"
            title="btn btn-success">
        <button class="btn btn-square btn-info" type="submit" data-toggle="tooltip" title="btn btn-info">Button</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline buttons" :desc="desc1" text="true">
        <button class="btn btn-square" :class="item.classes" v-for="(item, index) in color" :key="index" type="button">{{
            item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="bold Border outline buttons" :desc="desc2" text="true">
        <button class="btn btn-square" :class="item.classes" v-for="(item, index) in outline" :key="index" type="button">{{
            item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline Large buttons" :desc="desc3" text="true">
        <button class="btn btn-square  btn-lg" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline small buttons" :desc="desc4" text="true">
        <button class="btn btn-square  btn-sm" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Outline extra small buttons" :desc="desc5" text="true">
        <button class="btn btn-square btn-xs" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Disabled outline buttons" :desc="desc6" text="true">
        <button class="btn btn-square disabled" :class="item.classes" v-for="(item, index) in color" :key="index"
            type="button">Disabled</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Gradien buttons" :desc="desc7" text="true">
        <button class="btn btn-square" :class="item.classes" v-for="(item, index) in gradien" :key="index" type="button">{{
            item.title }}</button>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { Tooltip } from "bootstrap";
import { color, outline, gradien } from "@/core/data/buttons"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("The <code>.btn</code> class used with <code>&lt;button&gt;</code>, <code>&lt;a&gt;</code> and <code>&lt;input&gt;</code> elements.")
let desc1 = ref<string>("Add <code>.btn-square</code> and <code>.btn-outline-*</code> class for button with outline")
let desc2 = ref<string>("Add <code>.btn-square</code> and <code>.btn-outline-*-2x</code> class for button with bold outline")
let desc3 = ref<string>("Add <code>.btn-square</code>,<code>.btn-outline-*</code> and <code>.btn-lg</code> class for large button")
let desc4 = ref<string>('Add <code>.btn-square</code>,<code>.btn-outline-*</code> and <code>.btn-sm</code> class for small button')
let desc5 = ref<string>("Add <code>.btn-square</code>,<code>.btn-outline-*</code> and <code>.btn-xs</code> class for extra small button")
let desc6 = ref<string>('Add <code>.disabled</code> class or <code>disabled="disabled"</code> attribute for disabled button')
let desc7 = ref<string>('Add <code>.btn-square</code> and <code>.btn-*-gradien</code> class for gradien button')
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>