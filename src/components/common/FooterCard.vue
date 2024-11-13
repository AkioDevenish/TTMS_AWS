<template>
    <Card3 :colClass="item.col" v-for="(item, index) in footer" :key="index" footer="true" :footerclass="item.footerclass"
        footersClass="text-end" :cardbodyClass="item.bodyclass" :titleClass="item.class" :cardhaderClass="item.haderclass"
        headerTitle="true" :title="item.title" footertitle="Mofi Theme">
        <h5 class="pb-2 f-w-600"> {{ item.bodytitle }} </h5>
        <p class="mb-0">{{ item.bodydesc }}</p>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { footer } from "@/core/data/advance"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Star rating is displayed using <code>#u-rating-fontawesome-o </code> id using javascript.")
</script>