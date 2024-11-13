<template>
    <div class="chart-container progress-chart">
        <div id="progress1">
            <apexchart type="bar" height="70" ref="chart" :options="chartOptions10" :series="series10">
            </apexchart>
        </div>
        <div id="progress2">
            <apexchart type="bar" height="70" ref="chart" :options="chartOptions11" :series="series11">
            </apexchart>
        </div>
        <div id="progress3">
            <apexchart type="bar" height="70" ref="chart" :options="chartOptions12" :series="series12">
            </apexchart>
        </div>
        <div id="progress4">
            <apexchart type="bar" height="70" ref="chart" :options="chartOptions13" :series="series13">
            </apexchart>
        </div>
        <div id="progress5">
            <apexchart type="bar" height="70" ref="chart" :options="chartOptions14" :series="series14">
            </apexchart>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { series10, chartOptions10, series11, chartOptions11, series12, chartOptions12, series13, chartOptions13, series14, chartOptions14 } from "@/core/data/widgets-chart"
</script>