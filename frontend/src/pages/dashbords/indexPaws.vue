<template>
    <div class="container-fluid dashboard-4">
        <div class="row">
            <PawsInsMonitor />
            <PawsStatistics />
            <PawsTempCard /> 
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const PawsInsMonitor = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsInsMonitor.vue"))
const PawsTempCard = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsTempCard.vue"))
const PawsStatistics = defineAsyncComponent(() => import("@/components/theme/stations/paws/PawsStatistics.vue"))
</script>