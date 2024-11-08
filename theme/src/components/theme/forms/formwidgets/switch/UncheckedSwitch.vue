<template>
    <Card3 colClass="col-xl-4 col-sm-6" cardbodyClass="common-flex flex-column switch-wrapper" cardClass="height-equal"
        pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Unchecked switch" :desc="desc">
        <div class="d-flex" v-for="(item, index) in Unchecked" :key="index">
            <div class="text-end">
                <label class="switch mb-0">
                    <input type="checkbox" :checked="item.checked"><span class="switch-state " :class="item.class"> </span>
                </label>
            </div>
            <label class="col-form-label m-l-10">{{ item.label }}</label>
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { Unchecked } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.bg-*</code> class through created default switches. ")
</script>