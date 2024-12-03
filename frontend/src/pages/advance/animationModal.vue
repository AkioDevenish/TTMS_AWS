<template>
    <div class="container-fluid">
        <div class="row">
            <AnimationBox />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const AnimationBox = defineAsyncComponent(() => import("@/components/theme/advance/animation/AnimationBox.vue"))

</script>