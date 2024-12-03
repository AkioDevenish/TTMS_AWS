<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <RaisedsButtons />
                <RaisedsButtons2 />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const RaisedsButtons = defineAsyncComponent(() => import("@/components/theme/buttons/raised/RaisedsButtons.vue"))
const RaisedsButtons2 = defineAsyncComponent(() => import("@/components/theme/buttons/raised/RaisedsButtons2.vue"))

</script>