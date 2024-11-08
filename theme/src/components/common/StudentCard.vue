<template>
    <div class="col-xl-6 col-md-12 proorder-md-1">
        <div class="row">

            <Card1 colClass="col-xl-6 col-sm-6" v-for="(item, index) in studentdata" :key="index"
                :cardbodyClass="item.cardclass">
                <div class="d-flex gap-2 align-items-end">
                    <div class="flex-grow-1">
                        <h2>{{ item.number }}</h2>
                        <p class="mb-0 text-truncate"> {{ item.text }}</p>
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
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { studentdata } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))

</script>