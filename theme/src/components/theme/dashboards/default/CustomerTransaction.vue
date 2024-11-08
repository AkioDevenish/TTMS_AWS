<template>
    <Card1 colClass="col-xl-5 col-md-7 proorder-xl-4 box-col-5 proorder-md-6" dropdown="true" headerTitle="true"
        title="Customer Transaction" cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 ">

        <div id="customer-transaction">
            <apexchart type="bar" width="100%" height="350" ref="chart" :options="chartOptions2" :series="series2">
            </apexchart>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { series2, chartOptions2 } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>