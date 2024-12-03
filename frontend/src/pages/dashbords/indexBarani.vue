<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <BaraniInsMonitor />
            <BaraniStatistics />
            <BaraniTempCard /> 
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const BaraniInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/barani/BaraniInsMonitor.vue"))
const BaraniTempCard = defineAsyncComponent(() => import("@/components/theme/stations/barani/BaraniTempCard.vue"))
const BaraniStatistics = defineAsyncComponent(() => import("@/components/theme/stations/barani/BaraniStatistics.vue"))
</script>