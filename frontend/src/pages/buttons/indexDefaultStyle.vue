<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <DefultsButtons />
                <DefultsButtons2 />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const DefultsButtons = defineAsyncComponent(() => import("@/components/theme/buttons/default/DefultsButtons.vue"))
const DefultsButtons2 = defineAsyncComponent(() => import("@/components/theme/buttons/default/DefultsButtons2.vue"))

</script>