<template>
    <Card3 cardbodyClass="progress-showcase" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Basic progress bars" :desc="desc">
        <div class="row">
            <div class="col">
                <h6 class="mb-2">0% Getting Started </h6>
                <div class="progress mb-4">
                    <div class="progress-bar-animated progress-bar-striped text-center" role="progressbar" aria-valuenow="0"
                        aria-valuemin="0" aria-valuemax="100"> </div>
                </div>
                <div v-for="(item, index) in custom" :key="index">
                    <h6 class="mb-2">{{ item.title }}</h6>
                    <div class="progress mb-4">
                        <div class="progress-bar-animated progress-bar-striped  text-center" :class="item.class"
                            role="progressbar" :style="{ 'width': item.width }" aria-valuenow="30" aria-valuemin="0"
                            aria-valuemax="100">30%</div>
                    </div>
                </div>


            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { custom } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.progress-bar-animated </code>and <code>.progress-bar-striped </code>to animate the stripes right to left.")
</script>