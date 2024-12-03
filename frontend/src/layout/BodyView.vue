<template>
    <TapTop />
    <div class="page-wrapper " :class="display ? 'compact-wrapper ' : layoutobj" id="pageWrapper">
        <div class="page-header row" :class="{ close_icon: !store.togglesidebar }">
            <Header @click="sidebar_toggle" />
        </div>
        <div class="page-body-wrapper">
            <div class="sidebar-wrapper" :data-layout="storeLayout.svg == 'stroke-svg' ? 'stroke-svg' : 'fill-svg'"
                :class="[{ close_icon: !store.togglesidebar, 'sidebar-default': store.perentName }]">
                <Sidebar @click="sidebar_toggle" />
            </div>
            <div class="page-body">

                <router-view></router-view>

            </div>
            <FooterView />
        </div>
    </div>
    <Customizer />
</template>
<script lang="ts" setup>
import { defineAsyncComponent, ref, onMounted, watch } from 'vue'
import { useMenuStore } from "@/store/menu";
import { uselayoutStore } from "@/store/layout";
import { storeToRefs } from "pinia";
const Header = defineAsyncComponent(() => import("@/components/common/block/header/index.vue"))
const Sidebar = defineAsyncComponent(() => import("@/components/common/block/sidebar/index.vue"))
const FooterView = defineAsyncComponent(() => import("@/components/common/block/FooterView.vue"))
const TapTop = defineAsyncComponent(() => import("@/layout/TapTop.vue"))
const Customizer = defineAsyncComponent(() => import("@/components/common/block/customizer/indexCustomizer.vue"))
let sidebar_toggle_var = ref<boolean>(false);
let display = ref<boolean>(false)
let layoutobj = ref<any>({});
const store = useMenuStore();
const storeLayout = uselayoutStore();
const { layouts: layouts } = storeToRefs(storeLayout);
watch(
    () => layouts,
    () => {
        layoutobj.value = storeLayout.layouts.settings.sidebar_setting;
    },
    { deep: true },
);
watch(
    () => "router",
    () => {

        if ((window.innerWidth < 991 && storeLayout.layouts.settings.layout === 'Horizontal')) {
            const newlayout = JSON.parse(JSON.stringify(layoutobj).replace('horizontal-wrapper', 'compact-sidebar compact-small material-icon'));
            layoutobj.value = JSON.parse(JSON.stringify(newlayout))[storeLayout.layouts.settings.layout];
        } else {
            layoutobj.value = JSON.parse(JSON.stringify(layoutobj))[storeLayout.layouts.settings.layout];
        }
    }
)
function sidebar_toggle(value: boolean) {
    sidebar_toggle_var.value = !value;
}
function handleScroll() {
    if (window.innerWidth <= 1199) {
        display.value = true;
        store.togglesidebar = false

    } else {
        store.togglesidebar = true
        display.value = false;
    }
}
onMounted(() => {

    window.addEventListener('resize', handleScroll);
    layoutobj.value = storeLayout.layouts.settings.sidebar_setting;

});
</script>