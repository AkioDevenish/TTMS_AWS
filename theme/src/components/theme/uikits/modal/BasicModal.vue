<template>
    <Card3 colClass="col-lg-6" cardbodyClass="badge-spacing" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Basic modal" :desc="desc">

        <button class="btn " :class="item.class" v-for="(item, index) in basicmodal" :key="index" type="button"
            data-bs-toggle="modal" data-original-title="test" :data-bs-target="item.id">{{ item.title
            }}</button>
        <SimpleModel />
        <ScrollingModal />
        <TooltipsModal />
        <OpenModel />

    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { basicmodal } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const SimpleModel = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/SimpleModel.vue"))
const ScrollingModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/ScrollingModal.vue"))
const TooltipsModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/TooltipsModal.vue"))
const OpenModel = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/OpenModel.vue"))
let desc = ref<string>("Different types of basic modals using like <code>simple/scrolling/tooltips/grid/varying modal</code>.")
</script>
