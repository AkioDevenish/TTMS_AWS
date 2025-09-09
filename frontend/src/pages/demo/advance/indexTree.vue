<template>
    <div class="container-fluid">
        <div class="row">
            <BasicTree />
            <CheckTree />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicTree = defineAsyncComponent(() => import("@/components/theme/advance/tree/BasicTree.vue"))
const CheckTree = defineAsyncComponent(() => import("@/components/theme/advance/tree/CheckTree.vue"))
</script>