<template>
     <div class="row">
         <Card3 colClass="col-sm-12 col-xl-12" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Variations Of Left Ribbons"
        :desc="desc">
        <div class="row g-3">
                <div class="col-sm-6 col-xl-4" v-for="(item, index) in leftribbons" :key="index">
                    <div :class="item.class">
                        <div :class="item.color"><i :class="item.icon" v-if="item.icon"></i>{{ item.info }}</div>
                        <p v-html="item.dis"></p>
                    </div>
                </div>
            </div>
         </Card3>
     </div>
</template>
<script lang="ts" setup>
import { leftribbons } from "@/core/data/advance"
import { defineAsyncComponent,ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the class of <code>.ribbon-*</code>[ribbon-space-bottom/ribbon-clip/ribbon-vertical-left/ribbon-bookmark/ribbon-clip-bottom/ribbon-vertical-left] through create ribbons and all ribbon colors are available.<code>[.ribbon-*] </code>")

</script>