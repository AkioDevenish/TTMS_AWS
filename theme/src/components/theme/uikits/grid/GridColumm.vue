<template>
    <Card3 colClass="col-sm-12" cardbodyClass="grid-showcase" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Grid for column" :desc="desc">
        <div class="row">
            <div class=" text-center" :class="item.class" v-for="(item, index) in columm" :key="index">
                <span>{{ item.class }}</span></div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { columm } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("You may use predefined grid classes. Using <code>.col-md-* </code>you can set the grid system..")
</script>