<template>
    <div class="container-fluid">
        <div class="row">
            <MaskInput />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const MaskInput = defineAsyncComponent(() => import("@/components/theme/forms/formcontrol/inputmask/MaskInput.vue"))
</script>