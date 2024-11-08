<template>
    <Card3 colClass="col-md-6" cardbodyClass="fill-tooltip" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Filled tooltip" :desc="desc">
        <div class="common-flex">
            <button class="btn btn-outline-primary mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-html="true"
                data-bs-placement="top" data-bs-title="Tooltip Primary">Tooltip Primary</button>
            <button class="btn btn-outline-secondary mb-0 me-0" type="button" data-bs-toggle="tooltip"
                data-bs-placement="top" data-bs-html="true" data-bs-title="Tooltip Secondary">Tooltip Secondary</button>
            <button class="btn btn-outline-success mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-html="true" data-bs-title="Tooltip Success">Tooltip Success</button>
            <button class="btn btn-outline-info mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-html="true" data-bs-title="Tooltip Info">Tooltip Info</button>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, } from 'vue'
import { Tooltip } from "bootstrap";
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Tooltip in hover effect through fill dark color.<code>[.btn-outline-*]</code>. and <code>data-bs-title </code>to the content under the HTML Tag.")
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>