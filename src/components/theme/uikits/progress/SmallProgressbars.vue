<template>
    <Card3 colClass="col-xl-6" cardClass="height-equal" cardbodyClass="progress-showcase progress-b-space" titleClass="mb-0"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Small progress bars" :desc="desc">
        <div class="row">
            <div class="col">
                <div class="progress sm-progress-bar overflow-visible mt-4">
                    <div class="progress-bar-animated small-progressbar bg-primary rounded-pill progress-bar-striped"
                        role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"><span
                            class="txt-primary progress-label">30 MB Data</span><span class="animate-circle"></span></div>
                </div>
                <div class="progress sm-progress-bar overflow-visible">
                    <div class="progress-bar-animated small-progressbar bg-primary rounded-pill progress-bar-striped"
                        role="progressbar" style="width: 50%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"><span
                            class="txt-primary progress-label">50 MB Data</span><span class="animate-circle"></span></div>
                </div>
                <div class="progress sm-progress-bar overflow-visible">
                    <div class="progress-bar-animated small-progressbar bg-primary rounded-pill progress-bar-striped"
                        role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"><span
                            class="txt-primary progress-label">75 MB Data</span><span class="animate-circle"></span></div>
                </div>
                <div class="progress sm-progress-bar overflow-visible">
                    <div class="progress-bar-animated small-progressbar bg-primary rounded-pill progress-bar-striped"
                        role="progressbar" style="width: 90%" aria-valuenow="90" aria-valuemin="0" aria-valuemax="100"><span
                            class="txt-primary progress-label">90 MB Data</span><span class="animate-circle"></span></div>
                </div>
            </div>
        </div>
    </Card3>


    <Card3 colClass="col-xl-6" cardClass="height-equal" cardbodyClass="progress-showcase " titleClass="mb-0" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Large progress bars" :desc="desc1">
        <div class="row">
            <div class="col">
                <div class="progress lg-progress-bar" v-for="(item, index) in basic" :key="index">
                    <div class="progress-bar " :class="item.class" role="progressbar" :style="{ 'width': item.width }"
                        aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">{{ item.width }}</div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { basic } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use <code> .sm-progress-bar</code>  class to change progress size to small.")
let desc1 = ref<string>("Use <code> .sm-progress-bar</code>  class to change progress size to small.")
</script>