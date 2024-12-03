<template>
     <Card3 colClass="col-xxl-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Pagination Alignment"
        :desc="desc">
        <nav aria-label="Page navigation example">
            <ul class="pagination " :class="items.class" v-for="(items, index) in alignment" :key="index">
                <li class="page-item" :class="item.active" v-for="(item, index) in items.children" :key="index"><a
                        class="page-link" href="javascript:void(0)">{{ item.title }}</a></li>

            </ul>
        </nav>
     </Card3>
</template>
<script lang="ts" setup>
import {alignment } from "@/core/data/advance"
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Change the alignment of pagination components with flexbox utilities. For example, with <code>.justify-content-center:</code>.")

</script>