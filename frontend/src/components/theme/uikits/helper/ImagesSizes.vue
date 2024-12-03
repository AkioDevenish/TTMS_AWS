<template>
    <Card3 colClass="col-xl-6" cardClass="height-equal" cardheaderClass="card-no-border pb-0" titleClass="mb-0" pre="true"
        preClass="f-m-light mt-1" headerTitle="true" title="Images sizes" :desc="desc">
        <div class="gradient-border gap-3"><img :class="item.class" v-for="(item, index) in imgesize" :key="index"
                :src="getImages(item.img)" alt="img-size-30"></div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { imgesize } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the width and height of images class like: <code>.img-* </code>and <code>.img-h-*</code>.")
</script>