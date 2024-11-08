<template>
    <Card1 colClass="col-xxl-7 col-xl-12 box-col-12 proorder-md-8" dropdown="true" headerTitle="true"
        title="Monthly Attendance Report (Feb)" cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 ">
        <div class="monthly-report">
            <ul class="d-flex align-item-center gap-2">
                <li> <span class="bg-primary"> </span>Teacher</li>
                <li> <span class="bg-secondary"> </span>Student</li>
            </ul>
        </div>
        <div id="monthly-reportchart">
            <apexchart type="line" height="315" ref="chart" :options="chartOptions14" :series="series14">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series14, chartOptions14, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>