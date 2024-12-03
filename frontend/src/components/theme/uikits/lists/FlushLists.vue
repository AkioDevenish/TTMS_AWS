<template>
    <Card3 colClass="col-xl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Flush lists"
        :desc="desc">
        <ul class="list-group list-group-flush">
            <li class="list-group-item" v-for="(item, index) in flushs" :key="index"><i class="icofont icofont-arrow-right">
                </i>{{ item.title }}</li>
        </ul>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { flushs } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use <code> .list-group-flush</code> to remove some borders and rounded corners to render list group items.")
</script>