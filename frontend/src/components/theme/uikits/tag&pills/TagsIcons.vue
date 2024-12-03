<template>
    <Card3 colClass="col-sm-12 col-xl-6" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Badge tags with icon" :desc="desc">
        <div class="badge-spacing"><a class="badge b-ln-height " :class="item.class" v-for="(item, index) in icon"
                :key="index" href="#"><vue-feather :type="item.title"></vue-feather></a>
        </div>
    </Card3>


    <Card3 colClass="col-sm-12 col-xl-6" titleClass="mb-0" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Rounded pills with icons" :desc="desc">
        <div class="badge-spacing"><a class="badge rounded-circle p-2" :class="item.class" v-for="(item, index) in icon"
                :key="index" href="#"><vue-feather :type="item.title"></vue-feather></a>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { icon } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.badge </code>utility class to make more icons.")
let desc1 = ref<string>(" Use the <code>.rounded-pill</code> utility class to make icons badges more rounded with a larger <code>border-radius</code>.")
</script>