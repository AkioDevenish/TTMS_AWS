<template>
    <Card1 colClass="col-xxl-4 col-xl-7 box-col-7 col-md-6 proorder-md-3" dropdown="true" headerTitle="true"
        title="Actively Hours" cardhaderClass="card-no-border pb-0">
        <div id="actively-hours">
            <apexchart type="bar" height="345" ref="chart" :options="chartOptions13" :series="series13">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series13, chartOptions13, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>