<template>
    <div class="container-fluid">
        <div class="row">
            <MasonryDesc />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { defineAsyncComponent } from 'vue';
const MasonryDesc = defineAsyncComponent(() => import("@/components/theme/gallery/masonry/MasonryDesc.vue"))
</script>