<template>
    <Card3 colClass="col-xl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Default lists"
        :desc="desc">
        <ul class="list-group">
            <li class="list-group-item" v-for="(item, index) in defaults" :key="index"> <i
                    class="icofont icofont-arrow-right"></i>{{ item.title }}</li>

        </ul>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { defaults } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.list-group </code>define the list of items. and used <code>.list-group-item </code>to indicate the current content.")
</script>