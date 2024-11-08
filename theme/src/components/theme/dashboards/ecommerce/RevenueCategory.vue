<template>
    <Card1 colClass="col-xl-3 col-lg-5 col-sm-6" dropdown="true" headerTitle="true" title="Revenue By Category"
        cardhaderClass="card-no-border pb-0" cardbodyClass="revenue-category">
        <div id="pie-chart">
            <apexchart type="radialBar" height="350" ref="chart" :options="chartOptions16" :series="series16">
            </apexchart>
        </div>
        <div class="donut-legend" id="legend"></div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series16, chartOptions16, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>