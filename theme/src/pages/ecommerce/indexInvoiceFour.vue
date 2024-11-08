<template>
    <Card3 colClass="container invoice-2">
        <InvoicePageFour />
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const InvoicePageFour = defineAsyncComponent(() => import("@/components/theme/ecommerce/invoice/invoice4/InvoicePageFour.vue"))
</script>