<template>
    <div class="container-fluid">
        <div class="row">
            <BasicGroup />
            <OutlineGroup />
            <NestingGroup />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicGroup = defineAsyncComponent(() => import("@/components/theme/buttons/group/BasicGroup.vue"))
const OutlineGroup = defineAsyncComponent(() => import("@/components/theme/buttons/group/OutlineGroup.vue"))
const NestingGroup = defineAsyncComponent(() => import("@/components/theme/buttons/group/NestingGroup.vue"))
</script>