<template>
    <div class="container-fluid">
        <div class="row">
            <SimpleWizard />
            <ShippingForm />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const ShippingForm = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/ShippingForm.vue"))
const SimpleWizard = defineAsyncComponent(() => import("@/components/theme/forms/formlayout/formwizard/SimpleWizard.vue"))
</script>