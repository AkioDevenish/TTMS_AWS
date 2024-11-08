<template>
    <Card1 colClass="col-xl-6 col-lg-7 col-sm-12" dropdown="true" headerTitle="true" title="User by Continent"
        cardhaderClass="card-no-border pb-0" cardClass="overflow-hidden" cardbodyClass="user-continent pb-0">
        <div class="user-map-menu d-flex align-items-center gap-5">
            <div class="user-items">
                <h5>1,506<span>items</span></h5>
                <div class="progress">
                    <div class="progress-bar " :class="item.class" v-for="(item, index) in progresuser" :key="index"
                        role="progressbar" :style="{ 'width': item.width }" aria-valuenow="25" aria-valuemin="0"
                        aria-valuemax="100"></div>

                </div>
            </div>
            <div class="map-items">
                <ul class="d-flex align-items-center gap-3">
                    <li v-for="(items, index) in mapitems" :key="index">
                        <h5><span :class="items.class"></span>{{ items.title }}</h5>
                        <p class="mb-0">{{ items.number }}</p>
                    </li>
                </ul>
            </div>
        </div>
        <div class="contries-sale d-flex gap-4">
            <div class="map-value">
                <h5>All Over Contries's Sale</h5>
                <ul>
                    <li v-for="(datas, index) in contries" :key="index">
                        <div class="d-flex gap-2">
                            <div class="flex-shrink-0">
                                <svg>
                                    <use :class="datas.class"
                                        :xlink:href="require('@/assets/svg/icon-sprite.svg') + `#${datas.icon}`">
                                    </use>
                                </svg>
                            </div>
                            <div class="flex-grow-1">
                                <h6>{{ datas.title }}</h6>
                            </div><span>{{ datas.total }}%</span>
                        </div>
                    </li>

                </ul>
            </div>
            <div class="map">
                <div class="jvector-map-height" id="world-map2">
                    <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height: 220px">
                        <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />
                        <ol-tile-layer>
                            <ol-source-osm />
                        </ol-tile-layer>
                    </ol-map>
                </div>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { progresuser, mapitems, contries } from "@/core/data/dashboards"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

const center = ref<number[]>([40, 40]);
const projection = ref<string>("EPSG:4326");
const zoom = ref<number>(8);
const rotation = ref<number>(0);

</script>