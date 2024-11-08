<template>
    <Card3 colClass="col-xxl-4 col-md-6" cardhaderClass="rating-header" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Heart Rating Bar" :desc="desc">
        <div class="rating-container">
            <svg style="position: absolute; width: 0; height: 0;" height="0" version="1.1"
                xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                <defs>
                    <symbol id="icon-heart" class="icon" viewBox="0 0 32 32">
                        <path
                            d="M23.6 2c-3.363 0-6.258 2.736-7.599 5.594-1.342-2.858-4.237-5.594-7.601-5.594-4.637 0-8.4 3.764-8.4 8.401 0 9.433 9.516 11.906 16.001 21.232 6.13-9.268 15.999-12.1 15.999-21.232 0-4.637-3.763-8.401-8.4-8.401z" />
                    </symbol>
                </defs>
            </svg>
            <rate :length="5" :value="0" :showcount="true" iconref="icon-heart" />
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Heart Rating is displayed using <code>#u-rating-heart </code> id using javascript.")
</script>