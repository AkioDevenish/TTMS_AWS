<template>
    <div class="col-lg-12">
        <div class="header-faq">
            <h4 class="mb-0">Featured Tutorials</h4>
        </div>
        <div class="row">
            <div class="col-xl-3 xl-50 col-md-6 box-col-6" v-for="(item, index) in featured" :key="index">
                <div class="card features-faq product-box">
                    <div class="faq-image product-img"><img class="img-fluid" :src="getImages(item.imge)" alt="">
                        <div class="product-hover">
                            <ul>
                                <li><i class="icon-link"></i></li>
                                <li><i class="icon-import"></i></li>
                            </ul>
                        </div>
                    </div>
                    <div class="card-body">
                        <h5 class="f-w-600"> {{ item.title }}</h5>
                        <p>{{ item.desc }}</p>
                    </div>
                    <div class="card-footer"><span>{{ item.date }}</span><span class="pull-right"
                            v-html="stars(item.star)"></span></div>
                </div>
            </div>

        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
import { getImages } from "@/composables/common/getImages"
import { featured } from "@/core/data/knowledgebase"
function stars(count: number) {
    var stars = '';

    for (var i = 0; i < 5; i++) {
        if (count > i) {
            stars = stars + '<i class="fa fa-star font-primary"></i>';
        } else {
            stars = stars + '<i class="fa fa-star-o font-primary"></i>';
        }
    }

    return stars;
}
</script>