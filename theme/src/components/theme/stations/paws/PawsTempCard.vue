<template>
    <div>
        <div class="row g-2">
            <div class="col-xl-3 col-md-6 proorder-xl-3 proorder-md-3" v-for="(item, index) in paws_data" :key="index">
                <Card1 :cardbodyClass="item.cardclass">
                    <div class="d-flex gap-2 align-items-end">
                        <div class="flex-grow-1">
                            <h2>{{ item.number }}</h2>
                            <p class="mb-0 text-truncate">{{ item.text }}</p>
                            <div class="d-flex student-arrow text-truncate">
                                <p class="mb-0 up-arrow " :class="item.iconclass"><i :class="item.icon"></i></p>
                                <span class="f-w-500 " :class="item.fontclass">{{ item.total }}%</span>{{ item.month }}
                            </div>
                        </div>
                        <div class="flex-shrink-0"><img :src="getImages(item.img)" alt="">
                        </div>
                    </div>
                </Card1>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { paws_data } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>