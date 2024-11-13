<template>
    <Card3 colClass="col-xl-6 col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="With Indicators"
        :desc="desc">
        <div class="carousel slide" id="carouselExampleIndicators" data-bs-ride="true">
            <div class="carousel-indicators">
                <button class="active" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0"
                    aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1"
                    aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2"
                    aria-label="Slide 3"></button>
            </div>
            <div class="carousel-inner">
                <div class="carousel-item" :class="item.active == true ? 'active' : ''" v-for="(item, index) in indicators"
                    :key="index"><img class="d-block w-100" :src="getImages(item.img)" alt="drawing-room"></div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span
                    class="visually-hidden">Previous</span></button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators"
                data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span
                    class="visually-hidden">Next</span></button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { indicators } from "@/core/data/owlcarousel"
import { getImages } from "@/composables/common/getImages"
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.carousel-indicators</code> through carousel indicates.")
</script>