<template>
    <Card3 colClass="col-lg-6" cardbodyClass="badge-spacing" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Sizes modal" :desc="desc">
        <div class="btn " :class="item.class" v-for="(item, index) in sizemodal" :key="index" data-bs-toggle="modal"
            :data-bs-target="item.id">{{ item.title }}</div>
        <FullsereenModa />
        <ExtralargeModal />
        <LargeModal />
        <SmallModal />
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { sizemodal } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const FullsereenModa = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/FullsereenModa.vue"))
const ExtralargeModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/ExtralargeModal.vue"))
const LargeModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/LargeModal.vue"))
const SmallModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/SmallModal.vue"))
let desc = ref<string>("Modals have three optional sizes, available via modifier classes to be placed on a <code>.modal-dialog</code>")
</script>