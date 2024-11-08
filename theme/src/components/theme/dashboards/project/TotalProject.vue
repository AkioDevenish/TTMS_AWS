<template>
    <Card1 colClass="col-xl-4 col-xl-50 col-md-6 proorder-md-2" dropdown="true" headerTitle="true" title="Total Project"
        cardhaderClass="card-no-border pb-0" cardbodyClass="total-project">

        <h5 class="f-w-500">Currently Running<span class="px-2 f-w-500 font-primary">28 Projects</span></h5>
        <div id="total-project">
            <apexchart type="bar" height="220" ref="chart" :options="chartOptions4" :series="series4">
            </apexchart>
        </div>
        <ul>
            <li class="d-flex align-items-center gap-2" v-for="(item, index) in totalproject" :key="index"> <span
                    :class="item.bgclass"></span>
                <p>{{ item.title }}</p>
            </li>
        </ul>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { totalproject } from "@/core/data/dashboards"
import { series4, chartOptions4 } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>