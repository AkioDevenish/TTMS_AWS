<template>
    <Card1 colClass="col-xl-3 col-sm-6" cardClass="social-widget">
        <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-2">
                <div class="social-icons"><img src="@/assets/images/dashboard/social/1.png" alt="facebook icon"></div><span
                    class="f-w-600">Facebook</span>
            </div><span class="font-success f-12 d-xxl-block d-xl-none">+22.9%</span>
        </div>
        <div class="social-content">
            <div>
                <h5 class="mb-1">12,098</h5><span class="f-light">Followers</span>
            </div>
            <div class="social-chart">
                <div id="radial-facebook">
                    <apexchart type="radialBar" height="110" ref="chart" :options="chartOptions1" :series="series1">
                    </apexchart>
                </div>
            </div>
        </div>
    </Card1>

    <Card1 colClass="col-xl-3 col-sm-6" cardClass="social-widget">
        <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-2">
                <div class="social-icons"><img src="@/assets/images/dashboard/social/3.png" alt="twitter icon"></div><span
                    class="f-w-600">Twitter</span>
            </div><span class="font-success f-12 d-xxl-block d-xl-none">+14.09%</span>
        </div>
        <div class="social-content">
            <div>
                <h5 class="mb-1">12,564</h5><span class="f-light">Followers</span>
            </div>
            <div class="social-chart">
                <div id="radial-twitter">
                    <apexchart type="radialBar" height="110" ref="chart" :options="chartOptions3" :series="series3">
                    </apexchart>
                </div>
            </div>
        </div>
    </Card1>
    <Card1 colClass="col-xl-3 col-sm-6" cardClass="social-widget">
        <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-2">
                <div class="social-icons"><img src="@/assets/images/dashboard/social/2.png" alt="instagram icon"></div><span
                    class="f-w-600">Instagram</span>
            </div><span class="font-success f-12 d-xxl-block d-xl-none">+27.4%</span>
        </div>
        <div class="social-content">
            <div>
                <h5 class="mb-1">15,080</h5><span class="f-light">Followers</span>
            </div>
            <div class="social-chart">
                <div id="radial-instagram">
                    <apexchart type="radialBar" height="110" ref="chart" :options="chartOptions2" :series="series2">
                    </apexchart>
                </div>
            </div>
        </div>
    </Card1>
    <Card1 colClass="col-xl-3 col-sm-6" cardClass="social-widget">
        <div class="d-flex align-items-center justify-content-between">
            <div class="d-flex align-items-center gap-2">
                <div class="social-icons"><img src="@/assets/images/dashboard/social/4.png" alt="you tube icon"></div><span
                    class="f-w-600">Youtube</span>
            </div><span class="font-success f-12 d-xxl-block d-xl-none">+22.9%</span>
        </div>
        <div class="social-content">
            <div>
                <h5 class="mb-1">68,954</h5><span class="f-light">Followers</span>
            </div>
            <div class="social-chart">
                <div id="radial-youtube">
                    <apexchart type="radialBar" height="110" ref="chart" :options="chartOptions4" :series="series4">
                    </apexchart>
                </div>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
import { series1, chartOptions1, series2, chartOptions2, series3, chartOptions3, series4, chartOptions4, } from "@/core/data/widgets-chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
</script>