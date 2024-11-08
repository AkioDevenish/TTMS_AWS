<template>
    <h5 class="">Mix Layout</h5>
    <ul class="layout-grid customizer-mix">
        <li class="color-layout" data-attr="light-only" :class="{ active: mixLayout == 'light-only' }"
            @click="customizeMixLayout('light-only')">
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
                    <li class="bg-light body"></li>
                </ul>
            </div>
        </li>
        <li class="color-layout" data-attr="dark-only" :class="{ active: mixLayout == 'dark-only' }"
            @click="customizeMixLayout('dark-only')">
            <div class="header bg-dark">
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div class="body">
                <ul>
                    <li class="bg-dark sidebar"></li>
                    <li class="bg-dark body"></li>
                </ul>
            </div>
        </li>
    </ul>
</template>
<script lang="ts" setup>
import { ref, watch, onMounted } from "vue"
import { useMenuStore } from '@/store/menu'
import { uselayoutStore } from '@/store/layout'

let mixLayout = ref<string>('default')
let store = useMenuStore()
let storeLayout = uselayoutStore()

store.customizer
storeLayout.boxlayout
function customizeMixLayout(val: string) {
    mixLayout.value = val;
    document.body.className = val;
}

</script>