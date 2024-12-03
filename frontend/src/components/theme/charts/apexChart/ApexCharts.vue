<template>
    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Basic Area Chart ">
        <div id="basic-apex">
            <apexchart type="area" height="350" ref="chart" :options="chartOptions" :series="series">
            </apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Area Spaline Chart  ">
        <div id="area-spaline">
            <apexchart type="area" height="350" ref="chart" :options="chartOptions1" :series="series1">
            </apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Bar chart">
        <div id="basic-bar">
            <apexchart type="bar" height="350" ref="chart" :options="chartOptions2" :series="series2">
            </apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Column Chart">
        <div id="column-chart">
            <apexchart type="bar" height="350" ref="chart" :options="chartOptions3" :series="series3">
            </apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="3d Bubble Chart">
        <div id="chart-bubble">
            <apexchart type="bubble" height="350" ref="chart" :options="chartOptions4" :series="series4"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Stepline Chart">
        <div id="stepline">
            <apexchart type="line" height="350" ref="chart" :options="chartOptions5" :series="series5">
            </apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-12 box-col-6" headerTitle="true" title="Column Chart">
        <div id="annotationchart">
            <apexchart type="line" height="350" ref="chart" :options="chartOptions7" :series="series7"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" cardbodyClass="apex-chart" headerTitle="true" title="Pie Chart">
        <div id="piechart">
            <apexchart width="380" type="pie" :options="chartOptions6" :series="series6"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" cardbodyClass=" apex-chart" headerTitle="true" title="Donut Chart">
        <div id="donutchart">
            <apexchart width="380" type="donut" :options="chartOptions8" :series="series8"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-12 box-col-12" headerTitle="true" title="Mixed Chart">
        <div id="mixedchart">
            <apexchart height="350" type="line" :options="chartOptions9" :series="series9"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-12 box-col-12" headerTitle="true" title="Candlestick Chart">
        <div id="candlestick">
            <apexchart height="350" type="candlestick" :options="chartOptions10" :series="series10"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Radar Chart">
        <div id="radarchart">
            <apexchart height="350" type="radar" :options="chartOptions11" :series="series11"></apexchart>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6 box-col-6" headerTitle="true" title="Radial Bar Chart">
        <div id="circlechart">
            <apexchart height="350" type="radialBar" :options="chartOptions12" :series="series12"></apexchart>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { series, chartOptions, series12, chartOptions12, series11, chartOptions11, series10, chartOptions10, series9, chartOptions9, series8, chartOptions8, series6, chartOptions6, series7, chartOptions7, series5, chartOptions5, series4, chartOptions4, series3, chartOptions3, series2, chartOptions2, series1, chartOptions1 } from "@/core/data/apex-chart"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
</script>