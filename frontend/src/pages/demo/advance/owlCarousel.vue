<template>
    <div class="container-fluid">
        <div class="row">
            <SlidesOnly />
            <WithControls />
            <AutoPlay />
            <MouseWheel />
            <WithIndicators />
            <WithCaptions />
            <CrossFade />
            <IndividualCarousel />
            <DisableTouch />
            <DarkVariant />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const SlidesOnly = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/SlidesOnly.vue"))
const WithControls = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/WithControls.vue"))
const AutoPlay = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/AutoPlay.vue"))
const MouseWheel = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/MouseWheel.vue"))
const WithIndicators = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/WithIndicators.vue"))
const WithCaptions = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/WithCaptions.vue"))
const CrossFade = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/CrossFade.vue"))
const IndividualCarousel = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/IndividualCarousel.vue"))
const DisableTouch = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/DisableTouch.vue"))
const DarkVariant = defineAsyncComponent(() => import("@/components/theme/advance/owlcarousel/DarkVariant.vue"))
</script>