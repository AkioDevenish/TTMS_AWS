<template>
    <div class="row">
        <div class="col">
            <div class="mb-3">
                <label>Upload project file</label>
                <DropZone :maxFileSize="Number(60000000)" :uploadOnDrop="true">
                </DropZone>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import DropZone from "dropzone-vue";
</script>
<style scoped>
@import 'dropzone-vue/dist/dropzone-vue.common.css';
</style>