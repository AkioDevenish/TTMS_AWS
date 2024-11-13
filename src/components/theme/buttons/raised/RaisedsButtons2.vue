<template>
    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Custom state buttons" :desc="desc" text="true">
        <a class="btn btn-pill btn-primary btn-air-primary" href="#" data-toggle="tooltip" title="btn btn-primary"
            role="button">Link</a>
        <input class="btn btn-pill btn-secondary btn-air-secondary btn-air-secondary" type="button" value="Input"
            data-toggle="tooltip" title="btn btn-secondary">
        <input class="btn btn-pill btn-success btn-air-success btn-air-success" type="submit" value="Submit"
            data-toggle="tooltip" title="btn btn-success">
        <button class="btn btn-pill btn-info btn-air-info btn-air-info" type="submit" title="btn btn-info">Button</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline buttons" :desc="desc1" text="true">
        <button class="btn btn-pill" :class="item.classes" v-for="(item, index) in color1" :key="index" type="button">{{
            item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="bold Border outline buttons" :desc="desc2" text="true">
        <button class="btn btn-pill" :class="item.classes" v-for="(item, index) in outline1" :key="index" type="button">{{
            item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline Large buttons" :desc="desc3" text="true">
        <button class="btn btn-pill btn-lg" :class="item.classes" v-for="(item, index) in color1" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="outline small buttons" :desc="desc4" text="true">
        <button class="btn btn-pill btn-sm" :class="item.classes" v-for="(item, index) in color1" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Outline extra small buttons" :desc="desc5" text="true">
        <button class="btn btn-pill btn-xs" :class="item.classes" v-for="(item, index) in color1" :key="index"
            type="button">{{
                item.title }}</button>
    </Card3>

    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Disabled outline buttons" :desc="desc6" text="true">
        <button class="btn btn-pill disabled" :class="item.classes" v-for="(item, index) in color1" :key="index"
            type="button">Disabled</button>
    </Card3>


    <Card3 cardbodyClass="common-flex" headerTitle="true" title="Gradien buttons" :desc="desc7" text="true">
        <button class="btn btn-pill" :class="item.classes" v-for="(item, index) in gradien1" :key="index" type="button">{{
            item.title }}</button>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { Tooltip } from "bootstrap";
import { color1, outline1, gradien1 } from "@/core/data/buttons"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>('The <code>.btn</code> class used with <code>&lt;button&gt;</code>, <code>&lt;a&gt;</code> and <code>&lt;input&gt;</code> elements.')
let desc1 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-air-*</code> and <code>.btn-outline-*</code> class for button with outline")
let desc2 = ref<string>("Add <code>.btn-pill</code>,<code>.btn-air-*</code> and <code>.btn-outline-*-2x</code> class for button with bold outline")
let desc3 = ref<string>("<code>.btn-pill</code>,<code>.btn-air-*</code>,<code>.btn-outline-*</code> and <code>.btn-lg</code> class for large button with outline")
let desc4 = ref<string>("<code>.btn-pill</code>,<code>.btn-air-*</code>,<code>.btn-outline-*</code> and <code>.btn-sm</code> class for small button with outline")
let desc5 = ref<string>('<code>.btn-pill</code>,<code>.btn-air-*</code>,<code>.btn-outline-*</code> and <code>.btn-xs</code> class for extra small button with outline')
let desc6 = ref<string>('Add <code>.disabled</code> class or <code>disabled="disabled"</code> attribute for disabled button')
let desc7 = ref<string>('<code>.btn-pill</code>,<code>.btn-air-*</code>,<code>.btn-*</code> and <code>.btn-*-gradien</code> class for gradien button')
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>