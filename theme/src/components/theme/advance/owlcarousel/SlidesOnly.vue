<template>
    <Card3 colClass="col-xl-6 col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Slides Only"
        :desc="desc">
        <div class="carousel slide" id="carouselExampleSlidesOnly" data-bs-ride="carousel">
            <div class="carousel-inner">
                <div class="carousel-item" :class="item.active == true ? 'active' : ''" v-for="(item, index) in slidesonly"
                    :key="index"><img class="d-block w-100" :src="getImages(item.img)" alt="drawing-room"></div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { slidesonly } from "@/core/data/owlcarousel"
import { getImages } from "@/composables/common/getImages"
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("The <code>.active</code> class needs to be added to one of the slides otherwise the carousel will not be visible.<code>.d-block</code> and <code>.w-100 </code> on carousel images to prevent browser default image alignment.")
</script>