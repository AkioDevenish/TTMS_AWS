<template>
    <Card1 :colClass="col" dropdown="true" headerTitle="true" title="Opening of leaflets"
        cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 opening-box">
        <div class="d-flex align-items-center gap-2">
            <h2>{{ doller }} 1,463</h2>
            <div class="d-flex">
                <p class="mb-0 up-arrow"><i class="fa fa-arrow-up"></i></p><span class="f-w-500 font-success">+
                    20.08%</span>
            </div>
        </div>
        <div id="growthchart">
            <apexchart type="line" height="150" ref="chart" :options="chartOptions" :series="series">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { series, chartOptions } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let props = defineProps({
    doller: String,
    col: String
})
</script>