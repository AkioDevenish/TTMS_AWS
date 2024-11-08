<template>
    <Card3 colClass="container" cardClass="invoice-1">
        <InvoicePageOne />
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const InvoicePageOne = defineAsyncComponent(() => import("@/components/theme/ecommerce/invoice/invoice1/InvoicePageOne.vue"))
</script>