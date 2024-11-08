<template>
    <Card3 colClass="col-12" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Borders and displays" :desc="desc">
        <div class="row g-3">
            <div class="col-xl-4 col-sm-6" v-for="(item, index) in border" :key="index">
                <div class="border-wrapper h-100 border">
                    <h5 class="f-w-600 mb-3">{{ item.title }} </h5>
                    <div class="helper-common-box" v-for="(items, index) in item.children" :key="index">
                        <div :class="items.class"></div><span>{{ items.title }}</span>
                    </div>

                </div>
            </div>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { border } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use border utilities to add or remove an element's borders.")
</script>