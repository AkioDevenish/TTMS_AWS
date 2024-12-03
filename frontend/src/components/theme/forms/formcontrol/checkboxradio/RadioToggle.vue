<template>
    <Card3 colClass="col-md-6" pre="true" cardbodyClass="common-flex main-radio-toggle" preClass="f-m-light mt-1"
        headerTitle="true" title="Radio toggle buttons " :desc="desc">
        <div v-for="(item, index) in toggle" :key="index">
            <input class="btn-check radio-light-secondary" :id="item.id" type="radio" name="options" :checked="item.checked"
                :disabled="item.disabled">
            <label class="btn list-light-secondary" :for="item.id">{{ item.label }}</label>
        </div>

    </Card3>


    <Card3 colClass="col-md-6" pre="true" cardbodyClass="common-flex main-checkbox-toggle" preClass="f-m-light mt-1"
        headerTitle="true" title="Outlined checkbox styles" :desc="desc1">
        <div v-for="(item, index) in outlined " :key="index">
            <input class="btn-check" :id="item.id" type="checkbox" :checked="item.checked">
            <label class="btn " :class="item.class" for="btn-check-outlined">{{ item.label }}</label>
        </div>

    </Card3>
</template>
<script lang="ts" setup>
import { ref, defineAsyncComponent } from 'vue'
import { toggle, outlined } from "@/core/data/forms"
const Card3 = defineAsyncComponent(() => import("@/components/common/card/CardData3.vue"))
let desc = ref<string>(" The choice between these two approaches will depend on the type of toggle you are creating, and whether or not the toggle will make sense to users when announced as a checkbox or as an actual button. <code>[any one selected]</code>.")

let desc1 = ref<string>("The choice between these two approaches will depend on the type of toggle you are creating, and whether or not the toggle will make sense to users when announced as a checkbox or as an actual button. <code>[multiple selected]</code>.")
</script>