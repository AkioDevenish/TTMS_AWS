<template>
    <Card3 colClass="col-sm-12 col-xl-6" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Pills contextual variations" :desc="desc">
        <div class="badge-spacing"><span class="badge rounded-pill " :class="item.class" v-for="(item, index) in badges"
                :key="index">{{ item.title }}</span>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { badges } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.rounded-pill</code> utility class to make badges more rounded with a larger <code>border-radius</code>.")
</script>