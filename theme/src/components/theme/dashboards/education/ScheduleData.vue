<template>
    <Card1 colClass="col-xxl-5 col-xl-6 box-col-6 proorder-md-9" dropdown="true" headerTitle="true" title="Schedule"
        cardhaderClass="card-no-border pb-0" cardbodyClass="schedult-calendar pt-0 ">
        <div class="schedule-container">
            <div id="schedulechart">
                <apexchart type="rangeBar" height="355" ref="chart" :options="chartOptions15" :series="series15">
                </apexchart>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series15, chartOptions15, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>