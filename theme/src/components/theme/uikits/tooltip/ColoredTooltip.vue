<template>
    <Card3 colClass="col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Colored tooltip" :desc="desc">
        <div class="common-flex">
            <button class="mb-0 me-0 btn btn-primary" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Primary">Primary</button>
            <button class="mb-0 me-0 btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Secondary">Secondary</button>
            <button class="mb-0 me-0 btn btn-success" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Success">Success</button>
            <button class="mb-0 me-0 btn btn-warning text-black" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Warning">Warning</button>
            <button class="mb-0 me-0 btn btn-danger" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-title="Danger">Danger</button>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, } from 'vue'
import { Tooltip } from "bootstrap";
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>btn- *</code> to change dark background color and <code>data-bs-placement='*' </code>to tooltip positions change.")
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>