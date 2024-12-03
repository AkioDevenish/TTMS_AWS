<template>
    <Card3 colClass="col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Tooltip  directions"
        :desc="desc">
        <div class="common-flex">
            <button class="btn btn-primary mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="top"
                title="Tooltip on top">Tooltip on top</button>
            <button class="btn btn-secondary mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="right"
                title="Tooltip on right">Tooltip on right</button>
            <button class="btn btn-success mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="bottom"
                title="Tooltip on bottom">Tooltip on bottom</button>
            <button class="btn btn-warning mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="left"
                title="Tooltip on left">Tooltip on left</button>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, } from 'vue'
import { Tooltip } from "bootstrap";
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>btn-*</code> to change dark background color and<code> data-bs-placement='*'</code>[top/right/bottom/left] to tooltip direction change.")
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>