<template>
    <Card1 colClass="col-xxl-5 col-xl-4 col-lg-7 col-sm-12" dropdown="true" headerTitle="true" title="Sales Overview"
        cardhaderClass="card-no-border pb-0" cardbodyClass="pt-0 ">
        <div id="salse-overview">
            <apexchart type="rangeBar" height="350" ref="chart" :options="chartOptions11" :series="series11">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series11, chartOptions11, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>