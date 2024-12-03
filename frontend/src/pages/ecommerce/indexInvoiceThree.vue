<template>
    <Card3 colClass="container invoice-2">
        <InvoicePageThree />
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const InvoicePageThree = defineAsyncComponent(() => import("@/components/theme/ecommerce/invoice/invoice3/InvoicePageThree.vue"))
</script>