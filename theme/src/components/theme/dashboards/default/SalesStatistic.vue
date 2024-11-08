<template>
    <Card1 colClass="col-xxl-12 col-xl-12 box-col-12 proorder-xl-8 proorder-md-9" dropdown="true" headerTitle="true"
        title="ATMOS" cardhaderClass="card-no-border pb-0" cardbodyClass="sale-statistic">

        <div class="row">
            <div class="col-3 statistic-icon" v-for="(item, index) in sale" :key="index">
                <div class="light-card balance-card widget-hover">
                    <div class="icon-box"><img :src="getImages(item.img)" alt=""></div>
                    <div> <span class="f-w-500 f-light">{{ item.title }}</span>
                        <h5 class="mt-1 mb-0">{{ item.num }}</h5>
                    </div>
                    <div class="ms-auto text-end">
                        <div class="dropdown icon-dropdown">
                            <button class="btn dropdown-toggle" id="incomedropdown" type="button" data-bs-toggle="dropdown"
                                aria-expanded="false"><i class="icon-more-alt"></i></button>
                            <div class="dropdown-menu dropdown-menu-end" aria-labelledby="incomedropdown"><a
                                    class="dropdown-item" href="#">Today</a><a class="dropdown-item" href="#">Tomorrow</a><a
                                    class="dropdown-item" href="#">Yesterday </a></div>
                        </div><span class="f-w-600 " :class="item.fontclass">{{ item.total }}</span>
                    </div>
                </div>
            </div>

        </div>
        <div id="chart-dash-2-line">
            <apexchart type="line" height="270" ref="chart" :options="chartOptions3" :series="series3">
            </apexchart>
        </div>

    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { sale } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
import { series3, chartOptions3 } from "@/core/data/chart"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>