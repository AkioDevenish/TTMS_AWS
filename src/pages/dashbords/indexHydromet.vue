<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <HydrometInsMonitor />
            <HydrometStatistics />
            <HydrometTempCard /> 
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const HydrometInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/hydromet/HydrometInsMonitor.vue"))
const HydrometTempCard = defineAsyncComponent(() => import("@/components/theme/stations/hydromet/HydrometTempCard.vue"))
const HydrometStatistics = defineAsyncComponent(() => import("@/components/theme/stations/hydromet/HydrometStatistics.vue"))
</script>