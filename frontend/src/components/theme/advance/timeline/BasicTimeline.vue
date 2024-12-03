<template>
    <Card3 colClass="col-xl-6 box-col-6 notification main-timeline" cardbodyClass="dark-timeline basic-timeline"
        cardClass="height-equal" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Basic Timeline"
        :desc="desc">
        <ul>
            <li class="d-flex" v-for="(item, index) in basictimeline" :key="index">
                <div :class="item.dotClass"></div>
                <div class="w-100 ms-3">
                    <p class="d-flex justify-content-between mb-2"><span class="date-content light-background">{{ item.date
                    }}</span><span>{{ item.time }}</span></p>
                    <h6 class="mb-0">{{ item.title }}<span class="dot-notification"></span></h6>
                    <p class="f-light">{{ item.desc }}</p>
                </div>
            </li>
        </ul>
    </Card3>
</template>
<script lang="ts" setup>
import { basictimeline } from "@/core/data/advance"
import { defineAsyncComponent, ref } from 'vue'
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.main-basic-timeline </code>class through made basic timeline.")

</script>                