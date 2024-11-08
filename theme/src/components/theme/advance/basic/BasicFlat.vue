<template>
    <Card3 colClass="col-sm-12 col-xl-6" :cardClass="item.card" v-for="(item, index) in card" :key="index" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" :title="item.title" :desc="item.desc">
        <p class="mb-0" v-html="item.body"></p>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { card } from "@/core/data/advance"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Star rating is displayed using <code>#u-rating-fontawesome-o </code> id using javascript.")
</script>