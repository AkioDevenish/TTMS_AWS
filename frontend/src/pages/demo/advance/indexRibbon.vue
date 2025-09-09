<template>
    <div class="container-fluid">
        <LeftRibbons/>
        <RightRibbons/>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const LeftRibbons = defineAsyncComponent(() => import("@/components/theme/advance/ribbons/LeftRibbons.vue"))
const RightRibbons = defineAsyncComponent(() => import("@/components/theme/advance/ribbons/RightRibbons.vue"))
</script>