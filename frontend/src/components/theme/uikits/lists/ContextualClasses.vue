<template>
    <Card3 colClass="col-xxl-6 col-sm-12 box-col-12" cardClass="height-equal" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Contextual classes" :desc="desc">
        <div class="list-group"><a class="list-group-item list-group-item-action " :class="item.class"
                v-for="(item, index) in contextual" :key="index" href="#">This
                is {{ item.color }} bg you can use <em class=" f-w-800" :class="item.txt">{{ item.title }}</em>
                class.</a></div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { contextual } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use contextual classes to style list items with a stateful background and color.<code>.list-light-*</code> and <code>txt-*</code>.<")
</script>