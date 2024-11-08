<template>
    <div class="container-fluid">
        <div class="row">
            <FileSidebar />
            <FileContent />
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'

const FileSidebar = defineAsyncComponent(() => import("@/components/theme/filemaneger/FileSidebar.vue"))
const FileContent = defineAsyncComponent(() => import("@/components/theme/filemaneger/FileContent.vue"))
</script>