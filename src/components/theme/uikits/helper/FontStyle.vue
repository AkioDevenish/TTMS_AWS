<template>
    <Card3 colClass="col-xl-6" cardClass="height-equal" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Font-style" :desc="desc">
        <p :class="item.class" v-for="(item, index) in fontstyle" :key="index" v-html="item.title">
        </p>
    </Card3>


    <Card3 colClass="col-xl-6" cardClass="height-equal" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Font weight" :desc="desc1">
        <div class="helper-common-box" v-for="(item, index) in fontweght" :key="index">
            <div :class="item.class">
                {{ item.title }}</div>
        </div>
    </Card3>


    <Card3 colClass="col-xl-6" cardClass="height-equal" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Text colors" :desc="desc2">
        <div v-for="(item, index) in textcolors" :key="index">
            <div class="helper-common-box"></div>
            <div :class="item.class" v-html="item.title">
            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { fontstyle, fontweght, textcolors } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Use the font-style like: <code> .f-s-*[normal/italic/oblique/initial/inherit]</code>.")
let desc1 = ref<string>("  Use the font-weight classes like: <code>.f-w-* [100/300/400/600/700/900]</code>")
let desc2 = ref<string>(" Use the text color for <code>.font-*</code> class.")
</script>