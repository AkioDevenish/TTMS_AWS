<template>
    <div>
        <SidebarLoge />
        <nav class="sidebar-main">
            <div id="sidebar-menu">
                <li class="left-arrow" :class="hideLeftArrow ? 'disabled' : hideLeftArrow" @click="display2()">
                    <vue-feather type="arrow-left"></vue-feather>
                </li>
                <ul class="sidebar-links custom-scrollbar"
                    :style="[layoutobject?.includes('horizontal-wrapper') ? { 'margin-left': margin + 'px' } : {}]"
                    id="simple-bar">

                    <NavMenu />
                </ul>
                <li class="right-arrow" :class="hideRightArrow ? 'disabled' : hideRightArrow" @click="display()">
                    <vue-feather type="arrow-right"></vue-feather>
                </li>
            </div>
        </nav>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent, ref, watch, computed, defineEmits, onMounted } from 'vue'
import { uselayoutStore } from "@/store/layout";
import { useMenuStore } from "@/store/menu";
import { useRouter } from 'vue-router'
const SidebarLoge = defineAsyncComponent(() => import("@/components/common/block/sidebar/SidebarLoge.vue"))
const NavMenu = defineAsyncComponent(() => import("@/components/common/block/sidebar/NavMenu.vue"))
let sidebarType = useMenuStore();
let route = useRouter()
let emit = defineEmits(['click']);
let layoutobj = ref<any>({});
let isVisibe = ref<boolean>(true);
let store = useMenuStore();
let storeLayout = uselayoutStore();
let hideRightArrow = ref(store.hideRightArrow);
let hideLeftArrow = ref(store.hideLeftArrow);
let margin = ref(store.margin);
let isActive = ref<boolean>(false);
const layoutobject: any = computed({
    get() {
        return storeLayout.layouts.settings.sidebar_setting;
    },
    set() {
        layoutobj.value = storeLayout.layouts.settings.sidebar_setting;
        return layoutobj;
    },
});
onMounted(() => {
    setTimeout(() => {
        const elmnt = document.getElementById("myDIV");

        store.menuWidth > window.innerWidth ? ((store.hideRightArrow = false), (store.hideLeftArrowRTL = false)) : ((store.hideRightArrow = false), (store.hideLeftArrowRTL = true));
    }, 500);
    if (margin.value == 0) {
        hideRightArrow.value = false
    }
});

function display() {
    if (isActive.value == false) {
        isActive.value = !isActive.value;
    }
    if (margin.value >= -2500) {
        margin.value = margin.value - 500;
        hideLeftArrow.value = false;
        hideRightArrow.value = false
    }
    if (margin.value == -3000) {
        hideRightArrow.value = true
    }
}
function display2() {
    if (margin.value <= -500) {
        margin.value = margin.value + 500;
        hideLeftArrow.value = false;
        hideRightArrow.value = false
    }
    if (margin.value == 0) {
        hideLeftArrow.value = true;
    }
}
</script>