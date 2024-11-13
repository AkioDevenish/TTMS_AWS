<template>
    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" cardbodyClass="chart-block" headerTitle="true" title="Area Chart 2">
        <GChart class="chart-overflow" id="column-chart1" type="ColumnChart" :settings="{ packages: ['bar'] }"
            :data="area_chart2.chartData_1" :options="verticalChartOptions"
            :createChart="(el, google) => new google.charts.Bar(el)" @ready="onChartReady" />
    </Card3>
    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" cardbodyClass="chart-block" headerTitle="true" title="Column Chart 2">
        <GChart class="chart-overflow" id="column-chart2" type="ColumnChart" :settings="{ packages: ['bar'] }"
            :data="area_chart2.chartData_1" :options="horizontalChartOptions"
            :createChart="(el, google) => new google.charts.Bar(el)" @ready="onChartReady" />
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, computed } from 'vue'
import { GChart } from "vue-google-charts";
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
var secondary = localStorage.getItem('secondary_color') || "#48A3D7";
var primary = localStorage.getItem('primary_color') || "#7A70BA";
const chartsLib = ref(null)
const area_chart2 = {
    chartData_1: [
        ['Year', 'Sales', 'Expenses', 'Profit'],
        ['2014', 1e3, 400, 250],
        ['2015', 1170, 460, 300],
        ['2016', 660, 1120, 400],
        ['2017', 1030, 540, 450]
    ],
}
const verticalChartOptions = computed(() => {
    if (!chartsLib.value) return null;
    return chartsLib.value.charts.Bar.convertOptions({
        chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017'
        },
        bars: 'vertical',
        vAxis: {
            format: 'decimal'
        },
        height: 400,
        width: '100%',
        colors: [primary, secondary, "#61ae41"]
    });
})
const horizontalChartOptions = computed(() => {
    if (!chartsLib.value) return null;
    return chartsLib.value.charts.Bar.convertOptions({
        chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017'
        },
        bars: 'horizontal',
        vAxis: {
            format: 'decimal'
        },
        height: 400,
        width: '100%',
        colors: [primary, secondary, "#61ae41"]
    });
})
function onChartReady(chart: any, google: any) {
    chartsLib.value = google;
}
</script>