<template>
    <h5>Layout Type</h5>
    <ul class="main-layout layout-grid">
        <li data-attr="ltr" :class="{ active: layoutType == 'ltr' }" @click="customizeLayoutType('ltr')">
            <div class="header bg-light">
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div class="body">
                <ul>
                    <li class="bg-light sidebar"></li>
                    <li class="bg-light body">
                        <span class="badge badge-primary">LTR</span>
                    </li>
                </ul>
            </div>
        </li>
        <li data-attr="rtl" :class="{ active: layoutType == 'rtl' }" @click="customizeLayoutType('rtl')">
            <div class="header bg-light">
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div class="body">
                <ul>
                    <li class="bg-light body">
                        <span class="badge badge-primary">RTL</span>
                    </li>
                    <li class="bg-light sidebar"></li>
                </ul>
            </div>
        </li>
        <li v-bind:style="storeLayout.boxlayout ? '' : 'display: none;'" data-attr="box"
            :class="{ active: layoutType == 'box-layout' }" @click="customizeLayoutType('box-layout')"
            class="box-layout px-3">
            <div class="header bg-light">
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div class="body">
                <ul>
                    <li class="bg-light sidebar"></li>
                    <li class="bg-light body">
                        <span class="badge badge-primary">Box</span>
                    </li>
                </ul>
            </div>
        </li>
    </ul>
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useMenuStore } from "@/store/menu";
import { uselayoutStore } from "@/store/layout";
import { useRouter } from "vue-router";
let router = useRouter();
let layoutType = ref<string>("ltr");
let mixLayout = ref<string>("default");
let store = useMenuStore();
let storeLayout = uselayoutStore();
let layout = storeLayout.layouts;
let margin = ref(store.margin);
let layoff = ref<string>('')
store.customizer;
storeLayout.boxlayout;
function customizeLayoutType(val: string) {
    layoutType.value = val;
    storeLayout.setLayoutType(layout, val);
}
</script>