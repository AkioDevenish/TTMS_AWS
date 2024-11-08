<template>
    <Card3 colClass="col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="File input" :desc="desc">
        <div class="mb-3">
            <label class="form-label" for="formFile">Default file input example</label>
            <input class="form-control" id="formFile" type="file">
        </div>
        <div class="mb-3">
            <label class="form-label" for="formFileMultiple">Multiple files input example</label>
            <input class="form-control" id="formFileMultiple" type="file" multiple>
        </div>
        <div class="mb-3">
            <label class="form-label" for="formFileDisabled">Disabled file input example</label>
            <input class="form-control" id="formFileDisabled" type="file" disabled>
        </div>
        <div class="mb-3">
            <label class="form-label" for="formFileSm">Small file input example</label>
            <input class="form-control form-control-sm" id="formFileSm" type="file">
        </div>
        <div>
            <label class="form-label" for="formFileLg">Large file input example</label>
            <input class="form-control form-control-lg" id="formFileLg" type="file">
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("For default file/multiple file/disabled file/small file/large file input for use <code>&lt;input&gt; </code>with <code>(type='file').</code>")
</script>