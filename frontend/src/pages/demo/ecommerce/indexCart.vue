<template>
    <div class="container-fluid">
        <div class="row">
            <ProductCart />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const ProductCart = defineAsyncComponent(() => import("@/components/theme/ecommerce/cart/ProductCart.vue"))
</script>