<template>
     <div class="container-fluidz">
        <div class="row">
             <SimplePagination />
            <DisabledPagination />
            <IconsPagenation />
            <RoundedPagination />
            <AlignmentsPagination />
            <SizingPagination />
        </div>
     </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const SimplePagination = defineAsyncComponent(() => import("@/components/theme/advance/pagination/SimplePagination.vue"))
const DisabledPagination = defineAsyncComponent(() => import("@/components/theme/advance/pagination/DisabledPagination.vue"))
const IconsPagenation = defineAsyncComponent(() => import("@/components/theme/advance/pagination/IconsPagenation.vue"))
const RoundedPagination = defineAsyncComponent(() => import("@/components/theme/advance/pagination/RoundedPagination.vue"))
const AlignmentsPagination = defineAsyncComponent(() => import("@/components/theme/advance/pagination/AlignmentsPagination.vue"))
const SizingPagination = defineAsyncComponent(() => import("@/components/theme/advance/pagination/SizingPagination.vue"))
</script>