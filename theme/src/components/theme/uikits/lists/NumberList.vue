<template>
    <Card3 colClass="col-xl-4 col-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Lists with numbers"
        :desc="desc">
        <ol class="list-group list-group-numbered">
            <li class="list-group-item  fw-bold" :class="item.class" v-for="(item, index) in numbers" :key="index">
                {{ item.title }}</li>
        </ol>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { numbers } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.list-group-numbered</code> to ordered wise print numbers.")
</script>