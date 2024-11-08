<template>
    <Card3 colClass="col-md-6" pre="true" cardbodyClass="main-segment-btn card-wrapper input-group-wrapper"
        preClass="f-m-light mt-1" headerTitle="true" title="Segmented buttons " :desc="desc">
        <div class="input-group" v-for="(item, index) in segmented" :key="index">
            <input class="form-control" type="text" aria-label="Text input with segmented dropdown button"
                v-if="item.input2">
            <button class="btn " :class="item.class" type="button">{{ item.label }} </button>
            <button class="btn  dropdown-toggle dropdown-toggle-split" :class="item.class1" type="button"
                data-bs-toggle="dropdown" aria-expanded="false"><span class="visually-hidden">Toggle
                    Dropdown</span></button>
            <ul class="dropdown-menu  dropdown-block" :class="item.dropclass">
                <li v-for="(items, index) in item.children" :key="index"><a :class="items.class" :href="items.href">{{
                    items.text }}</a></li>
            </ul>
            <input class="form-control" type="text" v-if="item.input1"
                aria-label="Text input with segmented dropdown button">
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { segmented } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Multiple add-ons are supported and can be mixed with<code> dropdowns</code> versions.")
</script>