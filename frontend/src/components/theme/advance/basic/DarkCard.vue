<template>
    <Card3 colClass="col-sm-12" cardbodyClass="bg-dark" titleClass="text-white" cardhaderClass="bg-dark" footer="true"
        footersClass="text-white" footerclass="bg-dark" cardClass="Dark Color Card" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Icon In Heading" footertitle="Card Footer" :desc="desc">
        <div class="d-flex align-items-center gap-3 pills-blogger">
            <div class="blog-wrapper"> <img class="blog-img" src="@/assets/images/dashboard-2/headphones.png"
                    alt="head-phone"></div>
            <div class="blog-content">
                <p> <em class="txt-danger fw-bold">Smart headphones</em> — also called smart earbuds or hearable —
                    are high-tech in-ear devices that do more than transmit audio. These headphones are usually
                    wireless, and they can sync up with your phone, tablet, computer or other Bluetooth-enabled
                    device. The main appeal of hearables is convenience, as they allow you to complete common tasks
                    without directly accessing your phone or computer. Smart wireless headphones sync up to other
                    devices using Bluetooth technology, and many of their features rely on data from your smartphone
                    or computer.</p>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { card } from "@/core/data/advance"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.bg-dark </code>color for dark background card.")
</script>