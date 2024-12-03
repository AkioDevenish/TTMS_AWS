<template>
    <Card3 cardbodyClass="progress-showcase" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Basic progress bars" :desc="desc">
        <div class="row">
            <div class="col">
                <div class="progress">
                    <div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                    </div>
                </div>
                <div class="progress" v-for="(item, index) in basic" :key="index">
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
let desc = ref<string>("Progress components are built with two HTML elements, some CSS to set the width, and a few attributes. We use the <code>.progress </code>as a wrapper to indicate the max value of the progress bar. The <code>.progress-bar </code>requires an inline style, utility class, or custom CSS to set their width.")
</script>