<template>
    <div class="customizer-links" :class="{ open: store.customizer }">
        <div class="nav flex-column nac-pills" id="c-pills-tab" role="tablist" aria-orientation="vertical">
            <CustomizerSetting />
            <CustomizerSupport />
            <DocumentSection />
            <CheckFeatures />
            <BuyNow />
        </div>
    </div>
    <div class="customizer-contain" :class="{ open: store.customizer }">
        <div class="tab-content" id="c-pills-tabContent">
            <ConfigurationView />
            <div class="customizer-body custom-scrollbar">
                <CustomSetting />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { useMenuStore } from '@/store/menu'
import { defineAsyncComponent } from 'vue';
const CustomizerSetting = defineAsyncComponent(() => import("@/components/common/block/customizer/CustomizerSetting.vue"))
const CustomizerSupport = defineAsyncComponent(() => import("@/components/common/block/customizer/CustomizerSupport.vue"))
const DocumentSection = defineAsyncComponent(() => import("@/components/common/block/customizer/DocumentSection.vue"))
const CheckFeatures = defineAsyncComponent(() => import("@/components/common/block/customizer/CheckFeatures.vue"))
const ConfigurationView = defineAsyncComponent(() => import("@/components/common/block/customizer/ConfigurationView.vue"))
const BuyNow = defineAsyncComponent(() => import("@/components/common/block/customizer/BuyNow.vue"))
const CustomSetting = defineAsyncComponent(() => import("@/components/common/block/customizer/CustomSetting.vue"))
const store = useMenuStore()
store.customizer
</script>