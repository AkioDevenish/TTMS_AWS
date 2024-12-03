<template>
    <div class="container-fluid">
        <div class="row">
            <BasicFlat />
            <ShadowCard />
            <IconCard />
            <DarkCard />
            <FooterCard />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const BasicFlat = defineAsyncComponent(() => import("@/components/theme/advance/basic/BasicFlat.vue"))
const ShadowCard = defineAsyncComponent(() => import("@/components/theme/advance/basic/ShadowCard.vue"))
const IconCard = defineAsyncComponent(() => import("@/components/theme/advance/basic/IconCard.vue"))
const DarkCard = defineAsyncComponent(() => import("@/components/theme/advance/basic/DarkCard.vue"))
const FooterCard = defineAsyncComponent(() => import("@/components/common/FooterCard.vue"))
</script>