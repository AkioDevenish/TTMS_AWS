<template>
    <Card3 colClass="col-xxl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Badges Scrollbar"
        :desc="desc">
        <perfect-scrollbar class="vertical-scroll scroll-demo scroll-b-none" :settings="settings2">
            <ol class="list-group list-group-numbered scroll-rtl">
                <li class="list-group-item d-flex align-items-start flex-wrap" v-for="(item, index) in Badges" :key="index">
                    <div class="ms-2 me-auto">{{ item.title }}</div><span :class="item.badge">{{ item.span }}</span>
                </li>
            </ol>
        </perfect-scrollbar>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from "vue"
import { Badges } from "@/core/data/scrollable"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the<code>.badge </code> class through create more badges and <code>.vertical-scroll </code>used as vertical scroll.")
const settings2 = {
    maxScrollbarLength: 60,
    suppressScrollY: true,
    suppressScrollX: false
}
</script>