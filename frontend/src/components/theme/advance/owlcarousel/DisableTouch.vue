<template>
    <Card3 colClass="col-xl-6 col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Disable Touch Swiping"
        :desc="desc">
        <div class="carousel slide" id="carouselExampleControlsNoTouching" data-bs-touch="false">
            <div class="carousel-inner">
                <div class="carousel-item" :class="item.active == true ? 'active' : ''" v-for="(item, index) in disable"
                    :key="index"><img class="d-block w-100" :src="getImages(item.img)" alt="drawing-room"></div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControlsNoTouching"
                data-bs-slide="prev"><span class="carousel-control-prev-icon" aria-hidden="true"></span><span
                    class="visually-hidden">Previous</span></button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControlsNoTouching"
                data-bs-slide="next"><span class="carousel-control-next-icon" aria-hidden="true"></span><span
                    class="visually-hidden">Next</span></button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { disable } from "@/core/data/owlcarousel"
import { getImages } from "@/composables/common/getImages"
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Carousels support swiping left/right on touchscreen devices to move between slides. This can be disabled using the <code>data-bs-touch </code> attribute.")
</script>
