<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <ZentraInsMonitor />
            <ZentraStatistics />
            <ZentraTempCard />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const ZentraInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/zentra/ZentraInsMonitor.vue"))
const ZentraTempCard = defineAsyncComponent(() => import("@/components/theme/stations/zentra/ZentraTempCard.vue"))
const ZentraStatistics = defineAsyncComponent(() => import("@/components/theme/stations/zentra/ZentraStatistics.vue"))
</script>