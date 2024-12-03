<template>
    <div class="row">
        <Card2 colClass="col-lg-4 col-md-6 box-col-4" cardClass="o-hidden" chart="true" title="Total Sale" price="$3654.00"
            desc="Compare to last month" total="+65%">
            <apexchart type="area" height="200" ref="chart" :options="chartOptions5" :series="series5">
            </apexchart>
        </Card2>
        <Card2 colClass="col-lg-4 col-md-6 box-col-4" cardClass="o-hidden" chart="true" title="Total Project" price="12569"
            desc="Compare to last month" total="+65%">
            <apexchart type="area" height="200" ref="chart" :options="chartOptions6" :series="series6">
            </apexchart>
        </Card2>
        <Card2 colClass="col-lg-4 col-md-6 box-col-4" cardClass="o-hidden" chart="true" title="Total Product" price="93M"
            desc="Compare to last month" total="+65%">
            <apexchart type="area" height="200" ref="chart" :options="chartOptions7" :series="series7">
            </apexchart>
        </Card2>
    </div>
    <div class="row">
        <Card2 colClass="col-md-12 box-col-12" cardClass="o-hidden" charts="true" title="Monthly  History">
            <div class="row">
                <div class="col-12">
                    <apexchart type="bar" height="380" ref="chart" :options="chartOptions8" :series="series8">
                    </apexchart>
                </div>
            </div>
        </Card2>
        <Card3 colClass="col-xl-6 col-lg-12 box-col-6 xl-50" headerTitle="true" title="Skill Status">
            <div class="chart-container skill-chart">
                <apexchart type="radialBar" height="375" ref="chart" :options="chartOptions9" :series="series9">
                </apexchart>
            </div>
        </Card3>
        <Card3 colClass="col-xl-6 col-lg-12 box-col-6 xl-50" headerTop="true" dropdown="true" title="Order Status">
            <OrderStatus />
        </Card3>
    </div>
    <div class="row">
        <Card2 colClass="xl-50 col-xl-7 col-lg-12" headerTitle="true" title="Live Products"
            smallClass="small-chart-widget chart-widgets-small">
            <apexchart type="area" height="320" ref="chart" :options="chartOptions15" :series="series15">
            </apexchart>
        </Card2>
        <Card2 colClass="xl-50 col-xl-5 col-lg-12" headerTitle="true" title="Turn over">
            <apexchart type="area" height="300" ref="chart" :options="chartOptions16" :series="series16">
            </apexchart>
        </Card2>
        <Card2 colClass="xl-50 col-xl-6 col-lg-12" headerTitle="true" title="Cryptocurrency Prices" contain="crypto-chart">
            <apexchart type="area" height="400" ref="chart" :options="chartOptions17" :series="series17">
            </apexchart>
        </Card2>
        <Card2 colClass="xl-50 col-xl-6 col-lg-12" headerTitle="true" title="Crypto Annotations">
            <apexchart type="line" height="400" ref="chart" :options="chartOptions18" :series="series18">
            </apexchart>
        </Card2>
    </div>
    <div class="row">
        <Card3 colClass="col-sm-12 box-col-12" headerTitle="true" title="Stock Market" smallClass="donut-chart-widget">
            <apexchart type="line" height="450" ref="chart" :options="chartOptions19" :series="series19">
            </apexchart>
        </Card3>
        <Card3 colClass="col-xl-5 col-lg-12 box-col-12" headerTitle="true" title="Finance">
            <div class="chart-container column-container">
                <apexchart type="line" height="350" ref="chart" :options="chartOptions20" :series="series20">
                </apexchart>
            </div>
        </Card3>
        <Card3 colClass="col-xl-7 col-lg-12 box-col-6" headerTitle="true" title="Order Status">
            <div class="chart-container">
                <apexchart type="line" height="350" ref="chart" :options="chartOptions21" :series="series21">
                </apexchart>
            </div>
        </Card3>
        <Card2 colClass="xl-50 col-xl-5 col-lg-12 box-col-6" headerTitle="true" title="Monthly Sales"
            smallClass="small-chart-widget chart-widgets-small">
            <apexchart type="radar" height=" 300" ref="chart" :options="chartOptions22" :series="series22">
            </apexchart>
        </Card2>
        <Card2 colClass="xl-50 col-xl-7 col-lg-12 box-col-12" headerTitle="true" title="Uses"
            smallClass="small-chart-widget chart-widgets-small">
            <apexchart type="bubble" height="320" ref="chart" :options="chartOptions23" :series="series23">
            </apexchart>
        </Card2>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { series19, chartOptions19, series20, chartOptions20, series21, chartOptions21, series22, chartOptions22, series23, chartOptions23, series17, chartOptions17, series18, chartOptions18, series16, chartOptions16, series9, chartOptions9, series5, chartOptions5, series6, chartOptions6, series7, chartOptions7, series8, chartOptions8, series15, chartOptions15 } from "@/core/data/widgets-chart"
const Card2 = defineAsyncComponent(() => import("@/components/common/card/CardData2.vue"))
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const OrderStatus = defineAsyncComponent(() => import("@/components/theme/widgets/chart/OrderStatus.vue"))
</script>