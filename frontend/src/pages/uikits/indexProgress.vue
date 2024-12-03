<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <BasicProgressbar />
                <div class="row">
                    <StripedProgressbar />
                </div>
                <div class="row">
                    <MultipleBars />
                </div>
                <CustomProgressbars />
                <div class="row">
                    <SmallProgressbars />
                </div>
                <HeightProgressbars />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicProgressbar = defineAsyncComponent(() => import("@/components/theme/uikits/progress/BasicProgressbar.vue"))
const StripedProgressbar = defineAsyncComponent(() => import("@/components/theme/uikits/progress/StripedProgressbar.vue"))
const MultipleBars = defineAsyncComponent(() => import("@/components/theme/uikits/progress/MultipleBars.vue"))
const CustomProgressbars = defineAsyncComponent(() => import("@/components/theme/uikits/progress/CustomProgressbars.vue"))
const SmallProgressbars = defineAsyncComponent(() => import("@/components/theme/uikits/progress/SmallProgressbars.vue"))
const HeightProgressbars = defineAsyncComponent(() => import("@/components/theme/uikits/progress/HeightProgressbars.vue"))
</script>