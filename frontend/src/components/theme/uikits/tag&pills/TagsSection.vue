<template>
    <Card3 colClass="col-sm-12 col-xl-6" cardClass="height-equal" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Badge headings example" :desc="desc">
        <div v-for="(item, index) in badgeheadings" :key="index" v-html="item.title">

        </div>
    </Card3>


    <Card3 colClass="col-sm-12 col-xl-6" cardClass="height-equal" titleClass="mb-0" pre="true" preClass="f-m-light mt-1"
        headerTitle="true" title="Badges as part buttons" :desc="desc1">
        <div class="badge-spacing flex-column align-items-start">
            <button class="btn  d-flex align-items-center" :class="item.class" v-for="(item, index) in buttons" :key="index"
                type="button">{{ item.title }} <span
                    class="badge rounded-circle btn-p-space badge-light text-dark ms-2"><vue-feather
                        :type="item.icon"></vue-feather></span></button>

        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { badgeheadings, buttons } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" All html headings, <code>&lt;h1&gt;</code> through <code>&lt;h6&gt;</code> , are available in <code>.badge </code>tags.")
let desc1 = ref<string>("<code>.badge</code> can be used as part of <code>.btn</code> to provide a icons.")
</script>