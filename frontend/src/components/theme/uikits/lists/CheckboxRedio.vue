<template>
    <Card3 colClass="col-xl-4 col-md-6" cardbodyClass="dark-list" pre="true" preClass="f-m-light mt-1" headerTitle="true"
        title="Lists with checkbox" :desc="desc">
        <ul class="list-group">
            <li class="list-group-item" v-for="(item, index) in checkbox" :key="index">
                <input class="form-check-input me-1 " :class="item.class" :id="item.ids" type="checkbox" value="">
                <label class="form-check-label  mb-0" :class="item.txt" :for="item.ids">{{ item.title }}</label>
            </li>
        </ul>
    </Card3>

    <Card3 colClass="col-xl-4 col-md-6" pre="true" preClass="f-m-light mt-1" headerTitle="true" title="Lists with radios"
        :desc="desc">
        <ul class="list-group">
            <li class="list-group-item" v-for="(item, index) in radio" :key="index">
                <input class="form-check-input me-1 " :class="item.class" :id="item.ids" type="radio" name="listGroupRadio"
                    value="">
                <label class="form-check-label mb-0" :for="item.ids">{{ item.title }}</label>
            </li>
        </ul>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { checkbox, radio } from "@/core/data/uikits"
import { getImages } from "@/composables/common/getImages"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>("Use the <code>.form-check-input </code>to check your checkbox.")
let desc1 = ref<string>("Use the <code>.form-check-input </code>to check your radio buttons.")
</script>