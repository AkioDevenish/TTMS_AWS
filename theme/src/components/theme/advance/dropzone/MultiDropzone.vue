<template>
    <Card3 colClass="col-lg-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Multi File Upload"
        :desc="desc">
        <form class="dropzone" id="multiFileUpload" action="/upload.php">
            <DropZone :maxFileSize="Number(7000000)" :uploadOnDrop="true" :multipleUpload="true" :parallelUpload="2" />
        </form>
    </Card3>
</template>
<script lang="ts" setup>
import DropZone from "dropzone-vue";
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.dropzone </code> class through create upload files.<code>[https://www.dropzone.dev/].</code>")
</script>
<style scoped>
@import 'dropzone-vue/dist/dropzone-vue.common.css';
</style>