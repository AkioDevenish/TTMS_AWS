<template>
    <div :class="colClass">
        <div class="card " :class="cardClass" v-if="chart">
            <div class="chart-widget-top">
                <div class="row card-body pb-0 m-0">
                    <div class="col-xl-9 col-lg-8 col-9 p-0">
                        <h5 class="f-w-600 mb-2">{{ title }}</h5>
                        <h4>{{ price }}</h4><span>{{ desc }}</span>
                    </div>
                    <div class="col-xl-3 col-lg-4 col-3 text-end p-0">
                        <h6 class="txt-success">{{ total }}</h6>
                    </div>
                </div>
                <slot />
            </div>
        </div>
        <div class="card " :class="cardClass" v-if="charts">
            <div class="card-header">
                <h4>{{ title }}</h4>
            </div>
            <div class="bar-chart-widget">
                <div class="bottom-content card-body">

                    <slot />
                </div>
            </div>
        </div>
        <div class="card" :class="cardClass" v-if="headerTitle">
            <div :class="smallClass">
                <div class="card-header" :class="cardhaderClass">
                    <h4>{{ title }}</h4>
                </div>
                <div class="card-body" :class="cardbodyClass">
                    <div class="chart-container" :class="contain">
                        <div class="row">
                            <div class="col-12">
                                <slot />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
let props = defineProps({
    title: String,
    cardClass: String,
    colClass: String,
    cardbodyClass: String,
    cardhaderClass: String,
    headerTitle: String,
    dropdown: String,
    location: String,
    titleClass: String,
    meet: String,
    headerCard: String,
    chart: String,
    price: String,
    desc: String,
    total: String,
    charts: String,
    smallClass: String,
    contain: String
})
</script>