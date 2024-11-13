<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <FlatsButtons />
                <FlatsButtons2 />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const FlatsButtons = defineAsyncComponent(() => import("@/components/theme/buttons/flat/FlatsButtons.vue"))
const FlatsButtons2 = defineAsyncComponent(() => import("@/components/theme/buttons/flat/FlatsButtons2.vue"))

</script>