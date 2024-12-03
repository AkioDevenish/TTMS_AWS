<template>
    <Card1 colClass="col-xl-3 col-sm-6" dropdown="true" headerTitle="true" titleClass="daily-revenue-card"
        title="Total Sells" cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 total-sells">
        <div class="d-flex align-items-center gap-3">
            <div class="flex-shrink-0"><img src="@/assets/images/dashboard-3/icon/coin1.png" alt="icon"></div>
            <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2">
                    <h2>{{ doller }}12,463</h2>
                    <div class="d-flex total-icon">
                        <p class="mb-0 up-arrow bg-light-success"><i class="fa fa-arrow-up text-success"></i></p><span
                            class="f-w-500 font-success">+ 20.08% </span>
                    </div>
                </div>
                <p class="text-truncate">Compared to Jan 2024</p>
            </div>
        </div>
        <div id="admissionRatio">
            <apexchart type="area" height="90" ref="chart" :options="chartOptions7" :series="series7">
            </apexchart>
        </div>
    </Card1>
    <Card1 colClass="col-xl-3 col-sm-6" dropdown="true" headerTitle="true" titleClass="daily-revenue-card"
        title="Orders Value" cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 total-sells-2">
        <div class="d-flex align-items-center gap-3">
            <div class="flex-shrink-0"><img src="@/assets/images/dashboard-3/icon/shopping1.png" alt="icon"></div>
            <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2">
                    <h2>{{ doller }}78,596</h2>
                    <div class="d-flex total-icon">
                        <p class="mb-0 up-arrow bg-light-danger"><i class="fa fa-arrow-up text-danger"></i></p><span
                            class="f-w-500 font-danger">- 10.02%</span>
                    </div>
                </div>
                <p class="text-truncate">Compared to Aug 2024</p>
            </div>
        </div>
        <div id="order-value">
            <apexchart type="area" height="90" ref="chart" :options="chartOptions8" :series="series8">
            </apexchart>
        </div>
    </Card1>

    <Card1 colClass="col-xl-3 col-sm-6" dropdown="true" headerTitle="true" titleClass="daily-revenue-card"
        title="Daily Orders" cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 total-sells-3">
        <div class="d-flex align-items-center gap-3">
            <div class="flex-shrink-0"><img src="@/assets/images/dashboard-3/icon/sent1.png" alt="icon"></div>
            <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2">
                    <h2>{{ doller }}95,789</h2>
                    <div class="d-flex total-icon">
                        <p class="mb-0 up-arrow bg-light-success"><i class="fa fa-arrow-up text-success"></i></p><span
                            class="f-w-500 font-success">+ 13.23%</span>
                    </div>
                </div>
                <p class="text-truncate">Compared to may 2024</p>
            </div>
        </div>
        <div id="daily-value">
            <apexchart type="area" height="90" ref="chart" :options="chartOptions9" :series="series9">
            </apexchart>
        </div>
    </Card1>

    <Card1 colClass="col-xl-3 col-sm-6" dropdown="true" headerTitle="true" titleClass="daily-revenue-card"
        title="Daily Revenue" cardhaderClass="card-no-border pb-0" cardbodyClass="pb-0 total-sells-4">
        <div class="d-flex align-items-center gap-3">
            <div class="flex-shrink-0"><img src="@/assets/images/dashboard-3/icon/revenue1.png" alt="icon"></div>
            <div class="flex-grow-1">
                <div class="d-flex align-items-center gap-2">
                    <h2>{{ doller }}41,954</h2>
                    <div class="d-flex total-icon">
                        <p class="mb-0 up-arrow bg-light-danger"><i class="fa fa-arrow-up text-danger"></i></p><span
                            class="f-w-500 font-danger">- 17.06%</span>
                    </div>
                </div>
                <p class="text-truncate">Compared to july 2024</p>
            </div>
        </div>
        <div id="daily-revenue">
            <apexchart type="area" height="90" ref="chart" :options="chartOptions10" :series="series10">
            </apexchart>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { series7, chartOptions7, series8, chartOptions8, series9, chartOptions9, series10, chartOptions10, } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
let props = defineProps({
    doller: String,
})
</script>