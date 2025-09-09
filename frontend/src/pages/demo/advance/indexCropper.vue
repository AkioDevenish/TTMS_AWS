<template>
    <div class="container-fluid">
        <div class="img-cropper">
            <ImageCropper />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const ImageCropper = defineAsyncComponent(() => import("@/components/theme/advance/cropper/ImageCropper.vue"))
</script>