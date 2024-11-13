<template>
    <div class="checkout">
        <Card3 colClass="container-fluid" headerTitle="true" title="Billing Details">
            <div class="row">
                <CheckoutForm />
                <CheckoutDetail />
            </div>
        </Card3>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
const CheckoutForm = defineAsyncComponent(() => import("@/components/theme/ecommerce/checkout/CheckoutForm.vue"))
const CheckoutDetail = defineAsyncComponent(() => import("@/components/theme/ecommerce/checkout/CheckoutDetail.vue"))
</script>