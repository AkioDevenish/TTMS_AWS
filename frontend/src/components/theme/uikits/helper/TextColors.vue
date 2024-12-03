<template>
    <Card3 colClass="col-12" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Font sizes" :desc="desc">
        <div class="gradient-border">
            <div class="font-wrapper border" v-for="(item, index) in fontsize" :key="index">
                <div :class="item.class">Font-size .{{ item.class }}</div>
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { fontsize } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the font-size for <code>.f-* [14/16/18/20/22/24/26/28/30/32/34/36/38/40]</code>.")
</script>