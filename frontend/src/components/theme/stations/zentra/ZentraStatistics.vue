<template>
    <Card1 colClass="col-xl-12 col-md-12 proorder-xl-2 proorder-md-2"  dropdown="true" headerTitle="true" title="z6-26732"
        cardhaderClass="card-no-border pb-0">
        
        <div class="studay-statistics ">
            <ul class="d-flex align-item-center gap-2">
                <li> <span class="bg-primary"> </span>Rainfall</li>
                <li> <span class="bg-secondary"> </span>AirTemperature</li>
            </ul>
        </div>
        <div id="study-statistics">
            <apexchart type="area" height="230" ref="chart" :options="chartOptions12" :series="zentrastats">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { chartOptions12, zentrastats, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>