<template>
    <Card3 colClass="col-12" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Mofi custom modals" :desc="desc">
        <div class="row g-3">
            <ProfileModal />
            <ResultModal />
            <BalanceModal />
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { badges } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const ProfileModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/ProfileModal.vue"))
const ResultModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/ResultModal.vue"))
const BalanceModal = defineAsyncComponent(() => import("@/components/theme/uikits/modal/modals/BalanceModal.vue"))
let desc = ref<string>("Custom Modal make by Mofi.")
</script>