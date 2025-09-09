<template>
    <div class="container-fluid">
        <div class="row">
            <DefaultDropzone />
            <ImageDropzone />
            <SingleDropzone />
            <MultiDropzone />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const DefaultDropzone = defineAsyncComponent(() => import("@/components/theme/advance/dropzone/DefaultDropzone.vue"))
const ImageDropzone = defineAsyncComponent(() => import("@/components/theme/advance/dropzone/ImageDropzone.vue"))
const SingleDropzone = defineAsyncComponent(() => import("@/components/theme/advance/dropzone/SingleDropzone.vue"))
const MultiDropzone = defineAsyncComponent(() => import("@/components/theme/advance/dropzone/MultiDropzone.vue"))
</script>