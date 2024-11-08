<template>
    <Card3 colClass="col-xl-6" cardbodyClass="progress-showcase" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Progress bars striped" :desc="desc">
        <div class="row">
            <div class="col">
                <div class="progress" v-for="(item, index) in striped" :key="index">
                    <div class="progress-bar progress-bar-striped" :class="item.class" role="progressbar"
                        :style="{ 'width': item.width }" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>
    </Card3>


    <Card3 colClass="col-xl-6" cardbodyClass="progress-showcase" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Progress bars animated" :desc="desc">
        <div class="row">
            <div class="col">
                <div class="progress" v-for="(item, index) in striped" :key="index">
                    <div class="progress-bar-animated  progress-bar-striped" :class="item.class" role="progressbar"
                        :style="{ 'width': item.width }" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { striped } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Add <code>.progress-bar-striped</code> to any <code>.progress-bar </code> to apply a stripe via CSS gradient over the progress bar's background color Using CSS Effects.")
let desc1 = ref<string>("The striped gradient can also be animated. Add <code>.progress-bar-animated</code> to<code>.progress-bar</code> to animate the stripes right to left via CSS3 animations.")
</script>