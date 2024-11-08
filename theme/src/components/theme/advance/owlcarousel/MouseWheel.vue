<template>
    <Card3 colClass="col-xl-6 col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Mouse Wheel Variant"
        :desc="desc">
        <swiper :slidesPerView="3" :spaceBetween="10" :mousewheel="true" :loop="true" :pagination="{
            clickable: true,
        }" :modules="modules" class="mySwiper">
            <swiper-slide v-for="(item, index) in autoplay" :key="index">
                <div><img :src="getImages(item.img)" class="img-fluid" alt="" style="object-fit:cover"></div>
            </swiper-slide>
        </swiper>
    </Card3>
</template>
<script lang="ts" setup>
import { autoplay } from "@/core/data/owlcarousel"
import { getImages } from "@/composables/common/getImages"
import { Swiper, SwiperSlide } from "swiper/vue";
import { Pagination, Autoplay, Mousewheel } from "swiper";
import "swiper/css";
import "swiper/css/pagination";
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.owl-carousel </code>through slides.")
let modules = [Pagination, Autoplay, Mousewheel]
</script>