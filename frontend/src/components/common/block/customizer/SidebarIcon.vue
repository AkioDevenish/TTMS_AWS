<template>
    <h5>Sidebar Icon</h5>
    <ul class="sidebar-setting layout-grid">
        <li :class="{ active: svg == 'stroke-svg' }" data-attr="stroke-svg" @click="customSvg('stroke-svg')">
            <div class="header bg-light">
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div class="body bg-light"><span class="badge badge-primary">Stroke</span>
            </div>
        </li>
        <li :class="{ active: svg == 'fill-svg' }" data-attr="fill-svg" @click="customSvg('fill-svg')">
            <div class="header bg-light">
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div class="body bg-light"><span class="badge badge-primary">Fill</span></div>
        </li>
    </ul>
</template>
<script lang="ts" setup>
import { ref, onMounted } from "vue";
import { useMenuStore } from "@/store/menu";
import { uselayoutStore } from "@/store/layout";
const svg = ref<string>('stroke-svg')
const store = useMenuStore();
let storeLayout = uselayoutStore();

store.customizer;
storeLayout.boxlayout;
function customSvg(val: string) {
    svg.value = val
    storeLayout.setSvg(val)
}
</script>