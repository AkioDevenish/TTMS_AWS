<template>
    <Card3 colClass="col-sm-12 col-xl-6" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Outline dark and light alerts" :desc="desc">
        <div class="alert txt-primary border-primary alert-dismissible fade show" role="alert"><vue-feather
                type="clock"></vue-feather>
            <p>One of <strong>YouTube's</strong>most crucial ranking factors is Watch Time.</p>
            <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div class="alert txt-success border-success outline-2x alert-dismissible fade show alert-icons" role="alert">
            <vue-feather type="thumbs-up"></vue-feather>
            <p><b> Well done! </b>You successfully read this important message.</p>
            <button class="btn-close" type="button" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    </Card3>

    <Card3 colClass="col-sm-12 col-xl-6" cardbodyClass="dark-txt" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Alerts with icons and text actions" :desc="desc1">
        <div class="alert border-warning alert-dismissible fade show p-0" role="alert">
            <div class="alert-arrow bg-warning"><i class="icon-timer"></i></div>
            <p>Your time Over after <strong class="txt-dark">5</strong> minute</p>
            <button class="p-0 border-0 me-2 ms-auto" type="button" data-bs-dismiss="alert" aria-label="Close"><span
                    class="bg-warning px-3 py-1" aria-hidden="true">Check</span></button>
        </div>
        <div class="alert border-danger alert-dismissible fade show p-0 mb-0" role="alert">
            <div class="alert-arrow bg-danger"><i class="icon-heart"></i></div>
            <p>Oh snap! Change a few things up <strong class="txt-dark"> Notification check</strong></p>
            <button class="p-0 border-0 me-2 ms-auto" type="button" data-bs-dismiss="alert" aria-label="Close"><span
                    class="bg-danger text-white px-3 py-1" aria-hidden="true">Alert</span></button>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'

const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.border-* </code>utility class to quickly provide matching border and border-width within any alert.")
let desc1 = ref<string>("Use the <code>.dismiss-text</code> class to add dismiss text instead of icon")
</script>