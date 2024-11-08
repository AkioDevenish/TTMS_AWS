<template>
    <Card1 colClass="col-xl-6 col-md-6 proorder-md-2" dropdown="true" headerTitle="true" title="Study Statistics"
        cardhaderClass="card-no-border pb-0">
        <div class="studay-statistics">
            <ul class="d-flex align-item-center gap-2">
                <li> <span class="bg-primary"> </span>UX Design</li>
                <li> <span class="bg-secondary"> </span>Illustrations</li>
            </ul>
        </div>
        <div id="study-statistics">
            <apexchart type="area" height="230" ref="chart" :options="chartOptions12" :series="series12">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series12, chartOptions12, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>