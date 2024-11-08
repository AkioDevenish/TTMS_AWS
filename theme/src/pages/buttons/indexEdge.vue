<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-sm-12">
                <EdgesButtons />
                <EdgesButtons2 />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const EdgesButtons = defineAsyncComponent(() => import("@/components/theme/buttons/edge/EdgesButtons.vue"))
const EdgesButtons2 = defineAsyncComponent(() => import("@/components/theme/buttons/edge/EdgesButtons2.vue"))

</script>