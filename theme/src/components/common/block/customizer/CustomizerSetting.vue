<template>
    <a class="nav-link" :class="{ 'active show': store.customizer == 'settings' }" id="c-pills-home-tab"
        @click="openCustomizerSetting('settings')" href="javascript:void(0)">
        <div class="settings"><img src="@/assets/images/customizer/color.png" alt="color"></div><span>Quick option</span>
    </a>
</template>
<script lang="ts" setup>
import { useMenuStore } from '@/store/menu'
import { uselayoutStore } from "@/store/layout"

const storeLayout = uselayoutStore()

let store = useMenuStore()
function openCustomizerSetting(val: string) {
    store.customizer = val;
}
</script>