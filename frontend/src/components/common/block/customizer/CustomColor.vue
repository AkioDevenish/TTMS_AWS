<template>
    <h5>Unlimited Color</h5>
    <ul class="layout-grid unlimited-color-layout">
        <input id="ColorPicker1" type="color" v-model="primary" name="Background">
        <input id="ColorPicker2" type="color" v-model="secondary" name="Background">
        <button type="button" class="color-apply-btn btn btn-primary color-apply-btn" @click="customizeColor">Apply</button>
    </ul>
</template>
<script lang="ts" setup>
import { ref, watch, onMounted } from "vue"
import { useMenuStore } from '@/store/menu'
import { uselayoutStore } from '@/store/layout'
let layoutType = ref<string>('ltr')
let mixLayout = ref<string>('default')
let store = useMenuStore()
let storeLayout = uselayoutStore()
let primary = ref<string | null>('#7A70BA')
let secondary = ref<string | null>('#48A3D7')
let layout = storeLayout.layout
store.customizer
storeLayout.boxlayout
function customizeMixLayout(val: string) {
    mixLayout.value = val;
    document.body.className = val;
}
function customizeColor() {
    let primarycol = localStorage.getItem('primary_color');
    let secondarycol = localStorage.getItem('secondary_color');


    storeLayout.setColorScheme({ primary: primary.value, secondary: secondary.value });
    primary.value = primarycol
    secondary.value = secondarycol

}
onMounted(() => {
    let primarycol = localStorage.getItem('primary_color');
    let secondarycol = localStorage.getItem('secondary_color');
    primary.value = primarycol ? primarycol : '#7A70BA'
    secondary.value = secondarycol ? secondarycol : '#48A3D7'
})
</script>