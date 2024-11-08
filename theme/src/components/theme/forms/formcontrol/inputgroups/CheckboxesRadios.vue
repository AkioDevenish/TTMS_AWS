<template>
    <Card3 colClass="col-md-6" pre="true" cardbodyClass="checkbox-checked card-wrapper input-group-wrapper"
        preClass="f-m-light mt-1" headerTitle="true" title="Checkboxes and radios" :desc="desc">
        <div class="input-group" v-for="(item, index) in checkboxes" :key="index">
            <div class="input-group-text">
                <input class="form-check-input mt-0" :type="item.type" value="" :checked="item.checked"
                    aria-label="Checkbox for following text input">
            </div>
            <input class="form-control" type="text" aria-label="Text input with checkbox">
        </div>
    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { checkboxes } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" Place any checkbox or radio option within an input group's addon instead of text. We recommend adding <code>.mt-0</code> to the <code>.form-check-input</code> when there's no visible text next to the input.")
</script>