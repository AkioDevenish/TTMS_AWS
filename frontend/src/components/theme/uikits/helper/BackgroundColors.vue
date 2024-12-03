<template>
    <Card3 colClass="col-12" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Background colors" :desc="desc">
        <div class="row g-3">
            <div class="col-xl-4 col-sm-6" v-for="(items, index) in backgroundcolor" :key="index">
                <div class="border-wrapper h-100 border">
                    <h5 class="f-w-600 mb-3">{{ items.title }}</h5>
                    <div class="helper-common-box" v-for="(item, index) in items.children" :key="index">
                        <div class="helper-box" :class="item.class"></div><span>{{ item.title }}</span>
                    </div>
                </div>
            </div>
            <div class="col-xl-4 col-sm-12">
                <div class="border-wrapper h-100 border">
                    <h5 class="f-w-600 mb-3">Extended background colors</h5>
                    <div class="helper-common-box">
                        <div class="helper-box light-card"> </div><span>.light-card</span>
                    </div>
                    <div class="helper-common-box">
                        <div class="helper-box light-background border"></div><span>.light-background </span>
                    </div>
                </div>
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { backgroundcolor } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the <code>.bg-* </code>and <code>.alert-light-* </code>colors in Mofi theme. Use of any components.")
</script>