<template>
    <Card3 colClass="container invoice-2">
        <InvoicePageFive />
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const InvoicePageFive = defineAsyncComponent(() => import("@/components/theme/ecommerce/invoice/invoice5/InvoicePageFive.vue"))
</script>