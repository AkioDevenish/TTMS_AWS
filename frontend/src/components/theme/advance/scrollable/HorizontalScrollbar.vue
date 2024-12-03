<template>
    <Card3 colClass="col-xl-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Horizontal Scrollbar"
        :desc="desc">
        <perfect-scrollbar class="horizontal-scroll scroll-demo" :settings="settings6">
            <div class="horz-scroll-content">
                <div class="row">
                    <div class="col-2" v-for="(item, index) in horizontal" :key="index">
                        <div class="horizontal-img"><img class="img-fluid" :src="getImages(item.img)" alt="girl">
                        </div>
                    </div>
                </div>
            </div>
        </perfect-scrollbar>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from "vue"
import { horizontal } from "@/core/data/scrollable"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.horizontal-scroll </code>through move content horizontally.")
const settings6 = {
    maxScrollbarLength: 60,
    suppressScrollY: true,
    suppressScrollX: false
}
</script>