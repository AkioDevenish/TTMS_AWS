<template>
    <Card1 colClass="col-xl-6 col-lg-12" cardbodyClass="product-slider ">
        <div class="row align-items-center">
            <div class="col-sm-6">
                <div class="product-page-main p-0">
                    <div class="row align-items-center">
                        <div class="col-4 product-thumbnail">
                            <div class="pro-slide-right">
                                <Swiper direction="vertical" :slidesPerView="3" :loop="true" @swiper="setThumbsSwiper"
                                    :spaceBetween="10" :centeredSlides="true" :modules="modules"
                                    class="vertical-box-slider">
                                    <Swiper-slide class="mt-4" v-for="(products, index) in slide" :key="index">
                                        <div class="slide-box"><img class="img-fluid" :src="getImages(products.img)" alt="">
                                        </div>
                                    </Swiper-slide>
                                </Swiper>
                            </div>
                        </div>
                        <div class="col-8 px-0 product-main">
                            <div class="pro-slide-single">
                                <Swiper :slidesPerView="1" :loop="true" :thumbs="{ swiper: thumbsSwiper }"
                                    :spaceBetween="30" :centeredSlides="true" :modules="modules" class="mySwiper">
                                    <Swiper-slide v-for="(product, index) in proslide" :key="index">
                                        <div> <img class="img-fluid" :src="getImages(product.img)" alt="">
                                        </div>
                                    </Swiper-slide>
                                </Swiper>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-6">
                <div class="product-details my-4"><router-link to="/ecommerce/details/1">
                        <h4 class="text-truncate">Women’s Fit and Flare Knee length one Piece Dress </h4>
                    </router-link>
                    <h3 class="font-primary">$126</h3>
                    <h5>Select size:</h5>
                    <ul class="product-size">
                        <li>S </li>
                        <li>M </li>
                        <li>L </li>
                        <li>XL</li>
                    </ul>
                    <h5>Colour:</h5>
                    <ul class="product-color">
                        <li class="border-primary"><span class="bg-primary"> <i class="icon-check"></i></span></li>
                        <li class="border-secondary"><span class="bg-secondary"> </span></li>
                        <li class="border-warning"><span class="bg-warning"> </span></li>
                        <li class="border-tertiary"><span class="bg-tertiary"></span></li>
                    </ul>
                    <div class="discount-box">
                        <h6>Special Discount </h6>
                    </div>
                    <h3 class="text-truncate">Deal of the Day From <span class="font-secondary">$48 </span></h3>
                    <div class="countdown" id="clock-arrival" data-hours="1" data-minutes="2" data-seconds="3">
                        <TimerView />
                    </div>
                </div>
            </div>
        </div>
    </Card1>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
import { slide, proslide } from "@/core/data/dashboards"
import { getImages } from "@/composables/common/getImages"
import { Swiper, SwiperSlide } from "swiper/vue";
import { Autoplay, FreeMode, Navigation, Thumbs } from "swiper";
import "swiper/css/free-mode";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/thumbs"
const Card1 = defineAsyncComponent(() => import("@/components/common/card/CardData1.vue"))
const TimerView = defineAsyncComponent(() => import("@/components/common/TimerView.vue"))

const thumbsSwiper = ref()
const setThumbsSwiper = (swiper: string) => {
    thumbsSwiper.value = swiper;
}
const modules = [Autoplay, Navigation, FreeMode, Thumbs]
let swiperOptions = {

}
</script>