<template>
    <Card3 colClass="col-xl-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Link color in light theme"
        :desc="desc">
        <div class="row">
            <div class="col-xl-6" v-for="(items, index) in lightalert" :key="index">
                <div v-for="(item, index) in items.childern" :key="index">
                    <p class="mb-2 f-w-500">{{ item.title }}</p>
                    <div class="alert mb-3" :class="item.class" role="alert">
                        <p :class="item.alertclass">This is a <a class="alert-link" :class="item.alertclass" href="#">{{
                            item.text }}</a>
                            with an example link.Check it out.</p>
                    </div>
                </div>


            </div>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { lightalert } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.alert-link</code> utility class to quickly provide matching colored links within any alert.")
</script>