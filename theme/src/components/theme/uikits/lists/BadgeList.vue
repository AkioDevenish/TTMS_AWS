<template>
    <Card3 colClass="col-xxl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Numbered & badge lists" :desc="desc">
        <ol class="list-group list-group-numbered badge-list">
            <li class="list-group-item d-flex justify-content-between align-items-start flex-wrap"
                v-for="(item, index) in badge" :key="index">
                <div class="ms-2 me-auto">{{ item.title }}</div><span class="badge  rounded-pill p-2" :class="item.class">{{
                    item.badge }}</span>
            </li>
        </ol>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { badge } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the<code> .list-group-numbered</code> modifier class to  numbered list group items.Numbers are generated via CSS for better placement inside list group items.")
</script>