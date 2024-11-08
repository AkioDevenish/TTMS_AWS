<template>
    <Card3 colClass="col-12" cardbodyClass="d-flex flex-column gap-3" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Font weight" :desc="desc">
        <div v-for="(item, index) in weight" :key="index" v-html="item.font">
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { weight } from "@/core/data/uikits"

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Using <code>f-w-*</code> class, you can change the font weight.")
</script>