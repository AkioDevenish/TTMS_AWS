<template>
    <Card3 colClass="col-md-6" cardClass="height-equal" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Ratio" :desc="desc">
        <div class="avatar-showcase">
            <div class="avatars">
                <div class="avatar ratio" v-for="(item, index) in ratio" :key="index"><img class="b-r-8 "
                        :class="item.class" :src="getImages(item.img)" alt="#"></div>

            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { ratio } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Give the shape to avatar using <code>.ratio</code> and <code> img-* (50/70/80/90/100)</code> class.")
</script>