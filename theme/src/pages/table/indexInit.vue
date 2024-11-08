<template>
    <div class="container-fluid">
        <div class="row">
            <zeroConfiguration />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const zeroConfiguration = defineAsyncComponent(() => import("@/components/theme/table/basicinit/zeroConfiguration.vue"))
</script>