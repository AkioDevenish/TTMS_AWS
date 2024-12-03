<template>
    <Card1 colClass="col-xl-5 col-xl-50 proorder-md-5" dropdown="true" headerTitle="true" title="Projects Overview"
        cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0">


        <div class="current-sale-container order-container">
            <div class="overview-wrapper" id="orderoverview">
                <apexchart type="line" height="350" ref="chart" :options="chartOptions5" :series="series5">
                </apexchart>
            </div>
            <div class="back-bar-container">
                <div id="order-bar">
                    <apexchart type="bar" height="180" ref="chart" :options="chartOptions6" :series="series6">
                    </apexchart>
                </div>
            </div>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { series5, chartOptions5, series6, chartOptions6 } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>