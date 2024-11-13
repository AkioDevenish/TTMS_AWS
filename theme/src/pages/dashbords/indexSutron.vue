<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <SutronInsMonitor />
            <SutronStatistics />
            <SutronTempCard /> 
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const SutronInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/sutron/SutronInsMonitor.vue"))
const SutronTempCard = defineAsyncComponent(() => import("@/components/theme/stations/sutron/SutronTempCard.vue"))
const SutronStatistics = defineAsyncComponent(() => import("@/components/theme/stations/sutron/SutronStatistics.vue"))
</script>