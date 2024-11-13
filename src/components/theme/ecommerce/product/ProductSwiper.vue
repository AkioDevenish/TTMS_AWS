<template>
    <div>
        <swiper :slidesPerView="1" :spaceBetween="5" :loop="true">
            <swiper-slide>
                <div class="item w-100">

                    <div class="product-box row mb-2" v-for="(product, index) in data.slice(0, 3)" :key="index">

                        <div class="product-img col-md-3">
                            <img class="img-fluid img-100 media" :src='getImages(product.images[0])' alt="">
                        </div>

                        <div class="product-details col-md-5 text-start">
                            <span>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning"></i>
                            </span>
                            <router-link :to="'/ecommerce/details/' + product.sku">
                                <p class="mb-0">{{ product.name }}</p>
                            </router-link>
                            <div class="product-price">${{ product.price }}</div>
                        </div>
                    </div>
                </div>
            </swiper-slide>
            <swiper-slide>
                <div class="item">
                    <div class="product-box row mb-2" v-for="(product, index) in data.slice(3, 6)" :key="index">

                        <div class="product-img col-md-3">
                            <img class="img-fluid img-100 media" :src='getImages(product.images[0])' alt="">
                        </div>
                        <div class="product-details col-md-5 text-start">
                            <span>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning me-1"></i>
                                <i class="fa fa-star font-warning"></i>
                            </span>
                            <router-link :to="'/ecommerce/details/' + product.sku">
                                <p class="mb-0">{{ product.name }}</p>
                            </router-link>
                            <div class="product-price">${{ product.price }}</div>
                        </div>
                    </div>
                </div>
            </swiper-slide>
        </swiper>
    </div>
</template>
<script lang="ts" setup>
import { useProductsStore } from "@/store/products"
import { data } from "@/core/data/products"
import { getImages } from "@/composables/common/getImages"
import { Swiper, SwiperSlide } from "swiper/vue";
import "swiper/css";
const swiperOptions = {
    breakpoints: {
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        }
    }
}

</script>