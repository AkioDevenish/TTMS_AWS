<template>
    <div class="tab-pane fade show active" id="c-pills-home" :class="{ 'active show': store.customizer == 'settings' }"
        role="tabpanel" aria-labelledby="c-pills-home-tab">
        <LayoutType />
        <SidebarType />
        <SidebarIcon />
        <CustomColor />
        <MixLayout />
    </div>
</template>
<script lang="ts" setup>
import { useMenuStore } from '@/store/menu'
import { defineAsyncComponent } from 'vue';
const LayoutType = defineAsyncComponent(() => import("@/components/common/block/customizer/LayoutType.vue"))
const SidebarType = defineAsyncComponent(() => import("@/components/common/block/customizer/SidebarType.vue"))
const SidebarIcon = defineAsyncComponent(() => import("@/components/common/block/customizer/SidebarIcon.vue"))
const CustomColor = defineAsyncComponent(() => import("@/components/common/block/customizer/CustomColor.vue"))
const MixLayout = defineAsyncComponent(() => import("@/components/common/block/customizer/MixLayout.vue"))
const store = useMenuStore()
</script>