<template>
  <Card1 colClass="col-xxl-6 col-xl-4 col-md-12" cardClass="visitor-card" headerCard="true" title="Visitors"
    cardhaderClass="card-no-border pb-0" cardbodyClass="pt-3 ">
    <div class="visitors-container">
      <div id="visitor-chart">
        <apexchart type="bar" height="220" ref="chart" :options="chartOptions" :series="series">
        </apexchart>
      </div>
    </div>
  </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series, chartOptions, } from "@/core/data/widgets-chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>