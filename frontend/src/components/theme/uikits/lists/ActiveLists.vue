<template>
    <Card3 colClass="col-xl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Active lists"
        :desc="desc">
        <ul class="list-group">
            <li class="list-group-item " :class="item.class" v-for="(item, index) in active" :key="index"
                aria-current="true">
                <i class="icofont icofont-arrow-right"> </i>{{ item.title }}
            </li>
        </ul>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { active } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use<code>.active </code>to a<code>.list-group-item</code> to indicate the current active.")
</script>