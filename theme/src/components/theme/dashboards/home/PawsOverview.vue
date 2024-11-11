<template>
    <Card1 colClass="col-xl-6 col-md-6 proorder-xl-3 proorder-md-3"  location="true" headerTitle="true"
        title="3DPaws - T01 Rawin" cardClass="shifts-char-box" cardhaderClass="card-no-border pb-0">

        <div class="row">
            <div class="col-5">
                <div class="overview" id="shifts-overview">
                    <apexchart type="donut" height="200" :options="pawsoption" :series="pawsseries">
                    </apexchart>
                </div>
            </div>
            <div class="col-7 shifts-overview">
                <div class="d-flex gap-2" v-for="(item, index) in pawsoverview" :key="index">
                    <div class="flex-shrink-0"><span :class="item.bg"> </span></div>
                    <div class="flex-grow-1">
                        <h6>{{ item.title }}</h6>
                    </div><span>{{ item.number }}</span>
                </div>

            </div>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { pawsoption, pawsseries } from "@/core/data/chart"
import { pawsoverview } from "@/core/data/dashboards"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))


</script>