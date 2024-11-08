<template>
    <Card3 colClass="col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="HTML elements with hover effect" :desc="desc">
        <div class="common-flex">
            <button class="btn bg-primary mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-html="true"
                data-bs-placement="top" data-bs-title="&lt;em&gt;Thank&lt;/em&gt; &lt;u&gt;you&lt;/u&gt;">Notifications
                Received</button>
            <button class="btn bg-warning mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-html="true" data-bs-title="&lt;b&gt;Thank&lt;/b&gt; &lt;em&gt;you&lt;/em&gt;">Last
                Warning</button>
            <button class="btn bg-danger mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-html="true" data-bs-title="&lt;em&gt;Thank&lt;/em&gt; &lt;u&gt;you&lt;/u&gt;">It's
                Danger</button>
            <button class="btn bg-info mb-0 me-0" type="button" data-bs-toggle="tooltip" data-bs-placement="top"
                data-bs-html="true" data-bs-title="&lt;b&gt;Thank&lt;/b&gt; &lt;em&gt;you&lt;/em&gt;">Coming
                soon</button>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent, onMounted, } from 'vue'
import { Tooltip } from "bootstrap";
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>bg-*-light</code> to change light background color and <code>data-bs-title </code> to the content under the HTML tag.")
onMounted(() => {

    new Tooltip(document.body, {
        selector: "[data-bs-toggle='tooltip']",
    })
})
</script>