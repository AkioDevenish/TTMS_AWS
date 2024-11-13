<template>
    <div class="col-xxl-5 box-col-6 order-xxl-0 order-1">
        <div class="card">
            <div class="card-body">
                <div class="product-page-details">
                    <h3 class="f-w-600">{{ products.name }}</h3>
                </div>
                <div class="product-price"> ${{ products.price }}
                    <del>${{ products.salePrice }}</del>
                </div>
                <ul class="product-color">
                    <li class="bg-primary"></li>
                    <li class="bg-secondary"></li>
                    <li class="bg-success"></li>
                    <li class="bg-info"></li>
                    <li class="bg-warning"></li>
                </ul>
                <hr>
                <p>{{ products.description }}</p>
                <hr>
                <StockView />
                <hr>
                <div class="row">
                    <div class="col-md-4">
                        <h5 class="f-w-600 product-title">share it</h5>
                    </div>
                    <div class="col-md-8">
                        <div class="product-icon">
                            <ul class="product-social">
                                <li class="d-inline-block" v-for="(item, index) in social" :key="index"><a :href="item.link"
                                        target="_blank"><i class="fa " :class="item.icon"></i></a></li>
                            </ul>
                            <form class="d-inline-block f-right"></form>
                        </div>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-md-4">
                        <h5 class="f-w-600 product-title">Rate Now</h5>
                    </div>
                    <div class="col-md-8">
                        <div class="d-flex align-items-center">
                            <rate :length="5" :value="2" /><span>(250 review)</span>
                        </div>
                    </div>
                </div>
                <hr>
                <div class="m-t-15 btn-showcase"><router-link :to="'/ecommerce/cart'" class="btn btn-primary"
                        @click="addToCart(products)"> <i class="fa fa-shopping-basket me-2"></i>Add To
                        Cart</router-link>
                    <router-link class="btn btn-success" to='/ecommerce/cart' @click="addToCart(products)"><i
                            class="fa fa-shopping-cart me-2"></i>Buy Now</router-link>
                    <router-link :to="'/ecommerce/wishList'" class="btn btn-secondary"><i class="fa fa-heart me-2"></i>Add
                        To WishList</router-link>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from 'vue-router'
import { defineAsyncComponent } from 'vue';
import { social } from "@/core/data/ecommerce"
const StockView = defineAsyncComponent(() => import("@/components/theme/ecommerce/productpage/StockView.vue"))
import { useProductsStore } from "@/store/products"
let store = useProductsStore()
let router = useRouter()
let thumbsSwiper = ref(null)
const products: any = store.datas.find((item) => {
    if (parseInt(router.currentRoute._rawValue.params.id) === item.sku) return item;

})

function addToCart(product: object,) {

    store.addToCart(product);
}
</script>