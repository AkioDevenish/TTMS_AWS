<template>
    <Card3 colClass="col-xl-6 col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Individual Carousel-Item Interval" :desc="desc">
        <div class="carousel slide" id="carouselExampleInterval" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item" :class="item.active == true ? 'active' : ''" v-for="(item, index) in individual"
                    data-bs-interval="10000" :key="index"><img class="d-block w-100" :src="getImages(item.img)"
                        alt="drawing-room"></div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleInterval"
                data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span
                    class="visually-hidden">Previous</span></button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleInterval"
                data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span
                    class="visually-hidden">Next</span></button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { individual } from "@/core/data/owlcarousel"
import { getImages } from "@/composables/common/getImages"
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Add <code>data-bs-interval=''</code> to a<code> .carousel-item</code> to change the amount of time to delay between automatically cycling to the next item.")
</script>